from django.db import models
from django.utils import timezone


class Probe_request(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    ssid = models.ForeignKey('SSID', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "SSID: {}, MAC: {} at {}".format(self.ssid.ssid, self.client.mac, self.timestamp)

    class Meta:
        ordering = ['-timestamp']

class SSID(models.Model):
    ssid = models.CharField(max_length=64, unique=True)
    last_wiggled = models.DateTimeField(null=True, blank=True, default=None)
    probed_clients = models.ManyToManyField('Client', through=Probe_request)

    def __str__(self):
        return self.ssid

    def clients(self):
        return self.probed_clients.distinct()

class Network(models.Model):
    ssid = models.ForeignKey(SSID, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)

class Tag(models.Model):
    tag = models.CharField(max_length=64, default='Unnamed tag', unique=True)
    relevant_ssids = models.ManyToManyField(SSID)

    def apply_tag_to_clients(self):
        clients = Client.objects.all()
        for client in clients:
            for ssid in client.ssids():
                if ssid in self.relevant_ssids.all():
                    client.tags.add(self)
                    print("Added tag {} to {}".format(self.tag, client))
                    break

    def __str__(self):
        return self.tag

class Client(models.Model):
    mac = models.CharField(max_length=64, unique=True)
    probed_ssids = models.ManyToManyField(SSID, through=Probe_request)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.mac

    def get_probes(self):
        return Probe_request.objects.filter(client=self)

    def ssids(self):
        return self.probed_ssids.distinct()
