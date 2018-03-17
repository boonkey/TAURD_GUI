from socket import *
from Sensor import Sensor
from Logger import Logger
import csv, sys
from WorkerThread import WorkerThread
from multiprocessing import Process, Queue
from threading import Thread
import os, errno, signal


class GuiReceiver:
    def __init__(self):
        self.remote_ip = '192.168.1.10'
        self.remote_tcp_port = 7
        self.remote_udp_port = 5001
        self.tcp_message = "CLIENT_CONNECT"
        self.sensors = {}
        self.i=0
        self.keepAlive = True
        self.message_queue = Queue()
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.udp_socket.bind(('', 5001))
        if 'linux' in sys.platform:
            os.system("sudo ifconfig eth1 192.168.1.6")

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
        try:
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
            #print "inserted to q: ", self.message_queue.qsize()
            self.i+=1
            #print "\rPackets Recieved: %d" %self.i, 
        except IOError, e:
            if e.errno != errno.EINTR:
                raise


def signal_handler(signum, frame):
        print "\na signal number %d has been caught by handler" %signum
        g.keepAlive = False
        

if __name__ == "__main__":
    global g, logger_thread, listener_thread
    signal.signal(signal.SIGINT, signal_handler)
    g = GuiReceiver()
    if 'offline' in sys.argv:
        print "Starting in offline mode!"
        sensor_conf = "1:speed,0,120;2:rpm,0,8000;3:braking,0,100;4:throttle,0,100;5:wing_position,-100,100;6:s6,0,255;7:s7,0,255;8:s8,0,255;9:s9,0,255;10:s10,0,255;<FIN>"
        g.analyize_sensor_configuration(sensor_conf)
        g.logger = Logger(g.sensors)
        g.logger.log_init()
        g.print_message("Client Connected", 2)
        offline_thread = WorkerThread(g, 3)
        offline_thread.start()
        g.print_message("READY",1)
    else:
        print "Starting in Live mode"
        g.client_connect()
    logger_thread = WorkerThread(g, 1)
    listener_thread = WorkerThread(g, 0)
    webInterface_thread = WorkerThread(g, 2)
    listener_thread.start()
    logger_thread.start()
    webInterface_thread.start()
    while g.keepAlive:
        continue
    webInterface_thread.join()
    listener_thread.join()
    logger_thread.join()
    print "bye"
    