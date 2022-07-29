from django.db import models


class Alert(models.Model):
    coin_id = models.CharField(
        max_length=255,
        blank=False,
    )
    created_on = models.DateTimeField(
        blank=False,
        null=False,
        auto_now_add=True,
        editable=False,
    )
    deleted = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        editable=False,
        help_text="Whether the record is deleted or not (soft-delete)",
    )
    trigger_value = models.DecimalField(
        max_digits=16,
        decimal_places=3,
        blank=False,
        null=False,
        help_text="When the coin value crosses the specified `trigger_value` the alert is triggered.",
    )
    triggered_on = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
    )
    updated_on = models.DateTimeField(
        blank=False,
        null=False,
        auto_now=True,
        editable=False,
    )
    user = models.ForeignKey(
        "users.User",
        related_name="alerts",
        null=False,
        on_delete=models.CASCADE,
    )
