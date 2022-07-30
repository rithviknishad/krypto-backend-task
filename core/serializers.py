from rest_framework import serializers

from .models import Alert


class AlertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alert
        fields = (
            "url",
            "deleted",
            "created_on",
            "updated_on",
            "triggered_on",
            "coin_id",
            "trigger_value",
            "user",
        )
        read_only_fields = (
            "user",
            "created_on",
            "deleted",
            "triggered_on",
            "trigger_on_lte",
            "updated_on",
        )
