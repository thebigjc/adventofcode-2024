from aocd.models import Puzzle

puzzle = Puzzle(2024, 2)

def check(a):
    if len(a) < 2: return True
    diff = a[1] - a[0]
    if diff == 0 or abs(diff) > 3: return False
    for i in range(2, len(a)):
        d = a[i] - a[i-1]
        if d == 0 or abs(d) > 3 or d * diff < 0: return False
    return True

def solve1(data):
    safe_count = 0
    for line in data.strip().split('\n'):
        a = list(map(int, line.split()))
        if check(a): safe_count += 1
    return safe_count

def solve2(data):
    safe_count = 0
    for line in data.strip().split('\n'):
        a = list(map(int, line.split()))
        if check(a):
            safe_count += 1
            continue
        for i in range(len(a)):
            b = a[:i] + a[i+1:]
            if check(b):
                safe_count += 1
                break
    return safe_count

p1 = solve1(puzzle.input_data)
print("Part 1:", p1)
puzzle.answer_a = p1

p2 = solve2(puzzle.input_data)
print("Part 2:", p2)
puzzle.answer_b = p2

