import paramiko
from django.shortcuts import render

# Create your views here.
from ping3 import ping

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import City, IDC, Host
from .serializers import CitySerializer, IDCSerializer, HostSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class IDCViewSet(viewsets.ModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer

class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    @action(detail=False, methods=['get'], url_path='ping')
    def ping(self, request):
        '''
        提供一个 API，用于探测主机是否 ping 可达
        :param request:
        :return:
        '''
        host_ip = request.query_params.get('host', '127.0.0.1')
        delay = ping(host_ip, timeout=2)
        if delay is None:
            return Response({'host': host_ip, 'reachable': True})
        else:
            return Response({'host': host_ip, 'reachable': False})



