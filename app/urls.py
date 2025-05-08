from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import CityViewSet, IDCViewSet, HostViewSet

# urlpatterns = [
#     path('cities/', views.CityViewSet.as_view(), name='city-list'),
#     path('idcs/', views.IDCViewSet.as_view(), name='idc-list'),
#     path('hosts/', views.HostViewSet.as_view(), name='host-list'),
# ]

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'idcs', IDCViewSet, basename='idcs')
router.register(r'hosts', HostViewSet, basename='hosts')
# router.register(r'hosts/ping/', HostViewSet, basename='hosts-ping')

urlpatterns = [
    path('', include(router.urls)),
]