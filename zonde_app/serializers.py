from rest_framework import serializers
from .models import *

class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'

class Probe_request_serializer(serializers.ModelSerializer):

    ssid = serializers.SlugRelatedField(read_only=True, slug_field='ssid')
    client = serializers.SlugRelatedField(read_only=True, slug_field='mac')

    class Meta:
        model = Probe_request
        fields = ('ssid', 'client', 'timestamp')
