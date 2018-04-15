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
    path('api/<mac>/networks/', views.get_networks_mac, name='get_networks_mac'),
    path('api/name/<ssid>/networks/', views.get_networks_name, name='get_networks_name'),
    path('api/<int:year_s>/<int:month_s>/<int:day_s>/<int:hour_s>/<int:min_s>/<int:year_e>/<int:month_e>/<int:day_e>/<int:hour_e>/<int:min_e>/', views.tag_count, name='tag_count'),

    #path('api-auth/', include('rest_framework.urls'))
]
