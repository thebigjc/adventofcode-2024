TEST_INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

TEST_INPUT_2 = """T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
.........."""

import numpy as np


def parse_map(data):
    lines = data.strip("\n").split("\n")
    antennas = []
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch != "." and ch != "#":
                # This is an antenna with frequency ch
                antennas.append((ch, y, x))
    return lines, antennas


def find_collinear_points(p1, p2, max_y, max_x):
    y1, x1 = p1
    y2, x2 = p2

    y_coords, x_coords = np.meshgrid(np.arange(max_y), np.arange(max_x), indexing="ij")
    points = np.stack([y_coords, x_coords], axis=-1).reshape(-1, 2)

    v1 = np.array([y2 - y1, x2 - x1, 0])
    v2 = np.column_stack([points - np.array([y1, x1]), np.zeros(len(points))])

    cross_products = np.cross(v1, v2)

    collinear_mask = np.all(np.abs(cross_products) < 1e-10, axis=1)
    collinear_points = points[collinear_mask]

    return {tuple(point) for point in collinear_points}


def find_antinodes(lines, antennas):
    freq_dict = {}
    for f, y, x in antennas:
        freq_dict.setdefault(f, []).append((y, x))

    max_y = len(lines)
    max_x = len(lines[0])
    antinode_set_1 = set()
    antinode_set_2 = set()

    for f, coords in freq_dict.items():
        n = len(coords)
        if n < 2:
            continue

        for i in range(n):
            y1, x1 = coords[i]
            p1 = (y1, x1)

            for j in range(i + 1, n):
                y2, x2 = coords[j]
                p2 = (y2, x2)

                C1y, C1x = (2 * y1 - y2), (2 * x1 - x2)
                C2y, C2x = (2 * y2 - y1), (2 * x2 - x1)

                if 0 <= C1y < max_y and 0 <= C1x < max_x:
                    antinode_set_1.add((C1y, C1x))
                if 0 <= C2y < max_y and 0 <= C2x < max_x:
                    antinode_set_1.add((C2y, C2x))

                collinear = find_collinear_points(p1, p2, max_y, max_x)
                antinode_set_2.update(collinear)

    return antinode_set_1, antinode_set_2


def test_with_sample_data():
    lines, antennas = parse_map(TEST_INPUT)

    antinodes_p1, antinodes_p2 = find_antinodes(lines, antennas)
    assert len(antinodes_p1) == 14, f"Part 1: Expected 14, got {len(antinodes_p1)}"
    assert len(antinodes_p2) == 34, f"Part 2: Expected 34, got {len(antinodes_p2)}"

    lines2, antennas2 = parse_map(TEST_INPUT_2)
    _, antinodes_p2_2 = find_antinodes(lines2, antennas2)
    assert len(antinodes_p2_2) == 9, f"Part 2: Expected 9, got {len(antinodes_p2_2)}"


def solve_real_data():
    from aocd.models import Puzzle

    puzzle = Puzzle(2024, 8)
    data = puzzle.input_data

    lines, antennas = parse_map(data)

    antinodes_p1, antinodes_p2 = find_antinodes(lines, antennas)
    p1 = len(antinodes_p1)
    print("Part 1:", p1, "antinodes")
    puzzle.answer_a = p1
    p2 = len(antinodes_p2)
    print("Part 2:", p2, "antinodes")
    puzzle.answer_b = p2


if __name__ == "__main__":
    test_with_sample_data()
    solve_real_data()
