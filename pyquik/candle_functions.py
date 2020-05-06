# Функции для работы со свечами
import pandas as pd

# Осуществляетподпискунаполучениеисторическихданных(свечи)
#
# param
# name = "classCode" > Классинструмента.
# name = "securityCode" > Код
# name = "interval" > интервал свечей(тайм - фрейм)

class CandleFunctions:

    def getLastCandles(self, interval, count):
        # Запрос: {"data": "CETS|USD000UTSTOM|60", "id": 33, "cmd": "subscribe_to_candles", "t": 1588619654879}
        self.getRequest(cmd='subscribe_to_candles',data = f'{self.classCode}|{self.securityCode}|{interval}')
        # Запрос: {"data": "CETS|USD000UTSTOM|60", "id": 34, "cmd": "is_subscribed", "t": 1588619654886}
        self.getRequest(cmd='is_subscribed', data=f'{self.classCode}|{self.securityCode}|{interval}')
        # Запрос: {"data": "CETS|USD000UTSTOM|60|0", "id": 35, "cmd": "get_candles_from_data_source", "t": 1588619654890}
        candles = self.getRequest(cmd='get_candles_from_data_source', data=f'{self.classCode}|{self.securityCode}|{interval}|{count}')
        # Создание Pandas
        df = pd.DataFrame()
        for candl in candles['data']:
            datetime = candl['datetime']
            datetime = f'{datetime["year"]}-{datetime["month"]}-{datetime["day"]} {datetime["hour"]}:{datetime["min"]}:{datetime["sec"]}'
            df.loc[pd.to_datetime(datetime), ['OPEN','HIGH','LOW','CLOSE','VOL']] = [candl['open'], candl['high'],
                                                                           candl['low'], candl['close'], candl['volume']]
            # print(candl['datetime'])
        print(df)


