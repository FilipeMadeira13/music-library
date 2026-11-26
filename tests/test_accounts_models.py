import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from accounts.models import User
from library.choices import Service

pytestmark = pytest.mark.django_db


def test_auth_user_model_is_custom_user() -> None:
    assert get_user_model() is User


def test_create_user_normalizes_email_and_hashes_password() -> None:
    user = User.objects.create_user("Ana@EXAMPLE.com", "s3cret-pass")

    assert user.email == "Ana@example.com"
    assert user.check_password("s3cret-pass")
    assert not user.is_staff
    assert not user.is_superuser
    assert user.preferred_service is None
    assert str(user) == "Ana@example.com"


def test_create_user_without_email_fails() -> None:
    with pytest.raises(ValueError, match="e-mail"):
        User.objects.create_user("", "s3cret-pass")


def test_create_superuser_sets_flags() -> None:
    admin = User.objects.create_superuser("admin@example.com", "s3cret-pass")

    assert admin.is_staff
    assert admin.is_superuser


@pytest.mark.parametrize("flag", ["is_staff", "is_superuser"])
def test_create_superuser_rejects_false_flags(flag: str) -> None:
    with pytest.raises(ValueError, match=flag):
        User.objects.create_superuser("admin@example.com", "s3cret-pass", **{flag: False})


def test_duplicate_email_is_rejected() -> None:
    User.objects.create_user("ana@example.com", "s3cret-pass")

    with pytest.raises(IntegrityError):
        User.objects.create_user("ana@example.com", "other-pass")


def test_email_is_the_login_and_username_is_gone() -> None:
    assert User.USERNAME_FIELD == "email"
    assert User.REQUIRED_FIELDS == []
    field_names = {f.name for f in User._meta.get_fields()}  # noqa: SLF001 - _meta is Django's public model API
    assert "username" not in field_names
    assert "email" in field_names


@pytest.mark.parametrize("service", [Service.TIDAL, Service.QOBUZ, Service.OTHER])
def test_preferred_service_accepts_known_services(service: Service) -> None:
    user = User.objects.create_user("ana@example.com", "s3cret-pass", preferred_service=service)

    user.full_clean()
    user.refresh_from_db()
    assert user.preferred_service == service


def test_preferred_service_rejects_unknown_value() -> None:
    user = User(email="ana@example.com", preferred_service="napster")
    user.set_password("s3cret-pass")

    with pytest.raises(ValidationError) as exc:
        user.full_clean()
    assert "preferred_service" in exc.value.message_dict
