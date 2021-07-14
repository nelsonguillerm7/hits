"""Model hits"""
# Django core
from django.db import models
from django_fsm import FSMIntegerField, transition


class Hit(models.Model):
    """Class define model the hits"""

    class StatusChoices(models.IntegerChoices):
        """Class define choices"""

        ACTIVE = 1, "Open"
        ASSIGNED = 2, "Assigned"
        COMPLETED = 3, "Completed"
        FAILED = 4, "Failed"

    assignee = models.ForeignKey(
        "authentication.User",
        on_delete=models.PROTECT,
        verbose_name="hitman",
        related_name="hitman",
    )
    description = models.TextField(
        verbose_name="description",
    )
    target = models.CharField(
        max_length=256,
        verbose_name="target",
    )
    state = FSMIntegerField(
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        protected=True,
        verbose_name="Status",
    )
    creator = models.ForeignKey(
        "authentication.User",
        on_delete=models.PROTECT,
        verbose_name="creator",
        related_name="manager",
    )

    class Meta:
        """Class define information the model"""

        verbose_name = "Hit"
        verbose_name_plural = "Hits"
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.target}"

    @transition(
        field="state",
        source=StatusChoices.ACTIVE,
        target=StatusChoices.ACTIVE,
        custom=dict(verbose="OPEN", icon="far fa-hand-point-right"),
    )
    def active(self, **kwargs):
        """Method to correct procedure"""
        pass

    @transition(
        field="state",
        source=StatusChoices.ACTIVE,
        target=StatusChoices.ASSIGNED,
        custom=dict(verbose="ASSIGNED", icon="far fa-hand-point-right"),
    )
    def assigned(self, **kwargs):
        """Method to correct procedure"""
        pass

    @transition(
        field="state",
        source=StatusChoices.ASSIGNED,
        target=StatusChoices.COMPLETED,
        custom=dict(verbose="COMPLETED"),
    )
    def completed(self, **kwargs):
        """Method to correct procedure"""
        pass

    @transition(
        field="state",
        source=StatusChoices.ASSIGNED,
        target=StatusChoices.FAILED,
        custom=dict(verbose="FAILED"),
    )
    def failed(self, **kwargs):
        """Method to correct procedure"""
        pass
