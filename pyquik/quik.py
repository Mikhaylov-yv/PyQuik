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
    secClass_list = "SPBFUT,TQBR,TQBS,TQNL,TQLV,TQNE,TQOB,CETS"


    def __init__(self):
        self.sok_requests = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sok_callbacks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sok_callbacks.connect((self.host, self.port_callbacks))
        self.sok_requests.connect((self.host, self.port_requests))
        # Используемые переменные
        self.clientCode = '' # '400K74Z'
        self.tradeAccount = '' # 'MB0002513352'
        self.secClass = '' # 'CETS'
        self.toolCode = ''  # 'USD000UTSTOM'
        self.firmid = '' # 'MB0002500000'
        self.id = 0


    # Проверяет связь с программой
    def connekt(self):
       if "lua_error" not in list(self.getRequest('getWorkingFolder')):
           if self.getRequest('isConnected')['cmd'] == 'isConnected':
               print('Подключение выполненно')
           # time.sleep(2)

    def get_orderBook(self,toolCode):
        self.toolCode = toolCode
        self.tool(toolCode)
        # Запрос: {"data":"CETS|USD000UTSTOM|SEC_PRICE_STEP","id":8,"cmd":"getParamEx","t":1587660869557}
        self.getRequest(cmd='getParamEx',data = self.clientCode + '|' + toolCode + '|' + 'SEC_PRICE_STEP')
        # Запрос: {"data": "CETS|USD000UTSTOM|SEC_SCALE", "id": 9, "cmd": "getParamEx", "t": 1587660869561}
        self.getRequest(cmd='getParamEx',data = self.clientCode + '|' + toolCode + '|' + 'SEC_SCALE')
        # Запрос: {"data":"CETS|USD000UTSTOM|LOTSIZE","id":10,"cmd":"getParamEx","t":1587660869562}
        self.getRequest(cmd='getParamEx', data=self.clientCode + '|' + toolCode + '|' + 'LOTSIZE')
        # Запрос: {"data":"CETS|USD000UTSTOM","id":13,"cmd":"Subscribe_Level_II_Quotes","t":1587660869576}
        self.getRequest(cmd='Subscribe_Level_II_Quotes', data=self.secClass + '|' + toolCode )
        # Запрос: {"data":"CETS|USD000UTSTOM","id":14,"cmd":"IsSubscribed_Level_II_Quotes","t":1587660869588}
        self.getRequest(cmd='IsSubscribed_Level_II_Quotes', data=self.secClass + '|' + toolCode)
        # Запрос: {"data":"CETS|USD000UTSTOM","id":14,"cmd":"IsSubscribed_Level_II_Quotes","t":1587660869588}
        self.getRequest(cmd='IsSubscribed_Level_II_Quotes', data=self.secClass + '|' + toolCode)
        while (True):
            # Запрос: {"data": "CETS|USD000UTSTOM|LAST", "id": 11, "cmd": "getParamEx", "t": 1587660869568}
            self.getRequest(cmd='getParamEx', data=self.clientCode + '|' + toolCode + '|' + 'LAST')
            # Запрос: {"data":"MB0002500000|400K74Z|USD000UTSTOM|MB0002513352|2","id":12,"cmd":"getDepoEx","t":1587660869571}
            self.getRequest(cmd='getDepoEx', data=self.firmid + '|' + self.clientCode + '|'
                                                  + self.toolCode + '|' + self.tradeAccount + '|2')

    # Создание инструмента
    def tool(self, toolCode):
        data = self.secClass_list + '|' + toolCode
        self.secClass = self.getRequest(cmd='getSecurityClass', data=data)['data']
        # Зачем нужен clientCode пока не понятно
        self.clientCode = self.getRequest(cmd='getClientCode')['data']
        self.toll = self.getRequest(cmd = 'getSecurityInfo', data = self.secClass + '|' + toolCode)['data']
        self.tradeAccount = self.getRequest(cmd = 'getTradeAccount', data = self.secClass)['data']
        self.toll_info = self.getRequest(cmd = 'getClassInfo',data = self.secClass)['data']
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
        while (True):
            response = self.sok_requests.recv(2048)
            try:
                response = le(response.decode('ANSI'))
            except:
                response = le(response.decode('ANSI').replace('true','"true"'))
            print('Запрос: ' + str(request) + '\n' + 'Ответ: ' + str(response))
            return response


if __name__ == '__main__':
    q = Quik()
    q.connekt()
    q.get_orderBook('USD000UTSTOM')
    # print(q.get_request('getSecurityClass', data =  'SPBFUT,TQBR,TQBS,TQNL,TQLV,TQNE,TQOB,CETS|USD000000TOD'))
    # request = {"data":"SPBFUT,TQBR,TQBS,TQNL,TQLV,TQNE,TQOB,CETS|USD000000TOD","id":3,"cmd":"getSecurityClass","t":0}
    # print(q.get_workingfolder(request))
    # request = {"data":"","id":4,"cmd":"getClientCode","t":0}
    # print(q.get_workingfolder(request))
    # request = {"data":"CETS|USD000000TOD","id":5,"cmd":"getSecurityInfo","t":0}
    # print(q.get_workingfolder(request))
    # request = {"data":"MB0002500000|400K74Z|USD000000TOD|MB0002513352|2","id":6,"cmd":"getDepoEx","t":0}
    # print(q.get_workingfolder(request))




