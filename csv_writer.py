import os
import csv
from datetime import datetime

class CSVWriter(object):
    """docstring for CSVWriter."""
    def __init__(self, config, filename, fields):
        self.create_dirs(config['dir'])
        self.file = open(config['dir']+filename + '.csv','w')
        self.writer = csv.DictWriter(self.file, fieldnames=['Timestamp'] + fields,extrasaction='ignore')
        self.writer.writeheader()
        self.file.flush()

    def writerows(self,data):
        self.insert_timestamp(data)
        self.writer.writerows(data)
        self.file.flush()

    def create_dirs(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def insert_timestamp(self,data):
        ts = str(datetime.now())
        for item in data:
            item['Timestamp'] = ts