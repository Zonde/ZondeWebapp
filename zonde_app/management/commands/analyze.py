from django.core.management.base import BaseCommand, CommandError
from zonde_app.models import *
from django.db.models import Count

class Command(BaseCommand):
    help = 'Analyzes the probe requests in the database'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        unique_nets = Network.objects           \
            .values('ssid_id')                  \
            .annotate(count=Count('ssid_id'))   \
            .filter(count=1)
        for n in unique_nets:
            ssid = SSID.objects.get(id=n['ssid_id'])
            self.stdout.write("{}:".format(ssid.ssid))
            clients = Client.objects.filter(probe_request__ssid=ssid.id).distinct()
            for c in clients:
                self.stdout.write(c.mac)
            self.stdout.write('')

            

