from rest_framework.serializers import ModelSerializer

from simple_api.models import Vehicle


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
