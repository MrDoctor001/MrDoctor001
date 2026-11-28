"""Task 2 — Bubble Sort for hackathon team ranking.

Author: Diar (Student A)
"""

import random
import time

from dataset import get_teams_copy


def team_key(team):
    """Sort key: score desc, then submission_hour asc."""
    return (-team[4], team[5])


def bubble_sort_teams(teams):
    """Bubble sort with early exit. Returns (sorted_list, comparisons, swaps)."""
    arr = list(teams)
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            # higher score first; if equal, earlier submission first
            left = arr[j]
            right = arr[j + 1]
            need_swap = False
            if left[4] < right[4]:
                need_swap = True
            elif left[4] == right[4] and left[5] > right[5]:
                need_swap = True
            if need_swap:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return arr, comparisons, swaps


def check_against_sorted(teams):
    """Compare bubble sort result with sorted()."""
    mine, comps, swaps = bubble_sort_teams(teams)
    reference = sorted(teams, key=team_key)
    return mine == reference, comps, swaps, mine


def random_team(i):
    return (i, f"T{i}", ("A", "B"), "AI", random.uniform(0, 100), random.randint(1, 24))


def benchmark_bubble(sizes=(10, 100, 1000)):
    """Run bubble sort on random lists and collect counters."""
    rows = []
    for size in sizes:
        data = [random_team(i) for i in range(size)]
        start = time.perf_counter()
        _, comps, swaps = bubble_sort_teams(data)
        elapsed = time.perf_counter() - start
        rows.append({
            "n": size,
            "comparisons": comps,
            "swaps": swaps,
            "seconds": elapsed,
        })
    return rows


def run_task2():
    """Print Task 2 results."""
    print("=== Task 2: Bubble Sort ===")
    teams = get_teams_copy()
    ok, comps, swaps, ranked = check_against_sorted(teams)
    print(f"Matches sorted(): {ok}")
    print(f"Comparisons: {comps}, swaps: {swaps}")
    print("Ranking (score desc, hour asc):")
    for t in ranked:
        print(f"  #{t[0]} {t[1]:20s} score={t[4]:5.1f} hour={t[5]}")

    print("\nComplexity of Bubble Sort:")
    print("  Best:    O(n) comparisons, O(1) swaps (already sorted + early exit)")
    print("  Average: O(n^2)")
    print("  Worst:   O(n^2)")
    print("  Space:   O(1) extra (in-place on the working copy)")

    print("\nBenchmark on random data:")
    print(f"{'n':>6} {'comparisons':>14} {'swaps':>10} {'seconds':>12}")
    for row in benchmark_bubble():
        print(f"{row['n']:6d} {row['comparisons']:14d} {row['swaps']:10d} {row['seconds']:12.6f}")
