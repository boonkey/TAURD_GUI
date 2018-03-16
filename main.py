from socket import *
import signal
from Sensor import Sensor
from Logger import Logger
import csv, sys
from threading import Thread
from multiprocessing import Process, Queue


class GuiReceiver:
    def __init__(self):
        self.remote_ip = '192.168.1.10'
        self.remote_tcp_port = 7
        self.remote_udp_port = 5001
        self.tcp_message = "CLIENT_CONNECT"
        self.sensors = {}
        self.i=0
        self.message_queue = Queue()
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.udp_socket.bind(('', 5001))

    def print_color_header(self, color):
        if color == 0:
            return '\033[0m'
        elif color == 1: #GREEN
            return '\033[32m'
        elif color == 2: #YELLOW
            return '\033[33m'
        elif color == 3: #RED
            return '\033[31m'
        elif color == 4: #BLUE
            return '\033[34m'
        elif color == 5: #Purple
            return '\033[35m'
    
    def print_message(self, msg, color=0):
        print_msg = self.print_color_header(color) + msg + self.print_color_header(0)
        print print_msg
    
    def client_connect(self):
        self.print_message("starting connection", 1)
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self.remote_ip, self.remote_tcp_port))
        sock.send(self.tcp_message)
        data = sock.recv(1024)
        sock.close()
        self.analyize_sensor_configuration(data)
        self.logger = Logger(self.sensors)
        self.logger.log_init()
        #self.print_sensors_list()
        sensor_names = [sensor[1].name for sensor in self.sensors.iteritems()]
        self.worker_thread = Process(target=worker, args=(self.logger.log_file, self.message_queue, sensor_names))
        self.worker_thread.start()
        self.print_message("Client Connected", 2)

    def analyize_sensor_configuration(self, raw_data):
        sensors = raw_data.split(";")
        for sensor in sensors:
            #print sensor
            if sensor == "<FIN>":
                break
            id, data = sensor.split(":")
            if id != "0":
                name, low_val, high_val = data.split(",")
                self.sensors[id] = Sensor(id, name, low_val, high_val)
                print "id: %s ; name: %s, low: %s, high: %s" %(id,name,low_val,high_val)

    def print_sensors_list(self):
        for s_id, sensor in self.sensors.iteritems():
            print "Sensor number %s:\n%s" %(s_id, sensor)

    def get_udp_message(self):
        msg = self.udp_socket.recvfrom(1024)[0]
        values_dict = {}
        sensors_data = msg.split(";")
        for data in sensors_data:
            if len(data) != 0:
                s_id, value = data.split(":")
                if self.sensors.has_key(s_id):
                    self.sensors[s_id].update(value)
                    values_dict[self.sensors[s_id].name] = value
        self.message_queue.put(values_dict)
        self.i+=1
        print "\rPackets Recieved: %d" %self.i, 

    def __del__(self):
        print "cleanup"
        self.worker_thread.join()

def worker(log_file, q, sensor_names):
    print log_file
    with open(log_file, 'ab') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=sensor_names)
        while True:
            values = q.get()
            writer.writerow(values)


def signal_handler(signum, frame):
    print "a signal number %d has been caught by handler" %signum
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    g = GuiReceiver()
    g.client_connect()
    print "================================================="
    while True:
        g.get_udp_message()
