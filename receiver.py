import socket
import threading

import constants
from mgprint import gprint

class ReceiverThread(threading.Thread):
    receiver = None
    server_port = None

    def __init__(self, port):
        threading.Thread.__init__(self)

        self.server_port = port

    class Receiver():
        server_port = None
        sock = None

        def __init__(self, port):
            self.server_port = port

        def stop_connection(self):
            self.sock.close()

        def init_connection(self):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("", int(self.server_port)))

            gprint("receiver connection created...")

        def receive_packages(self):
            times = constants.NUMBER_OF_PACKAGES

            self.sock.listen(1)

            connection, client_address = self.sock.accept()
            gprint("client connected: %s" % str(client_address[0]))

            while times:
                times -= 1

                data = connection.recv(constants.MAX_PACKAGE_BUFFER_SIZE)
                gprint("package received: %s" % data.decode("utf8"))

            connection.close()
            gprint("client disconnected: %s" % str(client_address[0]))

    def run(self):
        gprint("starting receiver...")

        self.receiver = self.Receiver(self.server_port)

        self.receiver.init_connection()
        self.receiver.receive_packages()
        self.receiver.stop_connection()