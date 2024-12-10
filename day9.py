from aocd.models import Puzzle

SAMPLE_DATA = "2333133121414131402"


def parse_disk_map(data):
    # Parse the input string into alternating file/free lengths
    # Digits alternate between file-length and free-length.
    # If there's an odd number of digits, the last one is just a file-length with no trailing free.
    lengths = [int(x) for x in data]
    disk = []
    file_id = 0
    is_file = True
    i = 0
    while i < len(lengths):
        if is_file:
            # file length
            flen = lengths[i]
            disk.extend([str(file_id)] * flen)
            file_id += 1
            i += 1
        else:
            # free length
            freelen = lengths[i]
            disk.extend(["."] * freelen)
            i += 1
        is_file = not is_file
    return disk


def compact_disk(disk):
    # The process:
    # Move file blocks one at a time from the end of the disk to the leftmost free space block,
    # until there are no gaps ('.') remaining between file blocks.
    # A gap is defined as a '.' that appears before at least one file block to its right.

    # Find the initial rightmost file block
    rightmost_file_index = len(disk) - 1
    while rightmost_file_index >= 0 and disk[rightmost_file_index] == ".":
        rightmost_file_index -= 1

    # Maintain a list of indices for dots
    dot_indices = [i for i, c in enumerate(disk) if c == "."]

    while rightmost_file_index > 0 and dot_indices:
        # Find the first '.' that has a file block to its right
        dot_index = -1
        for idx in dot_indices:
            if idx < rightmost_file_index:
                dot_index = idx
                break

        if dot_index == -1:
            # No suitable '.' found, we are done
            break

        # Move the rightmost file block to the '.' position
        disk[dot_index] = disk[rightmost_file_index]
        disk[rightmost_file_index] = "."

        # Update the rightmost file index
        rightmost_file_index -= 1
        while rightmost_file_index >= 0 and disk[rightmost_file_index] == ".":
            rightmost_file_index -= 1

        # Update the list of dot indices
        dot_indices.remove(dot_index)
        dot_indices.append(rightmost_file_index)

    return disk


def find_file_spans(disk):
    """
    Find the spans (start, length) of each file in the disk.
    Returns a list of tuples (file_id, start_pos, length).
    """
    spans = []
    file_id = None
    span_start = None

    for i, c in enumerate(disk):
        if c == ".":
            if file_id is not None:
                # End of a file span
                spans.append((file_id, span_start, i - span_start))
                file_id = None
        else:
            if file_id != int(c):
                if file_id is not None:
                    # End of previous file span
                    spans.append((file_id, span_start, i - span_start))
                # Start of new file span
                file_id = int(c)
                span_start = i

    # Handle last span if it exists
    if file_id is not None:
        spans.append((file_id, span_start, len(disk) - span_start))

    return spans


def find_free_spans(disk):
    """Find spans of free space (start position and length)."""
    free_spans = []
    span_start = None

    for i, c in enumerate(disk):
        if c == ".":
            if span_start is None:
                span_start = i
        else:
            if span_start is not None:
                free_spans.append((span_start, i - span_start))
                span_start = None

    # Handle last span if it exists
    if span_start is not None:
        free_spans.append((span_start, len(disk) - span_start))

    return free_spans


def compact_disk_part2(disk):
    """
    Compact the disk by moving whole files to the leftmost possible position.
    Process files in order of decreasing file ID.
    """
    # Convert disk to list for modification
    disk = list(disk)

    # Get file spans and sort by file ID in descending order
    file_spans = find_file_spans(disk)
    file_spans.sort(key=lambda x: x[0], reverse=True)

    for file_id, start_pos, length in file_spans:
        # Find all free spans
        free_spans = find_free_spans(disk)

        # Find leftmost free span that can fit this file
        target_span = None
        for free_start, free_length in free_spans:
            if free_length >= length and free_start < start_pos:
                target_span = (free_start, free_length)
                break

        if target_span is not None:
            # Move the file to the new position
            file_content = disk[start_pos : start_pos + length]
            # Clear old position
            disk[start_pos : start_pos + length] = ["."] * length
            # Place file in new position
            disk[target_span[0] : target_span[0] + length] = file_content

    return disk


def compute_checksum(disk):
    # sum of (position * file_id) for each file block
    total = 0
    for pos, c in enumerate(disk):
        if c != ".":
            file_id = int(c)
            total += pos * file_id
    return total


def solve(data):
    print("Parsing disk map")
    disk = parse_disk_map(data)

    # Solve Part 1
    print("Compacting disk (Part 1)")
    disk_p1 = compact_disk(disk.copy())
    checksum_p1 = compute_checksum(disk_p1)

    # Solve Part 2
    print("Compacting disk (Part 2)")
    disk_p2 = compact_disk_part2(disk.copy())
    checksum_p2 = compute_checksum(disk_p2)

    return checksum_p1, checksum_p2


# Test with the sample data
SAMPLE_DATA = "2333133121414131402"
expected_sample_checksum_p1 = 1928
expected_sample_checksum_p2 = 2858

sample_p1, sample_p2 = solve(SAMPLE_DATA)
assert (
    sample_p1 == expected_sample_checksum_p1
), f"Part 1: got {sample_p1}, expected {expected_sample_checksum_p1}"
assert (
    sample_p2 == expected_sample_checksum_p2
), f"Part 2: got {sample_p2}, expected {expected_sample_checksum_p2}"
print("Sample tests passed.")
puzzle = Puzzle(2024, 9)
data = puzzle.input_data.strip()
p1, p2 = solve(data)

puzzle.answer_a = p1
puzzle.answer_b = p2
