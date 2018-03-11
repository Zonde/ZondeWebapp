from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import activate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from zonde_app.serializers import *
from rest_framework.parsers import JSONParser, FormParser
from zonde_app.models import *

# Create your views here.
def index(request):
    activate('Europe/Amsterdam')
    probes = Probe_request.objects.all()[:250]
    return render(request, 'zonde_app/index.html', {'probes': probes})



@api_view(['GET'])
def get_networks(request):
    networks = Network.objects.all()
    network_serializer = NetworkSerializer(networks, many=True)
    return Response(network_serializer.data)

@api_view(['GET'])
def get_client_ssids(request, mac):
    mac = mac.replace('-', ':')
    client = Client.objects.get(mac=mac)
    probes = Probe_request.objects.filter(client=client)
    probe_serializer = Probe_request_serializer(probes, many=True)
    return Response(probe_serializer.data)


@api_view(['POST'])
@parser_classes((FormParser, JSONParser))
def network_client_post(request):

    print(request.body)

    mac = request.data['mac'].lower()
    ssid = request.data['ssid']

    try:
        client = Client.objects.get(mac=mac)
    except Client.DoesNotExist:
        client = Client.objects.create(mac=mac)

    try:
        ssid = SSID.objects.get(ssid=ssid)
    except SSID.DoesNotExist:
        ssid = SSID.objects.create(ssid=ssid)

    Probe_request.objects.create(ssid=ssid, client=client)
    return Response(status=status.HTTP_200_OK)
