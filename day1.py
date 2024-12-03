TEST_DATA = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def solve_part1(data):
    left_list = []
    right_list = []
    for line in data.strip().splitlines():
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)
    left_list.sort()
    right_list.sort()
    total_distance = 0
    for i in range(len(left_list)):
        total_distance += abs(left_list[i] - right_list[i])
    return total_distance


def solve_part2(data):
    left_list = []
    right_list = []
    for line in data.strip().splitlines():
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)
    similarity_score = 0
    for num in left_list:
        similarity_score += num * right_list.count(num)
    return similarity_score


# Test cases for Part 1
assert solve_part1(TEST_DATA) == 11

# Test cases for Part 2
assert solve_part2(TEST_DATA) == 31

# Solve the puzzle with real data
from aocd.models import Puzzle

puzzle = Puzzle(2024, 1)
data = puzzle.input_data

part1_solution = solve_part1(data)
part2_solution = solve_part2(data)

print("Part 1:", part1_solution)
print("Part 2:", part2_solution)

puzzle.answer_a = part1_solution
puzzle.answer_b = part2_solution
