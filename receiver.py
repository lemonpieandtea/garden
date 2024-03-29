import json
import socket
import threading

import constants
import garden
from plant import json_to_plant
from mgprint import gprint

class ReceiverThread(threading.Thread):
    def __init__(self, garden, port):
        threading.Thread.__init__(self)

        self.garden = garden
        self.server_port = port

    class Receiver():
        def __init__(self, garden, port):
            self.garden = garden
            self.server_port = port

        def stop_connection(self):
            if self.sock:
                self.sock.close()
                self.sock = None

                gprint(" receiver connection closed")

        def init_connection(self):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("", int(self.server_port)))

            gprint(" receiver connection created")

        def receive_packages(self):
            times = constants.NUMBER_OF_PACKAGES

            self.sock.listen(1)

            connection, client_address = self.sock.accept()
            gprint("  client: %s" % str(client_address[0]))

            while times:
                data = connection.recv(constants.MAX_PACKAGE_BUFFER_SIZE)

                if data:
                    gprint("  <<< %s" % data.decode("utf8"))

                    try:
                        data_json = json.loads(data.decode("utf8"))

                        for item in range(int(data_json["amount"])):
                            self.garden.plant(json_to_plant(data_json))
                        times -= 1
                    except:
                        gprint("  ERROR: Wrong data received")

            connection.close()
            gprint("  disconnected: %s" % str(client_address[0]))

            self.garden.stop()

    def run(self):
        gprint(" START receiver thread")

        self.receiver = self.Receiver(self.garden, self.server_port)

        self.receiver.init_connection()
        self.receiver.receive_packages()
        self.receiver.stop_connection()

        gprint(" STOP receiver thread")
