TEST_DATA = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def check_safe(levels):
    diffs = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]
    if all(1 <= d <= 3 for d in diffs) or all(-3 <= d <= -1 for d in diffs):
        return True
    return False


def solve1(data):
    reports = data.strip().splitlines()
    safe_count = 0
    for report in reports:
        levels = list(map(int, report.split()))
        if check_safe(levels):
            safe_count += 1
    return safe_count


def solve2(data):
    reports = data.strip().splitlines()
    safe_count = 0
    for report in reports:
        levels = list(map(int, report.split()))
        if check_safe(levels):
            safe_count += 1
        else:
            for i in range(len(levels)):
                temp_levels = levels[:i] + levels[i + 1 :]
                if check_safe(temp_levels):
                    safe_count += 1
                    break
    return safe_count


assert solve1(TEST_DATA) == 2
assert check_safe([7, 6, 4, 2, 1]) == True
assert check_safe([1, 2, 7, 8, 9]) == False
assert check_safe([9, 7, 6, 2, 1]) == False
assert check_safe([1, 3, 2, 4, 5]) == False
assert check_safe([8, 6, 4, 4, 1]) == False
assert check_safe([1, 3, 6, 7, 9]) == True

assert solve2(TEST_DATA) == 4

from aocd.models import Puzzle

puzzle = Puzzle(2024, 2)
data = puzzle.input_data

part1_solution = solve1(data)
part2_solution = solve2(data)

print("Part 1:", part1_solution)
print("Part 2:", part2_solution)

puzzle.answer_a = part1_solution
puzzle.answer_b = part2_solution
