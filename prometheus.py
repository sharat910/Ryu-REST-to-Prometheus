from prometheus_client import Gauge
from pprint import pprint
class PrometheusClient(object):
    """docstring for PrometheusClient."""
    def __init__(self, prom_conf, root_key, labels, values):
        super(PrometheusClient, self).__init__()
        self.config = prom_conf
        self.root_key = root_key
        self.delim = self.config['join_delim']
        self.values = values
        self.labels = labels
        self.metrics = {} #key -> Gauge
        self.init_metrics()

    def init_metrics(self):
        for value in self.values:
            key = self.create_key(value)
            self.metrics[key] = Gauge(key,value,self.labels)

    def create_key(self,string):
        return self.delim.join([self.root_key,string])

    def publish(self,data):
        # pprint(data)
        for item_dict in data:
            labels = {x: item_dict[x] for x in self.labels}
            for metric in item_dict:
                if metric in self.values:
                    key = self.create_key(metric)
                    self.metrics[key].labels(**labels).set(item_dict[metric])
