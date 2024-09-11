import unittest
from common.unittest import PSTestCase, Time, MemorySize

class BOJ1000(PSTestCase):
    problem_url = 'https://www.acmicpc.net/problem/1000'
    time_limit = Time(seconds=1)
    memory_limit = MemorySize(mb=128)
    main = 'week1/BOJ1000.h2.py'

    def test_case1(self):
        input = """
            1 2
        """
        output = """
            3
        """
        self.assertTC(self.main, input, output)

if __name__ == '__main__':
    unittest.main()
