import csv
from time import gmtime, strftime
import os
from Sensor import Sensor
import random

class Logger:
    def __init__(self, sensors, log_file = 'TAURD_log'):
        self.log_file = log_file + strftime("-%Y-%m-%d_%H-%M-%S", gmtime()) + ".csv"
        self.sensor_names = [sensor[1].name for sensor in sensors.iteritems()]
        print "log: " , os.getcwd()

    def log_init(self):
        with open(self.log_file, 'wb') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = self.sensor_names)
            writer.writeheader()

    def log_line(self, values):
        print "values: ", values
        with open(self.log_file, 'ab') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.sensor_names)
            writer.writerow(values)