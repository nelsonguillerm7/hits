"""User model."""
# Django core
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_fsm import FSMIntegerField, transition
from .service import CheckRol


class User(AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    class StatusChoices(models.IntegerChoices):
        """Class define choices"""

        ACTIVE = 1, "ACTIVE"
        INACTIVE = 2, "INACTIVE"

    email = models.EmailField(
        unique=True,
        error_messages={"unique": "A user with this email already exists"},
    )
    state = FSMIntegerField(
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        protected=True,
        verbose_name="Status",
    )
    managers = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Jefe",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        """Class define meta information"""

        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """Return username."""
        return self.username

    @property
    def rol(self):
        return CheckRol.rol(self)

    @transition(
        field="state",
        source=StatusChoices.ACTIVE,
        target=StatusChoices.ACTIVE,
        custom=dict(verbose="ACTIVE"),
    )
    def active(self, **kwargs):
        """Method to correct procedure"""
        pass

    @transition(
        field="state",
        source=StatusChoices.ACTIVE,
        target=StatusChoices.INACTIVE,
        custom=dict(verbose="INACTIVE"),
    )
    def inactive(self, **kwargs):
        """Method to correct procedure"""
        self.is_active = False
