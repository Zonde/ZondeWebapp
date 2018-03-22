from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('api/networks/', views.get_networks, name='get_networks'),
    path('api/post/', views.network_client_post, name='network_client_post'),
    path('api/<mac>/probes/', views.get_client_probes, name='get_client_probes'),
    path('api/<mac>/<ssid>/probes/', views.get_client_ssid_probes, name='get_client_ssid_probes'),
    path('api/<mac>/ssids/', views.get_client_ssids, name='get_client_ssids'),
    path('api/<ssid>/clients/', views.get_ssid_clients, name='get_ssid_clients'),

    #path('api-auth/', include('rest_framework.urls'))
]
