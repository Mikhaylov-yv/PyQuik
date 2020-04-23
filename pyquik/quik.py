import socket
import json
from datetime import datetime
import time
from ast import literal_eval as le

class Quik:
    port_requests = 34130
    port_callbacks = 34131
    host = "127.0.0.1"
    CRLF = "\r\n\r\n"
    classCode = "SPBFUT,TQBR,TQBS,TQNL,TQLV,TQNE,TQOB,CETS"


    def __init__(self):
        self.sok_requests = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sok_callbacks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sok_callbacks.connect((self.host, self.port_callbacks))
        self.sok_requests.connect((self.host, self.port_requests))
        self.clientCode = ''
        self.id = 0

    # Проверяет связь с программой
    def connekt(self):
       if "lua_error" not in list(self.getRequest('getWorkingFolder')):
           if self.getRequest('isConnected')['cmd'] == 'isConnected':
               print('Подключение выполненно')
           # time.sleep(2)

    # Создание инструмента
    def tool(self, secCode):
        data = self.classCode + '|' + secCode
        secClass = self.getRequest(cmd='getSecurityClass', data=data)['data']
        # Зачем нужен clientCode пока не понятно
        self.clientCode = self.getRequest(cmd='getClientCode')
        self.toll = self.getRequest(cmd = 'getSecurityInfo',data = str(secClass) + '|' + str(secCode))

    # Определение secClass для создания инструмента
    def getSecurityClass(self, secCode):
        data = self.classCode + '|' + secCode
        secClass = self.getRequest(cmd = 'getSecurityClass',data = data)['data']
        self.clientCode = self.getRequest(cmd = 'getClientCode')
        return secClass

    # Метод для выполнения запроса к LUA скрипту
    def getRequest(self, cmd, data = '', t = 0):
        self.id = self.id + 1
        request = {"data": data, "id": self.id, "cmd": cmd, "t": t}
        raw_data = json.dumps(request)
        self.sok_requests.sendall((raw_data + self.CRLF).encode())
        while (True):
            response = self.sok_requests.recv(2048)
            response = le(response.decode('ANSI')[:-1])
            print('Запрос: ' + str(request) + '\n' + 'Ответ: ' + str(response))
            return response


if __name__ == '__main__':
    q = Quik()
    q.connekt()
    q.tool('USD000UTSTOM')
    # print(q.get_request('getSecurityClass', data =  'SPBFUT,TQBR,TQBS,TQNL,TQLV,TQNE,TQOB,CETS|USD000000TOD'))
    # request = {"data":"SPBFUT,TQBR,TQBS,TQNL,TQLV,TQNE,TQOB,CETS|USD000000TOD","id":3,"cmd":"getSecurityClass","t":0}
    # print(q.get_workingfolder(request))
    # request = {"data":"","id":4,"cmd":"getClientCode","t":0}
    # print(q.get_workingfolder(request))
    # request = {"data":"CETS|USD000000TOD","id":5,"cmd":"getSecurityInfo","t":0}
    # print(q.get_workingfolder(request))
    # request = {"data":"MB0002500000|400K74Z|USD000000TOD|MB0002513352|2","id":6,"cmd":"getDepoEx","t":0}
    # print(q.get_workingfolder(request))




