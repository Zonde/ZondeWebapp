from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('api/networks/', views.get_networks, name='get_networks'),
    path('api/post/', views.network_client_post, name='network_client_post'),

    path('api-auth/', include('rest_framework.urls'))
]
