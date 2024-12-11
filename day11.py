from aocd.models import Puzzle
import time
import numpy as np
from collections import Counter

TEST_DATA = """0 1 10 99 999"""

def transform(stones_dict):
    new_stones = Counter()

    for s, c in stones_dict.items():
        items = new_items(s)
        for r in items:
            new_stones[r] += c

    return new_stones

def new_items(s):
    if s == "0":
        # Rule 1
        return ("1", )
    else:
        length = len(s)
        if length % 2 == 0:
                # Rule 2: even number of digits, split into two stones
            half = length // 2
            left = s[:half].lstrip('0') or '0'  # Remove leading zeros, default to '0'
            right = s[half:].lstrip('0') or '0'
            return (left, right)
        else:
                # Rule 3: odd number of digits, multiply by 2024
            val = int(s) * 2024
            return (str(val), )

def blink(stones, times=1):
    durations = []
    total_start = time.time()
    stones_dict = Counter(stones)

    for i in range(times):
        start_time = time.time()
        print(f"Starting transform {i}, len(stones)={len(stones)}")
        stones_dict = transform(stones_dict)
        duration = time.time() - start_time
        durations.append(duration)
        total_duration = time.time() - total_start

        if len(durations) >= 3:
            x = np.array(range(len(durations)))
            y = np.array(durations)
            # Fit logarithmic curve: y = a * log(x) + b
            a, b = np.polyfit(np.log(x + 1), y, 1)
            
            # Estimate total time for all iterations
            estimated_total = a * np.log(times + 1) + b * times
            remaining = estimated_total - total_duration
            print(f"Transform {i} took {duration:.2f}s. Total: {total_duration:.2f}s. Est. remaining: {remaining:.2f}s ({remaining/3600:.1f}h)")
        else:
            print(f"Transform {i} took {duration:.2f}s. Total: {total_duration:.2f}s")

    return stones_dict.total()

def test_sample_data():
    # Given test from the prompt:
    # Initial: 0 1 10 99 999
    # After 1 blink:
    # should become: 1 2024 1 0 9 9 2021976
    stones = TEST_DATA.split()
    stones = blink(stones, 1)
    expected = ["1", "2024", "1", "0", "9", "9", "2021976"]
    assert stones == len(expected), f"Test failed! Got {stones}, expected {expected}"

    # Additional tests from the prompt examples:
    # Initial: 125 17
    # After 1 blink: 253000 1 7
    # After 2 blinks: 253 0 2024 14168
    # After 3 blinks: 512072 1 20 24 28676032
    # After 4 blinks: 512 72 2024 2 0 2 4 2867 6032
    stones = ["125", "17"]
    stones = blink(stones, 1)
    expected = ["253000","1","7"]
    assert stones == len(expected), f"After 1 blink got {stones}, expected {expected}"

    stones = ["125", "17"]
    stones = blink(stones, 2)
    expected = ["253","0","2024","14168"]
    assert stones == len(expected), f"After 2 blinks got {stones}, expected {expected}"

    stones = ["125", "17"]
    stones = blink(stones, 3)
    expected = ["512072","1","20","24","28676032"]
    assert stones == len(expected), f"After 3 blinks got {stones}, expected {expected}"

    stones = ["125", "17"]
    stones = blink(stones, 4)
    expected = ["512","72","2024","2","0","2","4","2867","6032"]
    assert stones == len(expected), f"After 4 blinks got {stones}, expected {expected}"

    # They mentioned that after 25 blinks starting with ["125","17"], number of stones = 55312
    stones = ["125", "17"]
    stones = blink(stones, 25)
    assert stones == 55312, f"After 25 blinks got {len(stones)} stones, expected 55312"

def solve_real_data(stones, blinks=25):
    # Blink 25 times
    stones = blink(stones, blinks)
    return stones

if __name__ == "__main__":
    test_sample_data()
    # Solve real puzzle data
    # Replace 'day' with the actual day number for the puzzle
    day = 11
    puzzle = Puzzle(2024, day)
    stones = puzzle.input_data.strip().split()

    p1 = solve_real_data(stones)
    puzzle.answer_a = p1

    p2 = solve_real_data(stones, 75)
    puzzle.answer_b = p2

