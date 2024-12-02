import torch
import time
from aocd.models import Puzzle

def main():
    puzzle = Puzzle(year=2024, day=1)
    data = puzzle.input_data

    device = torch.device('cpu')

    left_list = []
    right_list = []

    for line in data.strip().split('\n'):
        left_num_str, right_num_str = line.strip().split()
        left_list.append(int(left_num_str))
        right_list.append(int(right_num_str))

    total_distance, similarity_score = day1(device, left_list, right_list)

    print("Part 1 total distance:", total_distance)
    puzzle.answer_a = total_distance

    print("Part 2 similarity score:", similarity_score)
    puzzle.answer_b = similarity_score

def benchmark(device, left_list, right_list, runs=5):
    times = []
    for _ in range(runs):
        start_time = time.perf_counter()
        similarity_score = day1(device, left_list, right_list)
        if device.type == 'mps':
            torch.mps.synchronize()
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    average_time = sum(times) / runs
    return similarity_score, average_time

def day1(device, left_list, right_list):
    left_tensor = torch.tensor(left_list, device=device)
    right_tensor = torch.tensor(right_list, device=device)

    left_sorted, _ = torch.sort(left_tensor)
    right_sorted, _ = torch.sort(right_tensor)

    differences = torch.abs(left_sorted - right_sorted)

    total_distance = torch.sum(differences).item()

    left_expanded = left_tensor.unsqueeze(1) 
    right_expanded = right_tensor.unsqueeze(0)

    comparison_matrix = left_expanded == right_expanded 
    counts = comparison_matrix.sum(dim=1)

    similarity_score = (left_tensor * counts).sum().item()

    return total_distance, similarity_score

if __name__ == "__main__":
    main()
