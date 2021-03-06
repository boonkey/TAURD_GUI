from socket import *  #
from Sensor import Sensor
from Logger import Logger
from WorkerThread import WorkerThread
from multiprocessing import Process, Queue
import os, errno, signal, csv, sys, json
from common import *


class GuiReceiver:
    def __init__(self, verbose=False):
        self.remote_ip = '192.168.1.10'
        self.remote_tcp_port = 7
        self.remote_udp_port = 5001
        self.tcp_message = "CLIENT_CONNECT"
        self.sensors = {}
        self.keepAlive = True
        self.verbose = verbose
        self.message_queue = Queue()
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.udp_socket.settimeout(0.2)
        self.ready = True
        try:
            self.udp_socket.bind(('', 5001))
        except error, e:
            if e[0] == 98:
                print_message('Client already running. Exiting', 'fail')
                self.ready = False
            else:
                raise
        # if 'linux' in sys.platform:
        #     os.system("sudo ifconfig eth1 192.168.1.6")

    def client_connect(self):
        print_message("starting connection", 'ok')
        sock = socket(AF_INET, SOCK_STREAM)
        try:
            sock.connect((self.remote_ip, self.remote_tcp_port))
            sock.send(self.tcp_message)
            data = sock.recv(1024)
            sock.close()
        except Exception:
            print_message('Failed to connect to client', 'fail')
            return False
        self.analyize_sensor_configuration(data)
        self.logger = Logger(self.sensors)
        self.logger.log_init()
        try:
            with open('tmp_info', 'wb') as info_file:
                info_file.writelines(json.dumps(g.sensors, default=lambda x: x.__dict__))
        except IOError, e:
            print_message('Failed to send metadata', 'fail')
        print_message("Client Connected", 'ok')
        return True

    def analyize_sensor_configuration(self, raw_data):
        sensors = raw_data.split(";")
        for sensor in sensors:
            # print sensor
            if sensor == "<FIN>":
                break
            id, data = sensor.split(":")
            if id != "0":
                name, low_val, high_val = data.split(",")
                self.sensors[id] = Sensor(id, name, low_val, high_val)
                print_message("id: %s ; name: %s, low: %s, high: %s" % (id, name, low_val, high_val), 'info')

    def print_sensors_list(self):
        for s_id, sensor in self.sensors.iteritems():
            print_message("Sensor number %s:\n%s" % (s_id, sensor), 'info')

    def get_udp_message(self):
        try:
            msg = self.udp_socket.recvfrom(1024)[0]
            if self.verbose:
                print_message('Listener - UDP packet received', 'verb')
            values_dict = {}
            sensors_data = msg.split(";")
            for data in sensors_data:
                if len(data) != 0:
                    s_id, value = data.split(":")
                    if self.sensors.has_key(s_id):
                        self.sensors[s_id].update(value)
                        values_dict[self.sensors[s_id].name] = value
            self.message_queue.put(values_dict)
        except timeout, e:
            print_message('Failed to recieve UDP packet', 'fail')
        except IOError, e:
            if e.errno != errno.EINTR:
                raise


def signal_handler(signum, frame):
    print_message('Signal Received - Quitting', 'warn')
    g.keepAlive = False


if __name__ == "__main__":
    global g, logger_thread, listener_thread
    signal.signal(signal.SIGINT, signal_handler)
    print_message('Welcome To TTAURD TELEMATRY SYSTEM', 'info')
    print_message('Starting up...', 'info')
    offline = False
    g = GuiReceiver(verbose='verbose' in sys.argv)
    if not g.ready:
        print_message("Good Bye!", 'info')
        sys.exit(-1)
    # showoff()
    if 'offline' in sys.argv:
        offline = True
        print_message("Starting in offline mode!", 'info')
        g.analyize_sensor_configuration(sensor_conf)
        g.logger = Logger(g.sensors)
        g.logger.log_init()
        print_message("Client [offline] Connected", 'ok')
        offline_thread = WorkerThread(g, 3, verbose='verbose' in sys.argv)
        offline_thread.start()
        print_message('Offline mode started', 'ok')
        with open('tmp_info', 'wb') as info_file:
            info_file.writelines(json.dumps(g.sensors, default=lambda x: x.__dict__))
        print_message("Offline mode setup completed", 'ok')
    else:
        print_message("Starting in Live mode", 'info')
        if not g.client_connect():
            print_message('Failed to start. exiting', 'fail')
            sys.exit(-1)
        print_message("Live mode setup completed", 'ok')
    print_message('Starting worker threads', 'info')
    listener_thread = WorkerThread(g, 0, verbose='verbose' in sys.argv)
    listener_thread.daemon = True
    listener_thread.start()
    print_message('Listener thread started', 'ok')
    logger_thread = WorkerThread(g, 1, verbose='verbose' in sys.argv)
    logger_thread.daemon = True
    logger_thread.start()
    print_message('Logger thread started', 'ok')
    webInterface_thread = WorkerThread(g, 2, verbose='verbose' in sys.argv)
    webInterface_thread.daemon = True
    webInterface_thread.start()
    print_message('WebInterface thread started', 'ok')
    print_message('Initialization completed succesfully', 'ok')
    while g.keepAlive:
        continue
    print_message("Cleanup Stage", 'info')
    if offline:
        print_message("Closing offlne mode", 'info')
        offline_thread.join()
        print_message('Offline mode closed', 'ok')
    os.system('rm tmp*')
    print_message('Temporary files removed', 'ok')
    listener_thread.join()
    print_message('Listener thread joined', 'ok')
    logger_thread.join()
    print_message('Logger thread joined', 'ok')
    print_message("Cleanup Completed", 'ok')
    print_message("Good Bye!", 'info')
    sys.exit(0)
