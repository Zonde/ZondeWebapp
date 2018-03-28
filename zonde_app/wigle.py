from django_rq import job, enqueue
from zonde_app.models import *
from wigle_python import search
from wigle_python.exception import WigleError
from django.db import IntegrityError
import os

@job
def ssid_added(ssid):
    TOKEN = os.environ.get('WIGLE_TOKEN')
    if TOKEN is None:
        raise Exception("WIGLE_TOKEN not defined")
    print("Looking for ssid: {}".format(ssid))
    try:
        networks = search.ssid(TOKEN, ssid)
        for n in networks:
            try:
                Network.objects.create(ssid=ssid, latitude=n.lat, longitude=n.long, bssid=n.bssid)
            except IntegrityError:
                # Already exists
                pass
        print("Added {} networks for ssid {}".format(len(networks), ssid))
    except WigleError as e:
        print("Error occurred: {}".format(e))
        
