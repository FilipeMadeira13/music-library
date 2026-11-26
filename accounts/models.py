"""Custom user: e-mail is the login, there is no username."""

from typing import Any, ClassVar

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from library.choices import Service


class UserManager(BaseUserManager["User"]):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields: Any) -> "User":  # noqa: ANN401 - mirrors Django's **extra_fields signature
        if not email:
            msg = "The e-mail address is required."
            raise ValueError(msg)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,  # noqa: ANN401 - mirrors Django's **extra_fields signature
    ) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,  # noqa: ANN401 - mirrors Django's **extra_fields signature
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields["is_staff"] is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields["is_superuser"] is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # type: ignore[assignment]  # e-mail replaces the username field
    email = models.EmailField(_("e-mail"), unique=True)
    preferred_service = models.CharField(  # noqa: DJ001 - NULL means "not chosen yet", as in plano.md §2
        _("serviço preferido"),
        max_length=20,
        choices=Service.choices,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects: ClassVar[UserManager] = UserManager()  # type: ignore[assignment]  # email-based manager replaces Django's

    class Meta:
        verbose_name = _("usuário")
        verbose_name_plural = _("usuários")

    def __str__(self) -> str:
        return self.email
