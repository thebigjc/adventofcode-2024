from aocd.models import Puzzle

TEST_DATA = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def solve_part1(data, word="XMAS"):
    grid = data.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    count = 0

    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]

    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                found = True
                for i in range(len(word)):
                    nr, nc = r + dr * i, c + dc * i
                    if not (
                        0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == word[i]
                    ):
                        found = False
                        break
                if found:
                    count += 1

    return count


def solve_part2(data, word="MAS"):
    grid = [list(line) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    count = 0

    arms = [word, word[::-1]]

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != "A":
                continue
            for arm1 in arms:
                for arm2 in arms:
                    if (
                        grid[r - 1][c - 1] == arm1[0]
                        and grid[r][c] == arm1[1]
                        and grid[r + 1][c + 1] == arm1[2]
                    ):
                        if (
                            grid[r - 1][c + 1] == arm2[0]
                            and grid[r][c] == arm2[1]
                            and grid[r + 1][c - 1] == arm2[2]
                        ):
                            count += 1
    return count


# Test cases
assert solve_part1(TEST_DATA) == 18
assert solve_part2(TEST_DATA) == 9

# Solve the real puzzle
puzzle = Puzzle(2024, 4)
data = puzzle.input_data

solution_part1 = solve_part1(data)
print("Part 1 Solution:", solution_part1)
puzzle.answer_a = solution_part1

# Solve Part Two
solution_part2 = solve_part2(data)
print("Part 2 Solution:", solution_part2)
puzzle.answer_b = solution_part2
