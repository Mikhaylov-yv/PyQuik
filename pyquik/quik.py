import socket
import json
from datetime import datetime
import time
from ast import literal_eval as le

from orderbook import OrderBook
from candle_functions import CandleFunctions

class Quik(OrderBook, CandleFunctions):
    port_requests = 34130
    port_callbacks = 34131
    host = "127.0.0.1"
    CRLF = "\r\n\r\n"
    secClass_list = "SPBFUT,TQBR,TQBS,TQNL,TQLV,TQNE,TQOB,CETS,QJSIM"


    def __init__(self):

        # Используемые переменные
        self.clientCode = '' # '400K74Z'
        self.tradeAccount = '' # 'MB0002513352'
        self.classCode = '' # 'CETS'
        self.securityCode = ''  # 'USD000UTSTOM'
        self.firmid = '' # 'MB0002500000'
        self.id = 0


    # Проверяет связь с программой
    def connekt(self):
        self.sok_requests = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sok_callbacks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sok_callbacks.connect((self.host, self.port_callbacks))
        self.sok_requests.connect((self.host, self.port_requests))

        if "lua_error" not in list(self.getRequest('getWorkingFolder')):
            if self.getRequest('isConnected')['cmd'] == 'isConnected':
               print('Подключение выполненно')
           # time.sleep(2)

    def get_orderBook(self):
        OrderBook.get_orderBook(self)


    # Создание инструмента
    def tool(self, toolCode):
        self.securityCode = toolCode
        data = self.secClass_list + '|' + toolCode
        self.classCode = self.getRequest(cmd='getSecurityClass', data=data)['data']
        self.clientCode = self.getRequest(cmd='getClientCode')['data']
        self.toll = self.getRequest(cmd = 'getSecurityInfo', data =self.classCode + '|' + toolCode)['data']
        self.tradeAccount = self.getRequest(cmd = 'getTradeAccount', data = self.classCode)['data']
        self.toll_info = self.getRequest(cmd = 'getClassInfo', data = self.classCode)['data']
        self.firmid = self.toll_info['firmid']

    # Определение secClass для создания инструмента
    def getSecurityClass(self, secCode):
        data = self.secClass_list + '|' + secCode
        secClass = self.getRequest(cmd = 'getSecurityClass',data = data)['data']
        self.clientCode = self.getRequest(cmd = 'getClientCode')
        return secClass

    # Метод для выполнения запроса к LUA скрипту
    def getRequest(self, cmd, data = '', t = 0):
        self.id = self.id + 1
        request = {"data": data, "id": self.id, "cmd": cmd, "t": t}
        raw_data = json.dumps(request)
        self.sok_requests.sendall((raw_data + self.CRLF).encode())
        response = b''
        # Запускаем бесконечный цикл получения данных с принудительными выходами
        while True:
            try:
                # Получаем сообщения и складываем пока не получится объект типпа dict
                chunk = self.sok_requests.recv(8192)
                if not chunk:  # chunk == ''
                    break
                response += chunk
                try:
                    response_out = response.decode('ANSI')
                    response_out = le(response_out.replace('true', '"true"').replace('false', '"false"'))
                    if type(response_out) is dict: break
                except:
                    continue
            except socket.error:
                self.sok_requests.close()
                break
        print('Запрос: ' + str(request) + '\n' + 'Ответ: ' + str(response))
        response = response_out
        return response


if __name__ == '__main__':
    q = Quik()
    q.connekt()
    q.tool('SBER')
    q.getLastCandles(10,0)



