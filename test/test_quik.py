import sys

sys.path.append(r'..\pyquik')
sys.path.append(r'')
from test_data import Test_data
import quik


def test_connekt():
    q = quik.Quik()
    assert q.port_requests == 34130


def test_get_order_book():
    assert False


def test_tool():
    assert False


def test_get_security_class():
    assert False


def test_get_request():
    q = quik.Quik()
    q.connekt()
    q.tool('SBER')
    response = q.getRequest(cmd='get_candles_from_data_source', data='QJSIM|SBER|10|10')
    assert Test_data.response_lastCandles['data'] == response
