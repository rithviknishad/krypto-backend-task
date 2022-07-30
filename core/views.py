from rest_framework import viewsets
from rest_framework.decorators import action
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

    @action(detail=False, url_path="create", methods=["post"])
    def create_alert(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(detail=True, url_path="delete", methods=["get", "delete"])
    def delete_alert(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        prices = fetch_current_prices()
        serializer.save(
            user=self.request.user,
            trigger_on_lte=int(self.request.data["trigger_value"]) > prices[self.request.data["coin_id"]],
        )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
