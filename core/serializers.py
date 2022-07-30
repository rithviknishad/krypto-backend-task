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
            "status",
        )
        read_only_fields = (
            "created_on",
            "deleted",
            "triggered_on",
            "trigger_on_lte",
            "updated_on",
            "status",
        )
