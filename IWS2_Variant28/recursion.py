"""Task 4 — recursive algorithms for team combinations and max score.

Author: Diar (Student A)
"""

import sys
import time

from dataset import get_teams_copy


def combinations_recursive(names, k):
    """All teams of k participants from names (recursive).

    Base cases: k == 0 -> one empty team; k > len(names) or k < 0 -> none.
    Recursive case: teams with names[0] + teams without names[0].
    """
    if k == 0:
        return [()]
    if k < 0 or k > len(names):
        return []
    if not names:
        return []

    first = names[0]
    rest = names[1:]
    with_first = []
    for combo in combinations_recursive(rest, k - 1):
        with_first.append((first,) + combo)
    without_first = combinations_recursive(rest, k)
    return with_first + without_first


def combinations_iterative(names, k):
    """Iterative version of combinations (same result as recursive)."""
    if k < 0 or k > len(names):
        return []
    if k == 0:
        return [()]
    result = [()]
    for _ in range(k):
        new_result = []
        for combo in result:
            start = names.index(combo[-1]) + 1 if combo else 0
            for i in range(start, len(names)):
                new_result.append(combo + (names[i],))
        result = new_result
    return result


def max_score_team(teams):
    """Recursive: team with maximum score.

    Base case: one team left (or empty).
    Recursive case: compare first team with max of the rest.
    """
    if not teams:
        return None
    if len(teams) == 1:
        return teams[0]
    rest_best = max_score_team(teams[1:])
    if teams[0][4] >= rest_best[4]:
        return teams[0]
    return rest_best


def demo_recursion_limit():
    """Show RecursionError and handle it."""
    def deep(n):
        if n == 0:
            return 0
        return 1 + deep(n - 1)

    old_limit = sys.getrecursionlimit()
    print(f"Current recursion limit: {old_limit}")
    try:
        # force a deep call beyond the limit
        deep(old_limit + 50)
    except RecursionError as e:
        print(f"Caught RecursionError: {e}")
    else:
        print("Unexpected: no RecursionError")
    finally:
        print("Recursion demo finished (limit unchanged).")


def run_task4():
    """Print Task 4 results."""
    print("=== Task 4: Recursion ===")
    names = ["Arman", "Dana", "Ilya", "Sara", "Timur"]
    k = 3

    t0 = time.perf_counter()
    rec = combinations_recursive(names, k)
    t_rec = time.perf_counter() - t0

    t0 = time.perf_counter()
    it = combinations_iterative(names, k)
    t_it = time.perf_counter() - t0

    print(f"Combinations of {k} from {names}:")
    print(f"  recursive: {len(rec)} teams, time={t_rec:.6f}s")
    print(f"  iterative: {len(it)} teams, time={t_it:.6f}s")
    print(f"  results equal: {set(rec) == set(it)}")
    for c in rec[:5]:
        print(f"    {c}")
    if len(rec) > 5:
        print(f"    ... ({len(rec) - 5} more)")

    best = max_score_team(get_teams_copy())
    print(f"\nMax score team (recursive): {best[1]} score={best[4]}")

    print()
    demo_recursion_limit()
