from threading import Thread
import requests
import logging
import time

class Collector(Thread):
    """docstring for Collector."""
    def __init__(self,dpid, url, interval, prom_client, filter_dict=None):
        super(Collector, self).__init__()
        self.url = url.replace("<dpid>",str(dpid))
        self.dpid = dpid
        self.interval = interval
        self.prom_client = prom_client
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

            self.prom_client.publish(data)


            t_op = time.time() - t_start
            t_sleep = self.interval - t_op
            if t_sleep < 0:
                logging.error("Interval time not enough to complete operation.")
            else:
                time.sleep(t_sleep)

    def filter(self,data):
        key = self.filter_dict['key']
        values = list(map(str,self.filter_dict['values']))
        return filter(lambda item: item['key'] in values, data)
