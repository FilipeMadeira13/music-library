"""Custom user: e-mail is the login, there is no username."""

from typing import Any, ClassVar

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from library.choices import Service


class UserManager(BaseUserManager["User"]):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email: str | None) -> str:
        """Lower-case the whole address so login and uniqueness ignore case."""
        return (email or "").strip().lower()

    def get_by_natural_key(self, username: str | None) -> "User":
        return self.get(email=self.normalize_email(username))

    def _create_user(self, email: str, password: str | None, **extra_fields: Any) -> "User":  # noqa: ANN401 - mirrors Django's **extra_fields signature
        email = self.normalize_email(email)
        if not email:
            msg = "The e-mail address is required."
            raise ValueError(msg)
        try:
            validate_email(email)
        except ValidationError as exc:
            msg = f"Invalid e-mail address: {email!r}."
            raise ValueError(msg) from exc
        user = self.model(email=email, **extra_fields)
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
        constraints: ClassVar[list[models.BaseConstraint]] = [
            # Guards writes that skip save() (queryset.update, raw SQL).
            models.UniqueConstraint(
                Lower("email"),
                name="user_email_ci_unique",
                violation_error_message=_("Já existe um usuário com este e-mail."),
            ),
            # NULL is the only "not chosen" state; "" and unknown services are rejected.
            models.CheckConstraint(
                condition=models.Q(preferred_service__in=Service.values)
                | models.Q(preferred_service__isnull=True),
                name="user_preferred_service_valid",
            ),
        ]

    def __str__(self) -> str:
        return self.email

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401 - forwards Model.save's arguments unchanged
        self.email = type(self).objects.normalize_email(self.email)
        super().save(*args, **kwargs)
