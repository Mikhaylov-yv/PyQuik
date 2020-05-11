class Orders:

    # price - цена для заявки
    # operation - тип операции
    #   'B': покупка 'S': продажа
    # type - тип заявки "L": лимитированная
    # quantity - количество пакетов в
    def sendOrder(self, price, operation, type,  quantity = 1):
        # Запрос: {"data": {"CLASSCODE": "QJSIM", "SECCODE": "SBER", "ACTION": "NEW_ORDER", "ACCOUNT": "NL0011100043",
        #                   "CLIENT_CODE": "6214947", "QUANTITY": "1", "PRICE": "185,25", "OPERATION": "B",
        #                   "TRANS_ID": "6214947", "TYPE": "L"}, "id": 33, "cmd": "sendTransaction", "t": 1589204285663}
        # Ответ
        # сервера: {"id": 33, "t": 1589204285663, "data": true, "cmd": "sendTransaction"}
        data = {"CLASSCODE": self.classCode, "SECCODE": self.securityCode, "ACTION": 'NEW_ORDER', "ACCOUNT": self.account,
               "CLIENT_CODE": self.clientCode, "QUANTITY": quantity, "PRICE": price, "OPERATION": operation,
               "TRANS_ID": self.clientCode, "TYPE": type}

        self.getRequest(cmd = 'sendTransaction', data = data)
