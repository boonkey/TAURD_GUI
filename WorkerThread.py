from threading import Thread
from gui.WebInterface import WebInterface
import csv, urllib2
from socket import *
import random
from common import *
from Queue import Empty
import time

class WorkerThread(Thread):
    def __init__(self, guireceiver, job, verbose=False, *args, **kwargs):
        super(WorkerThread, self).__init__(*args, **kwargs)
        self.guireceiver = guireceiver
        self.job = job
        self.verbose = verbose
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
        gui = WebInterface(self.verbose)
        gui.run(self.guireceiver)
        print_message("GUI is shutting Down", 'info')

    def get_udp_message(self):
        while self.guireceiver.keepAlive:
            self.guireceiver.get_udp_message()
        print_message("Listener Thread Has finished", 'ok')

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
        print_message('Offline - Starting to send fake UDP packets', 'info')
        if self.verbose:
            print_message('Offline in verbose mode', 'verb')
        while self.guireceiver.keepAlive:
            values = self.random_values(self.guireceiver.sensors)
            string_values = ["%s:%s;" %(key,value) for key,value in values.iteritems()]
            # string_values = ['1:102;2:6592;3:0;4:100;5:0;6:12;7:97;8:88;9:8;10:191'] # for screenshot purposes
            data = "".join(string_values)
            s.sendto(data, ('255.255.255.255',5001))
            time.sleep(0.0492)
            if self.verbose:
                print_message('Fake message sent', 'verb')
    
    def run_logger(self):
        if self.verbose:
            print_message('Logger starting in verbose mode','verb')
        try:
            end = time.time()
            with open(self.guireceiver.logger.log_file, 'ab') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.guireceiver.logger.sensor_names)
                while self.guireceiver.keepAlive or self.guireceiver.message_queue.qsize() > 0:
                    try:
                        if self.verbose:
                            start = time.time()
                            print_message('Logger reset round time: %f' %(start - end), 'verb')
                        values = self.guireceiver.message_queue.get(timeout=0.5)
                        if self.verbose:
                            print_message('Logger - message arrived in queue. Queue size: %d' %self.guireceiver.message_queue.qsize(), 'verb')
                        string_values = ["%s=%s" %(key,value) for key,value in values.iteritems()]
                        json_string = "&".join(string_values)
                        req = urllib2.Request('http://localhost:8000/?%s' %json_string)
                        if self.verbose:
                            end = time.time()
                            print_message('Logger - message handling complete', 'verb')
                            print_message('Logger round time: %f' % (end - start), 'verb')
                        try:
                            urllib2.urlopen(req)
                        except Exception:
                            print_message('Failed to send values to browser', 'fail')
                        writer.writerow(values)
                    except EOFError:
                        print_message('Logger - getting from empty queue', 'fail')
                    except Empty:
                        print_message('Logger - queue timed out', 'fail')

            print_message("Logger Thread Has finished",'ok')
        except IOError, e:
            if e.errno != errno.EINTR:
                print_message('Logger Failed! errno = ' %e.errno, 'fail')
                raise
