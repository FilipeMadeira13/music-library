"""Admin forms for the e-mail based user (Django's defaults expect ``username``)."""

from typing import TYPE_CHECKING

from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm

from accounts.models import User

# Django's form classes are generic only in django-stubs; subscripting them at runtime fails.
if TYPE_CHECKING:
    _CreationFormBase = BaseUserCreationForm[User]
    _ChangeFormBase = DjangoUserChangeForm[User]
else:
    _CreationFormBase = BaseUserCreationForm
    _ChangeFormBase = DjangoUserChangeForm


class UserCreationForm(_CreationFormBase):
    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(_ChangeFormBase):
    class Meta:
        model = User
        fields = "__all__"
