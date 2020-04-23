import time

class OrderBook:

    def get_orderBook(self):
        # Запрос: {"data":"CETS|USD000UTSTOM|SEC_PRICE_STEP","id":8,"cmd":"getParamEx","t":1587660869557}
        self.getRequest(cmd='getParamEx',data = self.clientCode + '|' + self.toolCode + '|' + 'SEC_PRICE_STEP')
        # Запрос: {"data": "CETS|USD000UTSTOM|SEC_SCALE", "id": 9, "cmd": "getParamEx", "t": 1587660869561}
        self.getRequest(cmd='getParamEx',data = self.clientCode + '|' + self.toolCode + '|' + 'SEC_SCALE')
        # Запрос: {"data":"CETS|USD000UTSTOM|LOTSIZE","id":10,"cmd":"getParamEx","t":1587660869562}
        self.getRequest(cmd='getParamEx', data=self.clientCode + '|' + self.toolCode + '|' + 'LOTSIZE')
        # Запрос: {"data":"CETS|USD000UTSTOM","id":13,"cmd":"Subscribe_Level_II_Quotes","t":1587660869576}
        self.getRequest(cmd='Subscribe_Level_II_Quotes', data=self.secClass + '|' + self.toolCode )
        # Запрос: {"data":"CETS|USD000UTSTOM","id":14,"cmd":"IsSubscribed_Level_II_Quotes","t":1587660869588}
        self.getRequest(cmd='IsSubscribed_Level_II_Quotes', data=self.secClass + '|' + self.toolCode)
        # Запрос: {"data":"CETS|USD000UTSTOM","id":14,"cmd":"IsSubscribed_Level_II_Quotes","t":1587660869588}
        self.getRequest(cmd='IsSubscribed_Level_II_Quotes', data=self.secClass + '|' + self.toolCode)
        print('==========================\n==========================')
        # Бесконечная подписка на стакан
        while (True):
            # Запрос: {"data": "CETS|USD000UTSTOM|LAST", "id": 11, "cmd": "getParamEx", "t": 1587660869568}
            self.getRequest(cmd='getParamEx', data=self.secClass + '|' + self.toolCode + '|' + 'LAST')
            # Запрос: {"data":"MB0002500000|400K74Z|USD000UTSTOM|MB0002513352|2","id":12,"cmd":"getDepoEx","t":1587660869571}
            self.getRequest(cmd='getDepoEx', data=self.firmid + '|' + self.clientCode + '|'
                                                  + self.toolCode + '|' + self.tradeAccount + '|2')
            time.sleep(1)

if __name__ == '__main__':
    o = OrderBook()
