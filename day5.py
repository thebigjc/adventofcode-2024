from aocd.models import Puzzle

TEST_DATA = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def parse_input(data):
    rules_section, updates_section = data.strip().split("\n\n")
    rules = []
    for line in rules_section.strip().splitlines():
        a, b = line.strip().split("|")
        rules.append((int(a), int(b)))
    updates = []
    for line in updates_section.strip().splitlines():
        pages = list(map(int, line.strip().split(",")))
        updates.append(pages)
    return rules, updates


def is_update_correct(rules, update):
    position = {page: idx for idx, page in enumerate(update)}
    # Only consider rules where both pages are in the update
    relevant_rules = [(a, b) for a, b in rules if a in position and b in position]
    for a, b in relevant_rules:
        if position[a] >= position[b]:
            return False
    return True


def get_middle_page(update):
    mid_index = len(update) // 2
    return update[mid_index]


def reorder_update(rules, update):
    # Build the graph
    graph = {}
    in_degree = {}
    for page in update:
        graph[page] = []
        in_degree[page] = 0

    update_set = set(update)
    for a, b in rules:
        if a in update_set and b in update_set:
            graph[a].append(b)
            in_degree[b] += 1

    # Kahn's algorithm with priority queue (sort nodes in reverse order)
    # to match the expected reordering
    queue = [page for page in update if in_degree[page] == 0]
    queue.sort(reverse=True)  # Higher page numbers first
    sorted_update = []
    while queue:
        node = queue.pop(0)
        sorted_update.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
        queue.sort(reverse=True)
    if len(sorted_update) != len(update):
        raise Exception("Cycle detected in the rules!")
    return sorted_update


def solve(data):
    rules, updates = parse_input(data)
    total_part1 = 0
    total_part2 = 0
    for update in updates:
        if is_update_correct(rules, update):
            # Part 1: Correctly ordered updates
            middle_page = get_middle_page(update)
            total_part1 += middle_page
        else:
            # Part 2: Incorrectly ordered updates, reorder them
            sorted_update = reorder_update(rules, update)
            middle_page = get_middle_page(sorted_update)
            total_part2 += middle_page
    return total_part1, total_part2


# Test cases
total_p1, total_p2 = solve(TEST_DATA)
assert total_p1 == 143, f"Expected Part 1 total 143, got {total_p1}"
assert total_p2 == 123, f"Expected Part 2 total 123, got {total_p2}"
print("All test cases passed!")

# Solve the real puzzle
puzzle = Puzzle(2024, 5)
data = puzzle.input_data

# Solve the puzzle
total_part1, total_part2 = solve(data)
print("Part 1 Solution:", total_part1)
print("Part 2 Solution:", total_part2)

# Submit the answers
puzzle.answer_a = total_part1
puzzle.answer_b = total_part2
