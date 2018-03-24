from rest_framework import serializers
from .models import *

class NetworkSerializer(serializers.ModelSerializer):
    ssid = serializers.SlugRelatedField(read_only=True, slug_field='ssid')

    class Meta:
        model = Network
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):

    ssids = serializers.SlugRelatedField(read_only=True, many=True, slug_field='ssid')

    class Meta:
        model = Client
        fields = ('mac', 'ssids')

class Probe_request_serializer(serializers.ModelSerializer):

    ssid = serializers.SlugRelatedField(read_only=True, slug_field='ssid')
    client = serializers.SlugRelatedField(read_only=True, slug_field='mac')

    class Meta:
        model = Probe_request
        fields = ('ssid', 'client', 'timestamp')

class ssid_serializer(serializers.ModelSerializer):

    clients = serializers.SlugRelatedField(read_only=True, many=True, slug_field='mac')

    class Meta:
        model = SSID
        fields = ('ssid', 'clients')
