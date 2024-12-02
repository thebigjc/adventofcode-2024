import torch
from typing import List, Sequence
from aocd.models import Puzzle

# Constants
MIN_DIFFERENCE = 1
MAX_DIFFERENCE = 3
MIN_LEVELS = 2


def is_safe(levels: Sequence[int]) -> bool:
    """
    Check if a sequence of levels is safe according to the rules.
    A sequence is safe if all differences between consecutive numbers:
    - Are non-zero
    - Have the same sign (all increasing or decreasing)
    - Are between 1 and 3 inclusive
    """
    levels = torch.tensor(levels)
    differences = levels[1:] - levels[:-1]

    # Check for zero differences (unsafe)
    if torch.any(differences == 0):
        return False

    # Check if all differences have the same sign
    signs = torch.sign(differences)
    if torch.all(signs == 1) or torch.all(signs == -1):
        abs_differences = torch.abs(differences)
        return torch.all(
            (abs_differences >= MIN_DIFFERENCE) & (abs_differences <= MAX_DIFFERENCE)
        ).item()
    return False


def solve_part_a(reports: List[List[int]]) -> int:
    """Solve part A: Count reports that are naturally safe."""
    return sum(1 for report in reports if is_safe(report))


def solve_part_b(reports: List[List[int]]) -> int:
    """
    Solve part B: Count reports that are either naturally safe
    or can become safe by removing one number.
    """
    safe_count = 0

    for report in reports:
        if is_safe(report):
            safe_count += 1
        else:
            # Try removing each level
            for i in range(len(report)):
                modified_report = report[:i] + report[i + 1 :]
                if len(modified_report) >= MIN_LEVELS and is_safe(modified_report):
                    safe_count += 1
                    break

    return safe_count


def main():
    # Fetch puzzle input
    puzzle = Puzzle(year=2024, day=2)
    reports = [
        [int(x) for x in line.strip().split()]
        for line in puzzle.input_data.strip().split("\n")
    ]

    # Solve and submit answers
    answer_a = solve_part_a(reports)
    answer_b = solve_part_b(reports)

    print(f"Part A: {answer_a}")
    print(f"Part B: {answer_b}")

    puzzle.answer_a = answer_a
    puzzle.answer_b = answer_b


if __name__ == "__main__":
    main()
