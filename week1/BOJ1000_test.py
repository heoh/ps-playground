import unittest
from common.unittest import USER_SUFFIX, PSTestCase, Time, MemorySize, parse_testpath

base_dir, problem_name = parse_testpath(__file__)

class BOJ1000(PSTestCase):
    problem_url = 'https://www.acmicpc.net/problem/1000'
    time_limit = Time(seconds=1)
    memory_limit = MemorySize(mb=128)
    main = f'{base_dir}/{problem_name}{USER_SUFFIX}.py'

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
