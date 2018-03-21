from django.db import models
from django.utils import timezone


class SSID(models.Model):
    ssid = models.CharField(max_length=64, unique=True)
    last_wiggled = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.ssid

    def get_clients(self):
        return [client for client in Client.objects.all() if self in client.get_ssids()]

class Network(models.Model):
    ssid = models.ForeignKey(SSID, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)


class Client(models.Model):
    mac = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.mac

    def get_probes(self):
        return Probe_request.objects.filter(client=self)

    def get_ssids(self):
        return set([probe.ssid for probe in self.get_probes()])


class Probe_request(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ssid = models.ForeignKey(SSID, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "SSID: {}, MAC: {} at {}".format(self.ssid.ssid, self.client.mac, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
