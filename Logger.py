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

    def worker(self):
        while True:
            print "new work. size of queue: ", self.message_queue.qsize()
            self.log_line(self.message_queue.get())

    def random_values(self, sensorsList):
        values = {}
        for sensor in sensorsList.itervalues():
            value = str(random.randint(sensor.low_val, sensor.high_val))
            sensor.update(value)
            values[sensor.name] = value
        return values

if __name__ == "__main__":
    print 'pizza'
    s1 = Sensor('1', 'dan', 0, 10)
    s2 = Sensor('2', 'dan_s', -5, 12)
    s3 = Sensor('3', 'dan_sh', 0, 6000)
    sensors_list = {'1': s1, '2': s2, '3': s3}
    logger = Logger(sensors_list)
    print logger.log_file
    logger.log_init()
    for i in range(0, 10):
        logger.log_line(logger.random_values(sensors_list))
