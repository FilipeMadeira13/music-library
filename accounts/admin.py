from typing import TYPE_CHECKING

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User

# UserAdmin is generic only in django-stubs; subscripting it at runtime fails.
if TYPE_CHECKING:
    _UserAdminBase = DjangoUserAdmin[User]
else:
    _UserAdminBase = DjangoUserAdmin


@admin.register(User)
class UserAdmin(_UserAdminBase):
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "preferred_service", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Informações pessoais"), {"fields": ("first_name", "last_name", "preferred_service")}),
        (
            _("Permissões"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Datas importantes"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
