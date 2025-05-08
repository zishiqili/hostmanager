from rest_framework import serializers
from .models import City, IDC, Host

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class IDCSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city', write_only=True)

    class Meta:
        model = IDC
        fields = ['id', 'name', 'address', 'phone', 'contact_person', 'contact_email', 'contact_phone', 'city', 'city_id', 'created_at']

class HostSerializer(serializers.ModelSerializer):
    idc = IDCSerializer(read_only=True)
    idc_id = serializers.PrimaryKeyRelatedField(queryset=IDC.objects.all(), source='idc', write_only=True)

    class Meta:
        model = Host
        fields = ['id', 'name', 'ip_address', 'os', 'idc', 'idc_id', 'created_at']