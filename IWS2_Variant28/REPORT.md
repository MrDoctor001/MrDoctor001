# IWS №2 — Team Project Report

## 1. Project Title, Variant Number and Team Members

**Project title:** Hackathon Results Processing System  
**Variant:** 28 — Hackathon Results  

| Role | Full name | Group | Notes |
|------|-----------|-------|-------|
| Student A | Diar | SE-2401 | Tasks 1, 2, 4 |
| Student B | Diar | SE-2401 | Tasks 3, 5, 6 (solo project — both roles) |

Both students (same person in this submission) also worked on the shared dataset, Task 7, the text menu (`main.py`), combining modules, unit tests and this report.

---

## 2. Objective

To develop practical programming skills by creating a Python project that uses tuples, sets and dictionaries, implements sorting, searching and recursive algorithms with complexity analysis, applies OOP, works with files and exceptions, and is tested, debugged and optimized.

---

## 3. Problem Statement

**Common data set:** at least 12 hackathon teams. Each team is a tuple  
`(team_id, team_name, members, track, score, submission_hour)`,  
where `members` is a tuple of participant names. The same data is used in all tasks.

| Task | Statement |
|------|-----------|
| 1 | Represent teams as tuples; build `team_id → record` dictionary; with sets find unique participants, dual-team members (rule violation) and tracks with no submissions; with dictionaries compute average score per track and best team per track. |
| 2 | Implement Bubble Sort (early termination) by score descending, then submission_hour ascending; count comparisons/swaps; verify with `sorted()`; benchmark on 10 / 100 / 1000 elements; state Big-O. |
| 3 | Linear search: all teams containing a given participant. Iterative binary search by `team_id` on a sorted list. Compare with `bisect`. Count comparisons on 1k / 10k / 100k (including missing value). Explain O(n) vs O(log n). |
| 4 | Recursive: all combinations of *k* participants; recursive max-score team. Identify base/recursive cases. Iterative version of combinations + timing. Show and handle `RecursionError`. |
| 5 | Classes `Team`, subclass `StudentTeam` (inheritance + override `final_score`), `Hackathon` with `add` / `remove` / `find` / `leaderboard` / `winners_by_track`. At least 6 objects. |
| 6 | Save/load `teams.txt` (`';`-separated); write `results.txt` (results + diplomas); skip invalid lines to `errors.log`; `try/except/else/finally`; custom `InvalidTeamError`. |
| 7 | Fix buggy common-`team_id` function; optimize with set; measure times; write unit tests including edge cases. |

---

## 4. Data Model Description

### 4.1 Tuple record

```text
(team_id: int, team_name: str, members: tuple[str, ...],
 track: str, score: float, submission_hour: int)
```

A **tuple** fits one record because a submitted result is treated as a fixed snapshot (id, name, members, track, score, hour). Immutability avoids accidental field changes while sorting/searching. Members are nested as a tuple so the whole record stays hashable if needed and clearly “read-only”.

### 4.2 Dictionary and set

- `dict[team_id] → team_tuple` — O(1) average lookup by id.  
- `set` of names — O(1) average membership test (hash table).  

Membership in a set/dict is O(1) on average because Python uses open-addressing hash tables: the key is hashed to a bucket index, so finding an element does not require scanning all keys (unlike a list, which is O(n)).

### 4.3 Classes (Task 5)

```text
Team
  _team_id, _team_name, _track, _members, _score, _submission_hour
  add_member(), submit(), final_score(), __str__()
       ▲
       │ inherits / overrides final_score (+2 university bonus)
StudentTeam
  _university

Hackathon
  _teams: dict[team_id → Team]
  add(), remove(), find(), leaderboard(), winners_by_track()
```

`InvalidTeamError` — custom exception when members > 5 or score ∉ [0, 100].

---

## 5. Algorithm Description and Complexity Analysis

### 5.1 Bubble Sort (Task 2)

Outer passes over the list; adjacent pairs swapped if order is wrong (higher score first; if equal, smaller hour first). If a pass makes no swaps → early stop.

| Case | Time | Space |
|------|------|-------|
| Best (already sorted) | O(n) | O(1) extra |
| Average | O(n²) | O(1) |
| Worst (reverse order) | O(n²) | O(1) |

**Benchmark (random data, measured on this machine):**

| n | comparisons | swaps | seconds |
|---|-------------|-------|---------|
| 10 | ~45 | ~20–30 | ~0.00001 |
| 100 | ~4900 | ~2400 | ~0.0003 |
| 1000 | ~500000 | ~250000 | ~0.04 |

On the real dataset (14 teams): result matched `sorted(..., key=...)`; comparisons = 70, swaps = 31.

### 5.2 Searching (Task 3)

| Algorithm | Idea | Time |
|-----------|------|------|
| Linear (by member) | Scan every team / member | O(n · m) ≈ O(N) |
| Binary (by team_id) | Halve sorted range each step | O(log n) |
| bisect | Same binary idea on sorted ids | O(log n) |

**Comparison counts (hit / miss):**

| n | binary hit | binary miss | bisect hit | bisect miss |
|---|------------|-------------|------------|-------------|
| 1 000 | 9 | 10 | 9 | 9 |
| 10 000 | 13 | 14 | 13 | 13 |
| 100 000 | 16 | 17 | 16 | 16 |

Results of binary search and bisect coincide because both search a sorted array of `team_id` values and return the same index/element when the id exists (or “not found” when it does not). Binary search grows as log₂(n) (~17 for 100k), while linear would need up to ~100k comparisons — that is the practical difference between O(log n) and O(n).

