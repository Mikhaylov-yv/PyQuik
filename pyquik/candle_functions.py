# Функции для работы со свечами
import pandas as pd

# Осуществляетподпискунаполучениеисторическихданных(свечи)
#
# param
# name = "classCode" > Классинструмента.
# name = "securityCode" > Код
# name = "interval" > интервал свечей(тайм - фрейм)

class CandleFunctions:
    # Получает заданное количество последних свечей
    # interval свеча в минутах
    # count количество свечей 0 - все доступные
    def getLastCandles(self, interval, count):
        self._getLeadUp(interval)
        # Запрос: {"data": "CETS|USD000UTSTOM|60|0", "id": 35, "cmd": "get_candles_from_data_source", "t": 1588619654890}
        candles = self.getRequest(cmd='get_candles_from_data_source', data=f'{self.classCode}|{self.securityCode}|{interval}|{count}')
        # Создание Pandas
        self._toPandas(candles)

    # Осуществляет подписку на получение исторических данных (свечи)
    def subscribe(self, interval):
        self.getRequest(cmd='subscribe_to_candles',
                        data=f'{self.classCode}|{self.securityCode}|{interval}')

    # Отписывается от получения исторических данных (свечей)
    def unSubscribe(self,interval):
        self.getRequest(cmd='unsubscribe_from_candles',
                        data=f'{self.classCode}|{self.securityCode}|{interval}')

    # Проверка состояния подписки на исторические данные (свечи)
    def IsSubscribed(self, interval):
        response = self.getRequest(cmd='is_subscribed',
                        data=f'{self.classCode}|{self.securityCode}|{interval}')
        return  bool(response['data'])

    # Подписка на получение новых свечей по заданному интервалу
    def getSubLastCandles(self,interval):
        # Запрос: {"data": "CETS|USD000UTSTOM|1", "id": 4, "cmd": "is_subscribed", "t": 1588796396087}
        # Запрос: {"data": "CETS|USD000UTSTOM|1", "id": 5, "cmd": "unsubscribe_from_candles", "t": 1588796396096}
        # Запрос: {"data": "CETS|USD000UTSTOM|1", "id": 6, "cmd": "is_subscribed", "t": 1588796396097}
        # Запрос: {"data": "CETS|USD000UTSTOM|1", "id": 7, "cmd": "subscribe_to_candles", "t": 1588796396099}
        # Запрос: {"data": "CETS|USD000UTSTOM|1", "id": 8, "cmd": "is_subscribed", "t": 1588796396101}
        # Sec: USD000UTSTOM, Open: 74, 535, Close: 74, 555, Volume: 732
        # Проверяем подписку если есть отписываемся
        if self.IsSubscribed(interval):
            self.unSubscribe(interval)
        count = 1
        self.getSubs(cmd='get_candles_from_data_source',
                                      data=f'{self.classCode}|{self.securityCode}|{interval}|{count}')
        # self.subscribe(interval)
        # self.getSubs(cmd='is_subscribed',
        #                 data=f'{self.classCode}|{self.securityCode}|{interval}')



    def _getLeadUp(self, interval):
        # Запрос: {"data": "CETS|USD000UTSTOM|60", "id": 33, "cmd": "subscribe_to_candles", "t": 1588619654879}
        self.getRequest(cmd='subscribe_to_candles', data=f'{self.classCode}|{self.securityCode}|{interval}')
        # Запрос: {"data": "CETS|USD000UTSTOM|60", "id": 34, "cmd": "is_subscribed", "t": 1588619654886}
        self.getRequest(cmd='is_subscribed', data=f'{self.classCode}|{self.securityCode}|{interval}')

    def _toPandas(self, candles):
        df = pd.DataFrame()
        for candl in candles['data']:
            datetime = candl['datetime']
            datetime = f'{datetime["year"]}-{datetime["month"]}-{datetime["day"]} {datetime["hour"]}:{datetime["min"]}:{datetime["sec"]}'
            df.loc[pd.to_datetime(datetime), ['OPEN','HIGH','LOW','CLOSE','VOL']] = [candl['open'], candl['high'],
                                                                           candl['low'], candl['close'], candl['volume']]
            # print(candl['datetime'])
        print(df)


