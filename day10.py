# We will use a constant string for test data as requested.
# We'll use one of the given examples for testing. Let's choose the large example mentioned in the problem:
#
# Example input:
# 89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732
#
# For this example:
#   - There are 9 trailheads.
#   - Their scores (part one) in reading order sum to 36.
#   - Their ratings (part two) in reading order sum to 81.
#
# We will test against this data to ensure correctness.
#
# After confirming that the code works for this test data, we will also fetch the real data using the Puzzle API
# and submit the answers.

TEST_DATA = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def solve(grid):
    # grid: list of strings, each string a row of digits
    # Convert to 2D list of ints
    heightmap = [list(map(int, list(row))) for row in grid]
    rows = len(heightmap)
    cols = len(heightmap[0])

    # Identify all trailheads (cells with height 0)
    trailheads = [
        (r, c) for r in range(rows) for c in range(cols) if heightmap[r][c] == 0
    ]

    # For each trailhead, we want two things:
    # 1) Score: the count of distinct 9 positions reachable by a valid hiking trail.
    # 2) Rating: the total count of distinct trails leading to all 9 positions from that trailhead.

    # A hiking trail is a path starting at height 0 and each step moves to a cell of height exactly h+1,
    # no diagonal moves. The path ends at height 9.

    # We'll implement a DP approach:
    # For each trailhead, we compute the number of ways to reach each cell that follows the ascending pattern.
    # Then score = number of 9-cells that have at least one way.
    # rating = sum of ways to all 9-cells.

    # To do this efficiently for each trailhead:
    # We'll do a BFS/DP layer by layer from height 0 up to 9.

    def neighbors(r, c):
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc

    total_score = 0
    total_rating = 0

    for sr, sc in trailheads:
        # DP array: ways[r][c] = number of ways to reach (r,c) from this trailhead
        ways = [[0] * cols for _ in range(rows)]
        if heightmap[sr][sc] != 0:
            # Not a valid trailhead after all
            continue
        ways[sr][sc] = 1

        # Process cells in order of heights: from 0 up to 8 to find next steps of height+1
        for h in range(9):  # from height h to h+1
            # Find all cells of height h that are reachable
            h_cells = [
                (r, c)
                for r in range(rows)
                for c in range(cols)
                if heightmap[r][c] == h and ways[r][c] > 0
            ]
            for r, c in h_cells:
                # Try to move to cells of height h+1
                for nr, nc in neighbors(r, c):
                    if heightmap[nr][nc] == h + 1:
                        ways[nr][nc] += ways[r][c]

        # After filling ways up to height 9:
        # score: how many distinct 9-cells have ways > 0
        # rating: sum of ways for all 9-cells
        score = 0
        rating = 0
        for r in range(rows):
            for c in range(cols):
                if heightmap[r][c] == 9 and ways[r][c] > 0:
                    score += 1
                    rating += ways[r][c]

        total_score += score
        total_rating += rating

    return total_score, total_rating


def test_static_data():
    test_grid = TEST_DATA.strip().split("\n")
    score, rating = solve(test_grid)
    # According to the puzzle statement for this data:
    # sum of scores = 36
    # sum of ratings = 81
    assert score == 36, f"Expected score=36, got {score}"
    assert rating == 81, f"Expected rating=81, got {rating}"
    print("Test data passed!")


if __name__ == "__main__":
    # Test against static data
    test_static_data()

    # Now solve the real puzzle input
    from aocd.models import Puzzle

    day = 10
    puzzle = Puzzle(year=2024, day=day)
    real_data = puzzle.input_data.strip().split("\n")
    p1, p2 = solve(real_data)

    print("Part 1:", p1)
    print("Part 2:", p2)

    # Submit answers
    puzzle.answer_a = p1
    puzzle.answer_b = p2