### 5.3 Recursion (Task 4)

**combinations_recursive(names, k)**  
- Base: `k == 0` → `[()]`; `k` invalid / empty names → `[]`.  
- Recursive: combinations that include `names[0]` + those that do not.

**max_score_team(teams)**  
- Base: empty → `None`; one element → that team.  
- Recursive: max of first team vs max of the rest.

Iterative combinations produced the same 10 teams of size 3 from 5 names; times were similar on this small input. Calling a deep recursive function beyond `sys.getrecursionlimit()` raised `RecursionError`, which was caught in `try/except/finally`.

---

## 6. Flowchart / Pseudocode

### Bubble Sort

```text
arr ← copy of teams
for i ← 0 .. n-1:
    swapped ← false
    for j ← 0 .. n-i-2:
        compare arr[j] and arr[j+1] by (-score, hour)
        if out of order: swap; swapped ← true
    if not swapped: break
return arr
```

### Binary search by team_id

```text
left ← 0; right ← n-1
while left ≤ right:
    mid ← (left + right) // 2
    if arr[mid].id = target: return arr[mid]
    if arr[mid].id < target: left ← mid + 1
    else: right ← mid - 1
return None
```

### Recursive combinations

```text
comb(names, k):
    if k = 0: return [()]
    if k < 0 or k > len(names): return []
    with ← [ (names[0],)+c for c in comb(names[1:], k-1) ]
    without ← comb(names[1:], k)
    return with + without
```

---

## 7. Python Code

Project modules (each starts with an author docstring):

| File | Author | Content |
|------|--------|---------|
| `dataset.py` | both | 14 teams + track set |
| `data_structures.py` | Student A | Task 1 |
| `sorting.py` | Student A | Task 2 |
| `recursion.py` | Student A | Task 4 |
| `searching.py` | Student B | Task 3 |
| `models.py` | Student B | Task 5 + `InvalidTeamError` |
| `file_io.py` | Student B | Task 6 |
| `optimization.py` | both | Task 7 |
| `main.py` | both | text menu |
| `tests.py` | both | unit tests |

Full source is in the ZIP archive. Run:

```bash
cd IWS2_Variant28
python3 main.py          # interactive menu
python3 -m unittest tests -v
```

*(For the printed report, paste screenshots of each `.py` file from the IDE here.)*

---

## 8. Program Output and Test Cases

### Test case 1 — full dataset (14 teams)

- Unique participants: 32  
- Dual membership (violations): Aigerim Saduova, Dana Kim, Arman Bekov, …  
- Empty track: Blockchain  
- Best overall by sort: Secure Squad (95.0)

### Test case 2 — searching

- Linear search `"Dana Kim"` → teams #1 and #6  
- Binary search `team_id=5` → Secure Squad (same as bisect)  
- Missing id `999` → `None`

### Test case 3 — files with bad lines

Invalid rows written to `data/errors.log` (wrong field count, non-numeric score, >5 members, score > 100). Only the valid line is loaded.

### Unit tests

```text
Ran 12 tests in ~0.002s
OK
```

Covers empty list, single team, duplicate `team_id`, invalid score, optimized intersection, sorting vs `sorted()`, combinations, OOP inheritance, file skip-on-error.

*(Attach screenshots of the console for cases 1–3 and of the unittest run.)*

---

## 9. Debugging and Optimization (Task 7)

### (a) Bug found

Original function used nested loops and this condition:

```python
if not found:
    result.append(id1)
```

So it returned ids that are in `list1` but **not** in `list2` (set difference), instead of the intersection.

**Debugging steps:**  
1. Took small lists `a = [1,2,3,4,5]`, `b = [3,4,6,7]`.  
2. Expected `[3,4]`.  
3. Printed `id1` and `found` inside the loop — for 3 and 4, `found` was `True`, but they were skipped because of `if not found`.  
4. Changed logic to set intersection.

### (b) Complexity

| Version | Complexity |
|---------|------------|
| Buggy nested loops | O(n · m) time, O(k) extra |
| Optimized `set(list1) & set(list2)` | O(n + m) average |

### (c) Timing (`time.perf_counter`)

| n | buggy (s) | optimized (s) |
|---|-----------|---------------|
| 1000 | ~0.007 | ~0.00008 |
| 2000 | ~0.026 | ~0.00018 |
| 5000 | ~0.15 | ~0.0004 |

### (d) Tests

`tests.py` includes ≥5 tests for the optimized function and Tasks 1–6 (empty / single / duplicates / invalid score / file errors). Student A and Student B each cover ≥3 of their own functions (12 tests total).

---

## 10. Distribution of Work

| Student | Tasks | Modules | Tests |
|---------|-------|---------|-------|
| A (Diar) | 1, 2, 4 | `data_structures.py`, `sorting.py`, `recursion.py` | `TestStudentA` |
| B (Diar) | 3, 5, 6 | `searching.py`, `models.py`, `file_io.py` | `TestStudentB` |
| Both | dataset, 7, menu, report | `dataset.py`, `optimization.py`, `main.py`, `tests.py`, `REPORT.md` | `TestTask7` |

---

## 11. Conclusion

The project implements a complete hackathon results pipeline on one shared dataset: data structures, manual Bubble Sort and searches with counters and Big-O analysis, recursion with a safe `RecursionError` demo, OOP with inheritance, file I/O with exception handling, and a fixed/optimized intersection with unit tests and timing. The text menu in `main.py` runs every task. All requirements of Variant 28 are covered in the modules listed above.

---

*IWS №2 — Programming. Variant 28. Solo submission covering Student A and Student B roles.*
