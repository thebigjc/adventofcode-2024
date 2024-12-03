import re
from aocd.models import Puzzle

TEST_DATA = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

TEST_DATA_2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)do()?mul(8,5))
"""

def solve_part1(data):
    total = 0
    for match in re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', data):
        num1, num2 = map(int, match.groups())
        total += num1 * num2
    return total

def solve_part2(data):
    total = 0
    enabled = True
    for match in re.finditer(r'(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))', data):
        instruction = match.group(0)
        if instruction == 'do()':
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif instruction.startswith('mul(') and enabled:
            num1, num2 = map(int, match.groups()[1:])
            total += num1 * num2
    return total

# Test cases for Part 1
def test_part1():
    assert solve_part1(TEST_DATA) == 161
    print("Part 1 tests passed")

# Test cases for Part 2
def test_part2():
    assert solve_part2(TEST_DATA_2) == 48
    print("Part 2 tests passed")

# Run tests
test_part1()
test_part2()

# Solve the real puzzle
puzzle = Puzzle(2024, 3)
p1 = solve_part1(puzzle.input_data)
print(f"Part 1: {p1}")
puzzle.answer_a = p1

p2 = solve_part2(puzzle.input_data)
print(f"Part 2: {p2}")
puzzle.answer_b = p2