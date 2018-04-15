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
from django.shortcuts import get_object_or_404
from django_rq import job, enqueue
from zonde_app.wigle import ssid_added
from datetime import datetime

# Create your views here.
def index(request):
    activate('Europe/Amsterdam')
    probes = Probe_request.objects.all()[:250]
    return render(request, 'zonde_app/index.html', {'probes': probes})



@api_view(['GET'])
def get_networks(request):
    networks = Network.objects.all()[:250]
    network_serializer = NetworkSerializer(networks, many=True)
    return Response(network_serializer.data)

@api_view(['GET'])
def get_networks_name(request, ssid):
    ssid = get_object_or_404(SSID, ssid=ssid)
    networks = Network.objects.filter(ssid=ssid)
    network_serializer = NetworkSerializer(networks, many=True)
    return Response(network_serializer.data)

@api_view(['GET'])
def get_networks_mac(request, mac):
    mac = mac.replace('-', ':')
    client = get_object_or_404(Client, mac=mac)
    networks = Network.objects.filter(ssid__in=client.ssids())

    return Response(NetworkSerializer(networks, many=True).data)

@api_view(['GET'])
def tag_count(request, year_s, month_s, day_s, hour_s, min_s, year_e, month_e, day_e, hour_e, min_e):
    dt_s = datetime(year_s, month_s, day_s, hour_s, min_s)
    dt_e = datetime(year_e, month_e, day_e, hour_e, min_e)
    probes = Probe_request.objects.filter(timestamp__range=(dt_s, dt_e))
    clients = {p.client for p in probes}
    tag_data = ''
    ssid_data = ''
    ssids = {p.ssid for p in probes}

    for ssid in ssids:
        ssid_data += "{}    ".format(ssid)


    for tag in Tag.objects.all():
        count = len([x for x in clients if tag in x.tags.all()])
        tag_data += "{}: {}, ".format(tag, count)

    return Response(statsSerializer(Stats(len(clients), tag_data, ssid_data)).data)


@api_view(['GET'])
def get_client_probes(request, mac):
    mac = mac.replace('-', ':')
    client = get_object_or_404(Client, mac=mac)
    probes = client.get_probes()
    probe_serializer = Probe_request_serializer(probes, many=True)
    return Response(probe_serializer.data)

@api_view(['GET'])
def get_client_ssid_probes(request, mac, ssid):
    mac = mac.replace('-', ':')
    client = get_object_or_404(Client, mac=mac)
    ssid = get_object_or_404(SSID, ssid=ssid)
    probes = Probe_request.objects.filter(client=client, ssid=ssid)
    probe_serializer = Probe_request_serializer(probes, many=True)
    return Response(probe_serializer.data)

@api_view(['GET'])
def get_client_ssids(request, mac):
    mac = mac.replace('-', ':')
    client = get_object_or_404(Client, mac=mac)
    ssids = client.ssids()
    s = ssid_serializer(ssids, many=True)
    return Response(s.data)

@api_view(['GET'])
def get_ssid_clients(request, ssid):
    ssid = get_object_or_404(SSID, ssid=ssid)
    clients = ssid.clients()
    s = ClientSerializer(clients, many=True)
    return Response(s.data)

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
        ssid_added.delay(ssid)

    Probe_request.objects.create(ssid=ssid, client=client)

    return Response(status=status.HTTP_200_OK)

class Stats:

    def __init__(self, count, data, ssid_data):
        self.total_count = count
        self.tag_data = data
        self.ssid_data = ssid_data
