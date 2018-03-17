from threading import Thread
from gui import WebInterface
import csv, errno, signal

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

    def run_gui(self):
        WebInterface.run()
        #while self.guireceiver.keepAlive:
        #    continue
        print "\nGUI is shutting Down"

    def get_udp_message(self):
        while self.guireceiver.keepAlive:
            self.guireceiver.get_udp_message()
        print "\nListener Thread Has finished"    

    def run_logger(self):
        try:
            with open(self.guireceiver.logger.log_file, 'ab') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.guireceiver.logger.sensor_names)
                while self.guireceiver.keepAlive or self.guireceiver.message_queue.qsize() > 0:
                    values = self.guireceiver.message_queue.get()
                    print values
                    writer.writerow(values)
            print "Logger Thread Has finished"    
        except IOError, e:
            if e.errno != errno.EINTR:
                raise
