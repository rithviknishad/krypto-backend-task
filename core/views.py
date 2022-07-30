from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from utils.utils import fetch_current_prices

from . import permissions
from .models import Alert
from .serializers import AlertSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = (
        IsAuthenticated,
        permissions.Alert,
    )

    def perform_create(self, serializer):
        prices = fetch_current_prices()
        serializer.save(
            user=self.request.user,
            trigger_on_lte=self.request.data["trigger_value"] > prices[self.request.data["coin_id"]],
        )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
