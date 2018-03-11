from django.db import models
from django.utils import timezone


class SSID(models.Model):
    ssid = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.ssid

class Network(models.Model):
    ssid = models.ForeignKey(SSID, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)


class Client(models.Model):
    mac = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.mac

class Probe_request(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ssid = models.ForeignKey(SSID, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "SSID: {}, MAC: {} at {}".format(self.ssid.ssid, self.client.mac, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
