from threading import Thread
from gui.WebInterface import WebInterface
from Sensor import Sensor
import csv, errno, signal, json, urllib2, sys
from socket import *
import random
from common import *
from Queue import Empty
import time

class WorkerThread(Thread):
    def __init__(self, guireceiver, job, *args, **kwargs):
        super(WorkerThread, self).__init__(*args, **kwargs)
        self.guireceiver = guireceiver
        self.job = job
        if job == 0:
            print_message('Listener thread created', 'ok')
        elif job == 1:
            print_message('Logger thread created', 'ok')
        elif job == 2:
            print_message('WebInterface thread created', 'ok')
        elif job == 3:
            print_message('Offline thread created', 'ok')

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
        gui = WebInterface()
        gui.run(self.guireceiver)
        print "\nGUI is shutting Down"

    def get_udp_message(self):
        while self.guireceiver.keepAlive:
            self.guireceiver.get_udp_message()
        print_message("Listener Thread Has finished",'ok')

    def random_values(self, sensorsList):
        values = {}
        for sensor in sensorsList.itervalues():
            current_value = eval(sensor.low_val) + eval(sensor.value)
            if sensor.name != 'rpm':
                new_value = current_value + random.randint(-7,7)
            else:
                new_value = current_value + random.randint(-700,700)
            if new_value == eval(sensor.high_val):
                new_value = str(int(eval(sensor.high_val)*0.9))
            elif new_value == eval(sensor.low_val):
                new_value = str(int(eval(sensor.high_val)*0.1)+ eval(sensor.low_val))
            limited_value = max( min(eval(sensor.high_val),new_value),eval(sensor.low_val))
            value = str(limited_value)
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
            time.sleep(0.0492)
    
    def run_logger(self):
        try:
            with open(self.guireceiver.logger.log_file, 'ab') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.guireceiver.logger.sensor_names)
                while self.guireceiver.keepAlive or self.guireceiver.message_queue.qsize() > 0:
                    try:
                        values = self.guireceiver.message_queue.get(timeout = 1)
                        string_values = ["%s=%s" %(key,value) for key,value in values.iteritems()]
                        json_string = "&".join(string_values)
                        req = urllib2.Request('http://localhost:8000/?%s' %json_string)
                        try:
                            urllib2.urlopen(req)
                        except Exception:
                            print_message('Failed to send values to browser', 'fail')
                        writer.writerow(values)
                    except EOFError, e:
                        print_message('Logger - getting from empty queue', 'fail')
                    except Empty, e:
                        print_message('Logger - queue timed out', 'fail')

            print_message("Logger Thread Has finished",'ok')
        except IOError, e:
            if e.errno != errno.EINTR:
                print_message('Logger Failed! errno = ' %e.errno, 'fail')
                raise
