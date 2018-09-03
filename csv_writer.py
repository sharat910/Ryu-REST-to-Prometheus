import os
import csv
from datetime import datetime

class CSVWriter(object):
    """docstring for CSVWriter."""
    def __init__(self, config, filename, fields):
        self.config = config
        if self.config['enable']:
            self.initialize(filename,fields)
        
    def initialize(self, filename, fields):
        self.create_dirs()
        self.file = self.create_file(filename)
        self.writer = csv.DictWriter(self.file, fieldnames=['Timestamp'] + fields,extrasaction='ignore')
        self.writer.writeheader()
        self.file.flush()

    def writerows(self,data):
        if self.config['enable']:
            self.insert_timestamp(data)
            self.writer.writerows(data)
            self.file.flush()

    def create_file(self,filename):
        filedir = self.config['dir']
        timestamp = datetime.now()
        filehandle = open("%s%s-%s.csv" % (filedir,timestamp,filename),'w')
        return filehandle


    def create_dirs(self):
        path = self.config['dir']
        if not os.path.exists(path):
            os.makedirs(path)

    def insert_timestamp(self,data):
        ts = str(datetime.now())
        for item in data:
            item['Timestamp'] = ts