import socket
import json


class Quik:
    port_requests = 34130
    port_callbacks = 34131
    host = "127.0.0.1"
    CRLF = "\r\n\r\n"


    def __init__(self):
        self.sok_requests = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sok_callbacks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sok_callbacks.connect((self.host, self.port_callbacks))
        self.sok_requests.connect((self.host, self.port_requests))

    def get_workingfolder(self):
        request = {"data": "", "id": 1, "cmd": "getWorkingFolder", "t": 1587498697959}
        raw_data = json.dumps(request)
        self.sok_requests.sendall((raw_data + self.CRLF).encode())
        while (True):
            response = self.sok_requests.recv(2048)
            return response


if __name__ == '__main__':
    q = Quik()
    print(q.get_workingfolder())



