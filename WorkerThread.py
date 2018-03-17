from threading import Thread
from gui import WebInterface
from Sensor import Sensor
import csv, errno, signal, json, urllib2
from socket import *
import random

class WorkerThread(Thread):
    def __init__(self, guireceiver, job, *args, **kwargs):
        super(WorkerThread, self).__init__(*args, **kwargs)
        self.guireceiver = guireceiver
        self.job = job
        print self.job

    def run(self):
        if self.job == 0:
            self.get_udp_message()
        elif self.job == 1:
            self.run_logger()
        elif self.job == 2:
            self.run_gui()
        elif self.job == 3:
            self.run_fake_messages()

    def run_gui(self):
        WebInterface.run(self.guireceiver)
        #while self.guireceiver.keepAlive:
        #    continue
        print "\nGUI is shutting Down"

    def get_udp_message(self):
        while self.guireceiver.keepAlive:
            self.guireceiver.get_udp_message()
        print "\nListener Thread Has finished"    

    def random_values(self, sensorsList):
        values = {}
        for sensor in sensorsList.itervalues():
            value = str(random.randint(eval(sensor.low_val), eval(sensor.high_val)))
            sensor.update(value)
            values[sensor.id] = value
        return values

    def run_fake_messages(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        while self.guireceiver.keepAlive:
            values = self.random_values(self.guireceiver.sensors)
            string_values = ["%s:%s;" %(key,value) for key,value in values.iteritems()]
            data = "".join(string_values)
            s.sendto(data, ('255.255.255.255',5001))
    
    def run_logger(self):
        try:
            with open(self.guireceiver.logger.log_file, 'ab') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.guireceiver.logger.sensor_names)
                while self.guireceiver.keepAlive or self.guireceiver.message_queue.qsize() > 0:
                    values = self.guireceiver.message_queue.get()
#                    print "values : ", values
                    string_values = ["%s=%s" %(key,value) for key,value in values.iteritems()]
                    json_string = "&".join(string_values)
                    req = urllib2.Request('http://localhost:8000/?%s' %json_string)
                    try:
                        urllib2.urlopen(req)
                    except Exception:
                        print "basa"
                    writer.writerow(values)
            print "Logger Thread Has finished"    
        except IOError, e:
            if e.errno != errno.EINTR:
                raise
