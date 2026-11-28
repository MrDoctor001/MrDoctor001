"""Task 7 — debugging and optimizing common team_id lookup.

Author: Diar (Student A / Student B)
"""

import random
import time


def common_team_ids_buggy(list1, list2):
    """Buggy + inefficient version.

    Intended: return team_id values present in BOTH lists.
    Bug: uses `or` / wrong flag so ids that appear only in list1
    still get appended. Also nested loops -> O(n*m).
    """
    result = []
    for id1 in list1:
        found = False
        for id2 in list2:
            if id1 == id2:
                found = True
                break
        # logical error: should be `if found`
        if not found:
            result.append(id1)
    return result


def common_team_ids(list1, list2):
    """Optimized: intersection via set. Average O(n + m)."""
    return list(set(list1) & set(list2))


def measure_both(sizes=(1000, 2000, 5000)):
    rows = []
    for n in sizes:
        a = [random.randint(1, n * 2) for _ in range(n)]
        b = [random.randint(1, n * 2) for _ in range(n)]

        t0 = time.perf_counter()
        common_team_ids_buggy(a, b)
        t_bug = time.perf_counter() - t0

        t0 = time.perf_counter()
        common_team_ids(a, b)
        t_opt = time.perf_counter() - t0

        rows.append({"n": n, "buggy_s": t_bug, "optimized_s": t_opt})
    return rows


def debug_demo():
    """Show the bug with print-debugging on a small example."""
    print("=== Task 7: Debug & Optimize ===")
    a = [1, 2, 3, 4, 5]
    b = [3, 4, 6, 7]
    print(f"list1 = {a}")
    print(f"list2 = {b}")
    print(f"buggy result:     {common_team_ids_buggy(a, b)}")
    print(f"expected (1..):   {[x for x in a if x in b]}")
    print(f"optimized result: {sorted(common_team_ids(a, b))}")
    print()
    print("Debugging notes:")
    print("  Printed found flag for each id1 — saw found=True for 3 and 4,")
    print("  but they were NOT appended because of `if not found`.")
    print("  Fixed condition to membership check via set intersection.")
    print("  Complexity: buggy O(n*m), optimized O(n+m) average.")
    print()
    print(f"{'n':>6} {'buggy (s)':>12} {'optimized (s)':>14}")
    for row in measure_both():
        print(f"{row['n']:6d} {row['buggy_s']:12.6f} {row['optimized_s']:14.6f}")
