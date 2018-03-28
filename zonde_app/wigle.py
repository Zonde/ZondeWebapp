from django_rq import job, enqueue
from zonde_app.models import *
from wigle_python import search
import os

TOKEN = os.environ.get('WIGLE_TOKEN')
if TOKEN is None:
    raise Exception("WIGLE_TOKEN not defined")
else:
    print("Wigle token: {}".format(TOKEN))


@job
def ssid_added(ssid):
    print("Looking for ssid: {}".format(ssid))
    networks = search.ssid(TOKEN, ssid)
    for n in networks:
        Network.objects.create(ssid=ssid, latitude=n.lat, longitude=n.long, bssid=n.bssid)
    print("Added {} networks for ssid {}".format(len(networks), ssid))
