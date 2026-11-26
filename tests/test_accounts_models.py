import pytest
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, connection

from accounts.models import User
from library.choices import Service

pytestmark = pytest.mark.django_db


def test_auth_user_model_is_custom_user() -> None:
    assert get_user_model() is User


def test_create_user_normalizes_email_and_hashes_password(password: str) -> None:
    user = User.objects.create_user("  Ana@EXAMPLE.com ", password)

    assert user.email == "ana@example.com"
    assert user.check_password(password)
    assert not user.is_staff
    assert not user.is_superuser
    assert user.preferred_service is None
    assert str(user) == "ana@example.com"


def test_create_user_without_password_has_unusable_password() -> None:
    user = User.objects.create_user("oauth@example.com")

    assert not user.has_usable_password()


@pytest.mark.parametrize("email", ["", "   "])
def test_create_user_without_email_fails(email: str, password: str) -> None:
    with pytest.raises(ValueError, match="required"):
        User.objects.create_user(email, password)


@pytest.mark.parametrize("email", ["sem-arroba", "ana@", "@example.com"])
def test_create_user_with_malformed_email_fails(email: str, password: str) -> None:
    with pytest.raises(ValueError, match="Invalid e-mail"):
        User.objects.create_user(email, password)
    assert not User.objects.exists()


def test_create_superuser_sets_flags(password: str) -> None:
    admin = User.objects.create_superuser("admin@example.com", password)

    assert admin.is_staff
    assert admin.is_superuser


@pytest.mark.parametrize("flag", ["is_staff", "is_superuser"])
def test_create_superuser_rejects_false_flags(flag: str, password: str) -> None:
    with pytest.raises(ValueError, match=flag):
        User.objects.create_superuser("admin@example.com", password, **{flag: False})


def test_createsuperuser_command_without_input(
    monkeypatch: pytest.MonkeyPatch, password: str
) -> None:
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "Admin@Example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", password)

    call_command("createsuperuser", interactive=False, verbosity=0)

    admin = User.objects.get()
    assert admin.email == "admin@example.com"
    assert admin.is_superuser
    assert admin.check_password(password)


def test_duplicate_email_is_rejected(password: str, other_password: str) -> None:
    User.objects.create_user("ana@example.com", password)

    with pytest.raises(IntegrityError):
        User.objects.create_user("ana@example.com", other_password)


def test_duplicate_email_with_different_case_is_rejected(
    password: str, other_password: str
) -> None:
    User.objects.create_user("ana@example.com", password)

    with pytest.raises(IntegrityError):
        User.objects.create_user("ANA@Example.COM", other_password)


def test_save_normalizes_email_set_directly(password: str) -> None:
    user = User(email=" Ana@Example.COM ")
    user.set_password(password)
    user.save()

    user.refresh_from_db()
    assert user.email == "ana@example.com"


def test_db_rejects_mixed_case_duplicate_written_by_update(password: str) -> None:
    User.objects.create_user("ana@example.com", password)
    other = User.objects.create_user("bia@example.com", password)

    with pytest.raises(IntegrityError):
        User.objects.filter(pk=other.pk).update(email="ANA@example.com")


def test_full_clean_reports_case_insensitive_duplicate(password: str) -> None:
    User.objects.create_user("ana@example.com", password)
    user = User(email="ANA@example.com")
    user.set_password(password)

    with pytest.raises(ValidationError) as exc:
        user.full_clean()
    assert "email" in exc.value.message_dict


@pytest.mark.parametrize("typed", ["ana@example.com", "ANA@Example.com", " Ana@example.com "])
def test_authenticate_by_email_ignores_case(typed: str, password: str) -> None:
    user = User.objects.create_user("Ana@example.com", password)

    assert authenticate(email=typed, password=password) == user


def test_authenticate_with_wrong_password_fails(password: str, other_password: str) -> None:
    User.objects.create_user("ana@example.com", password)

    assert authenticate(email="ana@example.com", password=other_password) is None


def test_email_is_the_login_and_username_is_gone() -> None:
    assert User.USERNAME_FIELD == "email"
    assert User.REQUIRED_FIELDS == []
    with connection.cursor() as cursor:
        columns = {
            c.name
            for c in connection.introspection.get_table_description(cursor, User._meta.db_table)  # noqa: SLF001 - _meta is Django's public model API
        }
    assert "username" not in columns
    assert "email" in columns


@pytest.mark.parametrize("service", [Service.TIDAL, Service.QOBUZ, Service.OTHER])
def test_preferred_service_accepts_known_services(service: Service, password: str) -> None:
    user = User.objects.create_user("ana@example.com", password, preferred_service=service)

    user.full_clean()
    user.refresh_from_db()
    assert user.preferred_service == service


def test_preferred_service_rejects_unknown_value(password: str) -> None:
    user = User(email="ana@example.com", preferred_service="napster")
    user.set_password(password)

    with pytest.raises(ValidationError) as exc:
        user.full_clean()
    assert "preferred_service" in exc.value.message_dict


@pytest.mark.parametrize("value", ["napster", ""])
def test_db_rejects_invalid_preferred_service(value: str, password: str) -> None:
    with pytest.raises(IntegrityError):
        User.objects.create_user("ana@example.com", password, preferred_service=value)
