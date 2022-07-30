from django.db import models
from utils.models import BaseModel


class Alert(BaseModel, models.Model):
    coin_id = models.CharField(
        max_length=255,
        blank=False,
    )
    trigger_value = models.DecimalField(
        max_digits=16,
        decimal_places=3,
        blank=False,
        null=False,
        help_text="When the coin value crosses the specified `trigger_value` in USD, the alert is triggered.",
    )
    trigger_on_lte = models.BooleanField(
        blank=False,
        null=False,
        help_text="Whether to trigger the alert when the price reaches or falls below the set value. Otherwise when the price reaches or rises above the set value.",
        editable=False,
    )
    triggered_on = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
    )
    user = models.ForeignKey(
        "users.User",
        related_name="alerts",
        null=False,
        on_delete=models.CASCADE,
    )

    @property
    def triggered(self) -> bool:
        return bool(self.triggered_on)
