class Orders:

    # price - цена для заявки
    # operation - тип операции
    #   'B': покупка 'S': продажа
    # type - тип заявки "L": лимитированная
    # quantity - количество пакетов в
    def sendOrder(self, price, operation, type,  quantity = 1):
        price = self.price_step * round(price / self.price_step)
        data = {"CLASSCODE": self.classCode, "SECCODE": self.securityCode, "ACTION": 'NEW_ORDER', "ACCOUNT": self.account,
               "CLIENT_CODE": self.clientCode, "QUANTITY": str(int(quantity)), "PRICE": str(price), "OPERATION": operation,
               "TRANS_ID": self.clientCode, "TYPE": type}

        self.getRequest(cmd = 'sendTransaction', data = data)
