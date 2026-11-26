import pytest
from django.contrib import admin
from django.test import Client

from accounts.admin import UserAdmin
from accounts.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_client_logged(client: Client, password: str) -> Client:
    superuser = User.objects.create_superuser("admin@example.com", password)
    client.force_login(superuser)
    return client


def test_user_is_registered_with_custom_admin() -> None:
    assert isinstance(admin.site._registry[User], UserAdmin)  # noqa: SLF001 - no public API lists registered ModelAdmins


def test_changelist_and_change_page_render(admin_client_logged: Client, password: str) -> None:
    user = User.objects.create_user("ana@example.com", password)

    changelist = admin_client_logged.get("/admin/accounts/user/", {"q": "ana"})
    change = admin_client_logged.get(f"/admin/accounts/user/{user.pk}/change/")

    assert changelist.status_code == 200
    assert b"ana@example.com" in changelist.content
    assert change.status_code == 200


def test_add_user_through_admin_normalizes_email(
    admin_client_logged: Client, password: str
) -> None:
    response = admin_client_logged.post(
        "/admin/accounts/user/add/",
        {"email": "Bia@Example.com", "password1": password, "password2": password},
    )

    assert response.status_code == 302
    assert User.objects.get(email="bia@example.com").check_password(password)


def test_add_user_through_admin_rejects_case_insensitive_duplicate(
    admin_client_logged: Client,
    password: str,
) -> None:
    User.objects.create_user("bia@example.com", password)

    response = admin_client_logged.post(
        "/admin/accounts/user/add/",
        {"email": "BIA@example.com", "password1": password, "password2": password},
    )

    assert response.status_code == 200
    assert User.objects.filter(email="bia@example.com").count() == 1
