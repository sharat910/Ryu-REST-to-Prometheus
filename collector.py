from threading import Thread
import requests
import logging
import time
from pprint import pprint

class Collector(Thread):
    """docstring for Collector."""
    def __init__(self, dpid, url, interval, prom_client,csv_writer,filter_dict=None):
        super(Collector, self).__init__()
        self.url = url.replace("<dpid>",str(dpid))
        self.dpid = dpid
        self.interval = interval
        self.prom_client = prom_client
        self.csv_writer = csv_writer
        self.filter_dict = filter_dict

    def run(self):
        while True:
            t_start = time.time()

            #Get data and pase
            r = requests.get(self.url)
            data = []
            try:
                data = r.json()[str(self.dpid)]
            except Exception as e:
                logging.error("Eval error")
                logging.error(e)

            if self.filter_dict:
                data = self.filter(data)

            data = self.transform(data)
            
            pprint(data)
            #Actions
            self.prom_client.publish(data)
            self.csv_writer.writerows(data)


            t_op = time.time() - t_start

            print(self.prom_client.root_key,"Time taken:",t_op)

            t_sleep = self.interval - t_op
            if t_sleep < 0:
                logging.error("Interval time not enough to complete operation.")
                continue
            else:
                time.sleep(t_sleep)

    def filter(self,data):
        key = self.filter_dict['key']
        values = self.filter_dict['values']
        filtered = list(filter(lambda item: item[key] in values, data))
        return filtered

    def transform(self,data):
        return data

class QueueConfigCollector(Collector):

    def transform(self,data):
        new_data = []
        for item in data:
            new_item = {}
            new_item['queue_id'] = item['queue_id']
            new_item['port_no'] = item['port']
            new_item['min_rate'] = [prop['rate'] for prop in item['properties'] \
                                    if prop['property'] == 'MIN_RATE'][0]
            new_item['max_rate'] = [prop['rate'] for prop in item['properties'] \
                                    if prop['property'] == 'MAX_RATE'][0]
            new_data.append(new_item)
        return new_data

    def filter(self,data):
        key = self.filter_dict['key']
        values = self.filter_dict['values']
        filtered = list(filter(lambda item: item[key] in values, data[0]['queues']))
        return filtered

