import unittest
from pstest import PSTestCase, Time, MemorySize

class Test(PSTestCase):
    problem_url = "https://dmoj.ca/problem/aplusb"
    # time_limit = Time(seconds=5)
    # memory_limit = MemorySize(mb=256)

    def test_case1(self):
        input = """
            1
            -1 0
            0 1
            0 0
        """
        output = """
            1
        """
        self.assertTC(self.main, input, output)

    def test_case2(self):
        input = """
            1
            -1 0
            -5 -3
            2 5
            0 0
        """
        output = """
            0
        """
        self.assertTC(self.main, input, output)

    def test_case_u1(self):
        input = """
            1
            -5 -3
            -3 0
            0 1
            0 0
        """
        output = """
            1
        """
        self.assertTC(self.main, input, output)

    def test_case_u2(self):
        input = """
            3
            0 2
            2 4
            0 0
        """
        output = """
            2
        """
        self.assertTC(self.main, input, output)

    def test_case_u1(self):
        input = """
            3
            0 2
            2 4
            4 6
            0 0
        """
        output = """
            2
        """
        self.assertTC(self.main, input, output)

    def test_case_u4(self):
        input = """
            4
            -1 2
            0 1
            1 2
            2 4
            0 0
        """
        output = """
            2
        """
        self.assertTC(self.main, input, output)

    def random_test(self, SEED, M, LINE_N, LINE_RANGE, LINE_MAX_LEN=float('inf')):
        import random
        rand = random.Random(SEED)
        lines = [sorted((rand.randint(*LINE_RANGE), rand.randint(*LINE_RANGE))) for _ in range(LINE_N)]
        lines = list(filter(lambda line: line != [0, 0], lines))
        for line in lines:
            line_len = line[1] - line[0] + 1
            if line_len > LINE_MAX_LEN:
                line[1] = line[0] + LINE_MAX_LEN - 1
        def solve(lines):
            X = [0] * (M+1)
            def select(line, drop=False):
                for i in range(max(line[0], 0), min(line[1], M)+1):
                    X[i] += -1 if drop else 1
            def check():
                for x in X:
                    if x == 0:
                        return False
                return True
            def dfs(n, i):
                best = float('inf')
                if i == len(lines):
                    return n if check() else best
                best = min(best, dfs(n, i+1))
                select(lines[i])
                best = min(best, dfs(n+1, i+1))
                select(lines[i], drop=True)
                return best
            answer = dfs(0, 0)
            return answer if answer < float('inf') else 0
        answer = solve(lines)

        input = ''
        input += f'{M}\n'
        for s, e in lines:
            input += f'{s} {e}\n'
        input += '0 0\n'
        output = f'{answer}\n'
        self.assertTC(self.main, input, output)

    def test_case_r1(self):
        for i in range(10000):
            self.random_test(
                SEED=i,
                M=10,
                LINE_N=10,
                LINE_RANGE=(-5, 15),
                # LINE_MAX_LEN=3,
            )

    def test_case_r2(self):
        self.random_test(
            SEED=192,
            M=10,
            LINE_N=10,
            LINE_RANGE=(-5, 15),
        )



if __name__ == "__main__":
    unittest.main()
