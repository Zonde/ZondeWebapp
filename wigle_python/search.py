import requests
from . import common
from .exception import WigleError
from json import JSONDecodeError
from requests.auth import HTTPBasicAuth
import os
import http.client as http_client
import logging

SEARCH_URL = common.BASE_URL + '/network/search'

# Required properties for a network
PROPERTIES = ['trilat', 'trilong', 'ssid', 'netid', 'lastupdt']

class Network():
    """Represents a network from the WiGLE database
    """
    def __init__(self, trilat, trilong, ssid, netid, lastupdt):
        self.ssid = ssid
        self.bssid = netid
        self.lastupdt = lastupdt
        self.lat = trilat
        self.long = trilong

    def __str__(self):
        return "Network {} ({})".format(self.ssid, self.netid)

def ssid(token, ssid):
    if token is None:
        raise WigleError("Token was 'None'")
    params = { 'ssid': ssid }
    headers = { 'Authorization': 'Basic ' + token }
    networks = []
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    while True:
        res = requests.get(SEARCH_URL, params=params, headers=headers)
        try:
            json = res.json()
        except JSONDecodeError:
            raise WigleError("Failed to parse JSON, raw content: '{}'".format(res.text))
        # TODO also fetch and parse the other networks based on searchAfter property
        def prot_missing(item, prop):
            return "Protocol mismatch, {} did not have property '{}'".format(item, prop)
        if 'success' not in json:
            raise WigleError(prot_missing('response', 'success'))
        if not json['success']:
            if 'message' not in json:
                raise WigleError(prot_missing('response', 'message'))
            raise WigleError(json['message'])
        if 'totalResults' not in json:
            raise WigleError(prot_missing('response', 'totalResults'))
        if json['totalResults'] >= 1000
            raise WigleError("Too many results for ssid {} ({})".format(ssid, json['totalResults']))
        if 'results' not in json:
            raise WigleError(prot_missing('response', 'results'))
        if len(json['results']) == 0:
            break
        for result in json['results']:
            for prop in PROPERTIES:
                if prop not in result:
                    raise WigleError(prot_missing('result', prop))
            args = map(lambda p: result[p], PROPERTIES)
            networks.append(Network(*args))
        if 'search_after' in json:
            params['searchAfter'] = json['search_after']
        else:
            break
    return networks
