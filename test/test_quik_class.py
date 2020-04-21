import sys
sys.path.append(r'..\pyquik')
import quik
import unittest

class TestConnect(unittest.TestCase):

    def test_request(self):
        # Проблема с изменением вромени при тестировании
        q = quik.Quik()
        self.assertEqual(str(q.get_workingfolder()),
             '{"id":1,"t":1587501527485.7,"data":"C:\\\\SBERBANK\\\\QUIK_x64","cmd":"getWorkingFolder"}\n')

if __name__ == '__main__':
    unittest.main()