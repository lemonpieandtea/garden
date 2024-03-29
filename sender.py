import json
import random
import socket
import time
import threading

import constants
from mgprint import gprint

class SenderThread(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)

        self.client_ip = ip
        self.client_port = port

    class Sender():
        def __init__(self, ip, port):
            self.sock = None
            self.client_ip = ip
            self.client_port = port

        def stop_connection(self):
            if self.sock:
                self.sock.close()
                self.sock = None

                gprint(" sender connection closed")

        def init_connection(self):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.client_ip, int(self.client_port)))

            gprint(" sender connection created")

        def send_package(self, package):
            self.sock.send(package.encode("utf8"))
            gprint("  >>> %s:%s %s" % (self.client_ip, self.client_port, package))

    def run(self):
        gprint(" START sender thread")

        self.sender = self.Sender(self.client_ip, self.client_port)

        while not self.sender.sock:
            try:
                self.sender.init_connection()
            except:
                gprint(" ERROR: Can't init connection with server, retry in 1 sec")
                self.sender.stop_connection()
                time.sleep(1)

        self.generate_packages()
        self.sender.stop_connection()

        gprint(" STOP sender thread")

    def generate_packages(self):
        times = constants.NUMBER_OF_PACKAGES

        while times:
            try:
                self.sender.send_package(self.generate_package_json())

                if times:
                    time.sleep(random.randint(1, constants.MAX_NEW_PACKAGE_WAIT_TIME_SEC))
            except:
                gprint(" ERROR: Can't send data to server")
                time.sleep(1)

            times -= 1

    def generate_package_json(self):
        package = json.loads(constants.PACKAGE_TEMPLATE_JSON)

        package["name"] = random.choice(constants.PACKAGE_NAME_VARIANTS)
        package["amount"] = random.randint(constants.PACKAGE_MIN_AMOUNT, constants.PACKAGE_MAX_AMOUNT)
        package["value"] = random.randint(constants.PACKAGE_MIN_VALUE, constants.PACKAGE_MAX_VALUE)
        package["water"] = random.randint(constants.PACKAGE_MIN_WATER, constants.PACKAGE_MAX_WATER)
        package["frequency"] = random.randint(constants.PACKAGE_MIN_FREQUENCY, constants.PACKAGE_MAX_FREQUENCY)
        package["grow_time"] = random.randint(constants.PACKAGE_MIN_GROW_TIME, constants.PACKAGE_MAX_GROW_TIME)

        return json.dumps(package)
