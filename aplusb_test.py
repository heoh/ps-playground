import unittest
from pstest import PSTestCase, Time, MemorySize

class APlusBTest(PSTestCase):
    problem_url = "https://dmoj.ca/problem/aplusb"
    time_limit = Time(seconds=5)
    memory_limit = MemorySize(mb=256)

    def test_case1(self):
        input = """
            2
            1 1
            -1 0
        """
        output = """
            2
            -1
        """
        self.assertTC(self.main, input, output)

if __name__ == "__main__":
    unittest.main()
