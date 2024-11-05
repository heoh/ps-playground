# import sys; input = sys.stdin.readline

S, E = range(2)
INF = float('inf')

M = int(input())
lines = []
while True:
    s, e = map(int, input().split())
    if (s, e) == (0, 0):
        break
    if s > e:
        s, e = e, s
    if e < 0 or M < s:
        continue
    line = (max(s, 0), min(e, M))
    lines.append(line)

def solve():
    lines.sort(key=lambda x: (x[S], -x[E]))
    if lines[0][S] > 0:
        return 0

    dp = [INF] * (M+1)
    for s, e in lines:
        n = dp[s-1] if s > 0 else 0
        if n == INF:
            return 0
        for i in range(e, s-1, -1):
            if dp[i] <= n+1:
                break
            dp[i] = n+1

    return dp[M] if dp[M] < INF else 0

print(solve())
