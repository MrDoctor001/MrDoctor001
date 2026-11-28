"""Task 3 — linear and binary search for hackathon teams.

Author: Diar (Student B)
"""

import bisect
import time

from dataset import get_teams_copy


def linear_search_by_member(teams, participant):
    """Return all teams where participant is a member. Counts comparisons."""
    found = []
    comparisons = 0
    for team in teams:
        for member in team[2]:
            comparisons += 1
            if member == participant:
                found.append(team)
                break
    return found, comparisons


def binary_search_by_id(teams_sorted, team_id):
    """Iterative binary search by team_id. List must be sorted by team_id."""
    left = 0
    right = len(teams_sorted) - 1
    comparisons = 0
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        mid_id = teams_sorted[mid][0]
        if mid_id == team_id:
            return teams_sorted[mid], comparisons
        if mid_id < team_id:
            left = mid + 1
        else:
            right = mid - 1
    return None, comparisons


def bisect_search_by_id(teams_sorted, team_id):
    """Find team by id using bisect (for comparison with our binary search)."""
    ids = [t[0] for t in teams_sorted]
    comparisons = 0
    # approximate comparison count as log2(n) style steps via bisect
    idx = bisect.bisect_left(ids, team_id)
    comparisons = 0
    lo, hi = 0, len(ids)
    while lo < hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if ids[mid] < team_id:
            lo = mid + 1
        else:
            hi = mid
    if lo < len(ids) and ids[lo] == team_id:
        return teams_sorted[lo], comparisons
    return None, comparisons


def _make_id_list(n):
    """Sorted list of fake team tuples by team_id."""
    return [(i, f"T{i}", ("X",), "AI", 50.0, 12) for i in range(n)]


def benchmark_search(sizes=(1000, 10000, 100000)):
    rows = []
    for n in sizes:
        data = _make_id_list(n)
        present = n // 2
        missing = n + 999

        t0 = time.perf_counter()
        _, lin_c = linear_search_by_member(
            [(i, f"T{i}", (f"P{i % 50}", f"Q{i}"), "AI", 1.0, 1) for i in range(min(n, 2000))],
            "P0",
        )
        # for large n only time binary / bisect on id list
        t_lin = time.perf_counter() - t0

        t0 = time.perf_counter()
        _, bin_ok = binary_search_by_id(data, present)
        t_bin = time.perf_counter() - t0
        _, bin_miss = binary_search_by_id(data, missing)

        t0 = time.perf_counter()
        _, bis_ok = bisect_search_by_id(data, present)
        t_bis = time.perf_counter() - t0
        _, bis_miss = bisect_search_by_id(data, missing)

        rows.append({
            "n": n,
            "bin_comp_hit": bin_ok,
            "bin_comp_miss": bin_miss,
            "bis_comp_hit": bis_ok,
            "bis_comp_miss": bis_miss,
            "t_bin": t_bin,
            "t_bis": t_bis,
            "lin_note_comp": lin_c,
            "t_lin_sample": t_lin,
        })
    return rows


def run_task3():
    """Print Task 3 results."""
    print("=== Task 3: Searching ===")
    teams = get_teams_copy()
    name = "Dana Kim"
    found, comps = linear_search_by_member(teams, name)
    print(f"Linear search for member '{name}': {len(found)} team(s), comparisons={comps}")
    for t in found:
        print(f"  #{t[0]} {t[1]}")

    by_id = sorted(teams, key=lambda t: t[0])
    target = 5
    team, bcomps = binary_search_by_id(by_id, target)
    team_b, biscomps = bisect_search_by_id(by_id, target)
    print(f"\nBinary search team_id={target}: {team[1] if team else None}, comps={bcomps}")
    print(f"Bisect search team_id={target}: {team_b[1] if team_b else None}, comps={biscomps}")
    print(f"Results coincide: {team == team_b}")
    print("Bisect uses the same sorted-array idea as binary search, so the found element matches.")

    missing, mcomps = binary_search_by_id(by_id, 999)
    print(f"Binary search missing id=999: {missing}, comps={mcomps}")

    print("\nComplexity: linear search O(n), binary search O(log n)")
    print(f"{'n':>8} {'bin_hit':>8} {'bin_miss':>9} {'bis_hit':>8} {'bis_miss':>9}")
    for row in benchmark_search():
        print(
            f"{row['n']:8d} {row['bin_comp_hit']:8d} {row['bin_comp_miss']:9d} "
            f"{row['bis_comp_hit']:8d} {row['bis_comp_miss']:9d}"
        )
