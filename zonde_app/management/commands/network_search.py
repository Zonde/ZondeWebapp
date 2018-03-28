from django.core.management.base import BaseCommand, CommandError
from zonde_app.models import *
from django_rq import job, enqueue
from zonde_app.wigle import ssid_added

class Command(BaseCommand):
    def handle(self, *args, **options):
        for ssid in SSID.objects.all():
            if Network.objects.filter(ssid=ssid).exists():
                print("{} already has a network.".format(ssid))
                continue
            ssid_added.delay(ssid)
