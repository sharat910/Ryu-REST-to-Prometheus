from collector import StatCollector

class MeterStatCollecter(StatCollector):
    """docstring for MeterStatCollecter."""
    def __init__(self, app_config):
        super(MeterStatCollecter, self).__init__(app_config)
        self.meter_config = self.config['data_type']['meter']

    def load_endpoints(self):
        self.endpoints = self.meter_config['endpoints']

    def parse_and_publish(self,endpoint_type,request_body):
        data = eval(request_body)
        data = filter(lamda x: x['meter_id'] in self.meter_config['filter'], data)

        if endpoint_type == 'counters':
            self.handle_meter_counters(data,prom)
        elif endpoint_type == 'config':
            self.handle_meter_config(data,prom)

    def handle_meter_counters(self,data,prom):
        for m in meter_counters:
