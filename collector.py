import requests
import threading
import time
from prometheus_client import Gauge

from ..config_loader import get_config

class StatCollector(object):
    """docstring for StatCollector."""
    def __init__(self, app_config):
        super(StatCollector, self).__init__()
        self.app_config = app_config
        self.config = get_config("stats_collector")
        self.base_url = self.get_base_url()
        self.endpoints = []
        self.prom = {} #data_type -> key -> Gauge

    def init_prometheus(self,endpoints):
        for endpoint_type in self.endpoints:
            delim = self.config['prometheus']['join_delim']
            root_key = delim.join([
                            self.meter_config['prefix'],endpoint_type])
            labels,values = self.get_labels_and_values(endpoint_type)
            for value in values:
                key = delim.join([root_key,value])
                self.prom[key] = Gauge(key,value,labels)

    def get_base_url(self):
        url = "http://%s:%s" % (self.app_config['hostname'],
                                self.app_config['port'])
        return url + self.config['base_url']

    def fetch_from_endpoints(self):
        for endpoint in self.endpoints:
            endpoint_type = endpoint[endpoint.keys()[0]]
            endpoint_info = endpoint[endpoint_type]
            url = self.base_url + endpoint_info['url']
            self.spawn_fetcher(endpoint_type, url,endpoint_info['interval'])

    def spawn_fetcher(self,endpoint_type,url,interval):
        t = threading.Thread(target=self.fetch, args = (endpoint_type,url,interval))
        t.daemon = True
        t.start()

    def fetch(self,endpoint_type,url,interval):
        while True:
            t_start = time.time()
            r = requests.get(url)
            self.parse_and_publish(endpoint_type,r.body)
            t_exec = time.time() - t_start
            time.sleep(interval - t_exec)


    def parse_and_publish(self,request_body):
        pass

    def collect(self):
        for data_type in self.config['data_types']:
            self.init_prometheus()
