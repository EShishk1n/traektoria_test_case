from rest_framework.viewsets import ModelViewSet

from simple_api.models import Vehicle
from simple_api.serializers import VehicleSerializer


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

