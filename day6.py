from aocd.models import Puzzle
import threading
import sys
import sysconfig

SAMPLE_DATA = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

DIRS = {"^": 0, ">": 1, "v": 2, "<": 3}
DR = [-1, 0, 1, 0]
DC = [0, 1, 0, -1]


def parse_grid(input_data):
    grid = [list(line) for line in input_data.strip("\n").split("\n")]
    start_pos = None
    start_dir = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val in "^v<>":
                start_pos = (r, c)
                start_dir = DIRS[val]
                grid[r][c] = "."  # Replace guard symbol with floor
                return grid, start_pos, start_dir
    raise ValueError("No guard start found")


def can_move_forward(grid, rows, cols, r, c, d):
    nr = r + DR[d]
    nc = c + DC[d]
    if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
        return None
    return grid[nr][nc] != "#"


def turn_right(d):
    # 0=up,1=right,2=down,3=left
    return (d + 1) % 4


def simulate_no_obstacle(grid, start_pos, start_dir):
    rows, cols = len(grid), len(grid[0])
    r, c = start_pos
    d = start_dir
    visited = set()
    visited.add((r, c))
    moves = []

    while True:
        forward_status = can_move_forward(grid, rows, cols, r, c, d)
        if forward_status is None:
            break
        if forward_status is False:
            d = turn_right(d)
            continue

        r += DR[d]
        c += DC[d]
        moves.append((r, c))
        visited.add((r, c))

    return len(visited), moves


def encode_state(r, c, d, cols):
    return (r * cols + c) * 4 + d


def simulate_with_loop_detection(grid, start_pos, start_dir, obstacle_cell):
    rows, cols = len(grid), len(grid[0])
    r, c = start_pos
    d = start_dir
    total_states = rows * cols * 4
    visited = [False] * (total_states)

    while True:
        s = encode_state(r, c, d, cols)
        if visited[s]:
            # Loop detected
            return True
        visited[s] = True

        # Attempt forward
        nr = r + DR[d]
        nc = c + DC[d]
        # Check bounds
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            # Leaves map
            return False
        # Check obstacle
        if (nr, nc) == obstacle_cell or grid[nr][nc] == "#":
            # Turn right
            d = turn_right(d)
            continue
        # Move forward
        r, c = nr, nc


def worker(grid, start_pos, start_dir, candidate_cells_chunk, result_list, index):
    count = 0
    for cell in candidate_cells_chunk:
        if cell == start_pos:
            continue
        if simulate_with_loop_detection(grid, start_pos, start_dir, cell):
            count += 1
    result_list[index] = count


def solve_part2_parallel(input_data, num_threads=10):
    grid, start_pos, start_dir = parse_grid(input_data)
    _, moves = simulate_no_obstacle(grid, start_pos, start_dir)
    candidate_cells = list(set(moves))

    chunk_size = (len(candidate_cells) + num_threads - 1) // num_threads
    chunks = [
        candidate_cells[i : i + chunk_size]
        for i in range(0, len(candidate_cells), chunk_size)
    ]

    results = [0] * len(chunks)
    threads = []

    for i, chunk in enumerate(chunks):
        t = threading.Thread(
            target=worker, args=(grid, start_pos, start_dir, chunk, results, i)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)


def solve_part1(input_data):
    grid, start_pos, start_dir = parse_grid(input_data)
    visited_count, _ = simulate_no_obstacle(grid, start_pos, start_dir)
    return visited_count


def solve_part2(input_data):
    grid, start_pos, start_dir = parse_grid(input_data)
    _, moves = simulate_no_obstacle(grid, start_pos, start_dir)

    candidate_cells = set(moves)
    loop_count = 0

    # Just check each candidate cell by simulating from scratch:
    for cell in candidate_cells:
        if cell == start_pos:
            continue
        if simulate_with_loop_detection(grid, start_pos, start_dir, cell):
            loop_count += 1

    return loop_count


if __name__ == "__main__":
    py_version = float(".".join(sys.version.split()[0].split(".")[0:2]))
    status = sysconfig.get_config_var("Py_GIL_DISABLED")

    if py_version >= 3.13:
        status = sys._is_gil_enabled()
    if status is None:
        print("GIL cannot be disabled for Python version <= 3.12")
    if status == 0:
        print("GIL is currently disabled")
    if status == 1:
        print("GIL is currently active")

    # Test sample
    sample_p1 = solve_part1(SAMPLE_DATA)
    print("Sample Part 1:", sample_p1)
    assert sample_p1 == 41

    sample_p2 = solve_part2_parallel(SAMPLE_DATA)
    print("Sample Part 2:", sample_p2)
    assert sample_p2 == 6

    puzzle = Puzzle(2024, 6)
    real_data = puzzle.input_data
    p1 = solve_part1(real_data)
    print("Part 1 (real):", p1)
    puzzle.answer_a = p1

    p2 = solve_part2_parallel(real_data)
    print("Part 2 (real):", p2)
    puzzle.answer_b = p2
