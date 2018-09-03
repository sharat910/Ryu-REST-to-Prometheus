from pprint import pprint
from prometheus_client import start_http_server

from collector import Collector, QueueConfigCollector
from config_loader import get_config
from prometheus import PrometheusClient
from csv_writer import CSVWriter

def spawn_collectors(c):
    root_url = "http://%s:%s/%s" % (c['hostname'],c['port'],c['base_url'])
    pprint(c)
    for data_type_name in c['data_type']:
        data_type = c['data_type'][data_type_name]
        
        if data_type['enable'] == False:
            continue
        
        filter_dict = data_type.get('filter',None)

        for endpoint_name in data_type['endpoints']:
            endpoint = data_type['endpoints'][endpoint_name]

            url = root_url + endpoint['url']
            interval = endpoint['interval']

            prom_key = "%s:%s" % (data_type_name,endpoint_name)
            labels = endpoint['labels']
            values = endpoint['values']
            print(data_type_name,endpoint_name)
            pc = PrometheusClient(c['prometheus'],prom_key,labels,values)
            csv = CSVWriter(c['csvwriter'],prom_key,labels+values)

            if data_type_name == 'queue' and endpoint_name == 'config':
                worker = QueueConfigCollector(c['dpid'],url,interval,pc,csv,filter_dict)
                worker.start()
                continue

            worker = Collector(c['dpid'],url,interval,pc,csv,filter_dict)
            worker.start()

if __name__ == '__main__':
    c = get_config()
    spawn_collectors(c)
    start_http_server(c['prometheus']['port'])
