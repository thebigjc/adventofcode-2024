from concurrent.futures import ThreadPoolExecutor
from aocd.models import Puzzle

TEST_DATA = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

def can_achieve_target(target, numbers, allow_concatenation=False):
    possible_values = {numbers[0]}
    for next_num in numbers[1:]:
        new_values = set()
        for val in possible_values:
            # '+'
            add_val = val + next_num
            if add_val <= target:
                new_values.add(add_val)
            # '*'
            mul_val = val * next_num
            if mul_val <= target:
                new_values.add(mul_val)
            # '||' if allowed
            if allow_concatenation:
                concat_val = int(str(val) + str(next_num))
                if concat_val <= target:
                    new_values.add(concat_val)
        possible_values = new_values
        if not possible_values:
            return False
    return target in possible_values

def process_line(line, allow_concatenation=False):
    if not line.strip():
        return 0
    lhs, rhs = line.split(':')
    target = int(lhs.strip())
    numbers = list(map(int, rhs.strip().split()))
    return target if can_achieve_target(target, numbers, allow_concatenation) else 0

def solve_with_data(data, allow_concatenation=False, parallel=True):
    lines = data.strip().split('\n')
    if parallel:
        # Using ThreadPoolExecutor to avoid pickling issues.
        # Note: This might not speed up CPU-bound tasks much due to the GIL,
        # but it will avoid the pickling error encountered with ProcessPoolExecutor.
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda l: process_line(l, allow_concatenation), lines))
        return sum(results)
    else:
        total = 0
        for line in lines:
            total += process_line(line, allow_concatenation)
        return total

if __name__ == "__main__":
    test_part1 = solve_with_data(TEST_DATA, allow_concatenation=False, parallel=True)
    print("Test Part 1 Result:", test_part1)
    assert test_part1 == 3749, f"Expected 3749, got {test_part1}"
    print("Part 1 Test passed!")
    
    test_part2 = solve_with_data(TEST_DATA, allow_concatenation=True, parallel=True)
    print("Test Part 2 Result:", test_part2)
    assert test_part2 == 11387, f"Expected 11387, got {test_part2}"
    print("Part 2 Test passed!")
    
    # Solve real data
    puzzle = Puzzle(year=2024, day=7)
    real_data = puzzle.input_data

    # Part 1 answer
    p1 = solve_with_data(real_data, allow_concatenation=False, parallel=True)
    print("Part 1 Answer:", p1)
    puzzle.answer_a = p1

    # Part 2 answer
    p2 = solve_with_data(real_data, allow_concatenation=True, parallel=True)
    print("Part 2 Answer:", p2)
    puzzle.answer_b = p2
