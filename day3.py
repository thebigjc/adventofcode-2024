import re
from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=3)

def solve(data, part2=False):
    s = 0
    ok = True
    for i in re.findall(r'(mul|do|don\'t)\((\d*),?(\d*)\)', data):
        if part2:
            if i[0] == 'do': ok = True
            if i[0] == 'don\'t': ok = False
            if i[0] == 'mul' and ok: s += int(i[1]) * int(i[2] or 1)
        else:
            if i[0] == 'mul': s += int(i[1]) * int(i[2] or 1)

    return s

p1 = solve(puzzle.input_data)
print("Part 1:", p1)
puzzle.answer_a = p1

p2 = solve(puzzle.input_data, True)
print("Part 2:", p2)
puzzle.answer_b = p2