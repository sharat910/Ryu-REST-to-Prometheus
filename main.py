from collector_new import Collector
from config_loader import get_config
from prometheus import PrometheusClient
from pprint import pprint
from prometheus_client import start_http_server
if __name__ == '__main__':
    c = get_config()
    root_url = "http://%s:%s/%s" % (c['hostname'],c['port'],c['base_url'])
    pprint(c)
    for data_type_name in c['data_type']:
        data_type = c['data_type'][data_type_name]
        if data_type_name == 'meter' or data_type_name == 'queue':
            continue
        for endpoint_name in data_type['endpoints']:
            endpoint = data_type['endpoints'][endpoint_name]

            url = root_url + endpoint['url']
            interval = endpoint['interval']

            prom_key = "%s:%s" % (data_type_name,endpoint_name)
            labels = endpoint['labels']
            values = endpoint['values']

            print(data_type_name,endpoint_name)
            pc = PrometheusClient(c['prometheus'],prom_key,labels,values)
            worker = Collector(c['dpid'],url,interval,pc)
            worker.start()
        start_http_server(8080)
