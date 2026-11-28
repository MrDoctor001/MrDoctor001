"""Unit tests for IWS2 Variant 28 (Tasks 1–7).

Authors: Diar (Student A / Student B)
"""

import os
import tempfile
import unittest

from data_structures import (
    average_score_by_track,
    best_team_by_track,
    build_team_dict,
    dual_membership,
    tracks_without_submissions,
    unique_participants,
)
from dataset import ALL_TRACKS, get_teams_copy
from file_io import load_teams, save_teams, teams_from_dataset
from models import Hackathon, InvalidTeamError, StudentTeam, Team
from optimization import common_team_ids, common_team_ids_buggy
from recursion import combinations_iterative, combinations_recursive, max_score_team
from searching import binary_search_by_id, linear_search_by_member
from sorting import bubble_sort_teams, team_key


class TestStudentA(unittest.TestCase):
    """Tests for Tasks 1, 2, 4 (Student A)."""

    def test_build_team_dict_and_unique(self):
        teams = get_teams_copy()
        d = build_team_dict(teams)
        self.assertEqual(len(d), len(teams))
        self.assertEqual(d[1][1], "Neural Ninjas")
        names = unique_participants(teams)
        self.assertIn("Dana Kim", names)
        self.assertTrue(len(names) >= 20)

    def test_dual_membership_and_empty_track(self):
        violators = dual_membership()
        self.assertIn("Aigerim Saduova", violators)
        empty = tracks_without_submissions()
        self.assertIn("Blockchain", empty)
        # empty list edge case
        self.assertEqual(unique_participants([]), set())
        self.assertEqual(build_team_dict([]), {})

    def test_bubble_sort_matches_sorted(self):
        teams = get_teams_copy()
        ranked, comps, swaps = bubble_sort_teams(teams)
        ref = sorted(teams, key=team_key)
        self.assertEqual(ranked, ref)
        self.assertGreater(comps, 0)
        # single team
        one = [teams[0]]
        r, c, s = bubble_sort_teams(one)
        self.assertEqual(r, one)
        self.assertEqual(c, 0)
        # empty
        r, c, s = bubble_sort_teams([])
        self.assertEqual(r, [])

    def test_combinations_and_max_score(self):
        names = ["A", "B", "C", "D"]
        rec = combinations_recursive(names, 2)
        it = combinations_iterative(names, 2)
        self.assertEqual(set(rec), set(it))
        self.assertEqual(len(rec), 6)
        self.assertEqual(combinations_recursive(names, 0), [()])
        best = max_score_team(get_teams_copy())
        self.assertEqual(best[0], 5)  # Secure Squad 95.0
        self.assertIsNone(max_score_team([]))


class TestStudentB(unittest.TestCase):
    """Tests for Tasks 3, 5, 6 (Student B)."""

    def test_linear_and_binary_search(self):
        teams = get_teams_copy()
        found, comps = linear_search_by_member(teams, "Dana Kim")
        self.assertEqual(len(found), 2)
        self.assertGreater(comps, 0)
        found_empty, _ = linear_search_by_member([], "X")
        self.assertEqual(found_empty, [])

        by_id = sorted(teams, key=lambda t: t[0])
        team, _ = binary_search_by_id(by_id, 5)
        self.assertIsNotNone(team)
        self.assertEqual(team[1], "Secure Squad")
        missing, _ = binary_search_by_id(by_id, 999)
        self.assertIsNone(missing)

    def test_oop_validation_and_inheritance(self):
        t = Team(1, "T", "AI", ["A", "B"], 50, 10)
        t.add_member("C")
        self.assertEqual(len(t.members), 3)
        st = StudentTeam(2, "S", "Web", "AITU", ["X"], 80, 11)
        self.assertGreaterEqual(st.final_score(0), t.final_score(0) + 0)  # +2 bonus
        self.assertEqual(st.final_score(0), 82.0)

        with self.assertRaises(InvalidTeamError):
            Team(3, "Bad", "AI", ["1", "2", "3", "4", "5", "6"], 10, 1)
        with self.assertRaises(InvalidTeamError):
            Team(4, "BadScore", "AI", ["1"], 150, 1)

        h = Hackathon()
        h.add(t)
        h.add(st)
        self.assertEqual(len(h), 2)
        self.assertEqual(h.find(1).team_name, "T")
        # duplicate team_id
        with self.assertRaises(ValueError):
            h.add(Team(1, "Dup", "Web", ["Z"], 10, 1))

    def test_file_load_skips_invalid(self):
        h = teams_from_dataset()
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "teams.txt")
            err = os.path.join(tmp, "errors.log")
            save_teams(h, path)
            loaded = load_teams(path, err)
            self.assertEqual(len(loaded), len(h))

            bad = os.path.join(tmp, "bad.txt")
            with open(bad, "w", encoding="utf-8") as f:
                f.write("1;Good;A,B;AI;90;10;\n")
                f.write("broken\n")
                f.write("2;Bad;A;Web;nope;10;\n")
                f.write("3;Huge;A,B,C,D,E,F;AI;40;10;\n")
            fixed = load_teams(bad, err)
            self.assertEqual(len(fixed), 1)
            with open(err, encoding="utf-8") as f:
                log = f.read()
            self.assertIn("broken", log)


class TestTask7(unittest.TestCase):
    """Tests for optimized common_team_ids + edge cases."""

    def test_common_ids_basic(self):
        a = [1, 2, 3, 4]
        b = [3, 4, 5]
        self.assertEqual(sorted(common_team_ids(a, b)), [3, 4])

    def test_common_ids_empty_and_single(self):
        self.assertEqual(common_team_ids([], [1, 2]), [])
        self.assertEqual(common_team_ids([7], [7]), [7])
        self.assertEqual(common_team_ids([7], [8]), [])

    def test_common_ids_duplicates(self):
        a = [1, 1, 2, 2, 3]
        b = [2, 2, 4]
        self.assertEqual(sorted(common_team_ids(a, b)), [2])

    def test_buggy_is_wrong(self):
        a = [1, 2, 3]
        b = [2, 3, 4]
        # buggy returns difference, not intersection
        self.assertNotEqual(sorted(common_team_ids_buggy(a, b)), [2, 3])
        self.assertEqual(sorted(common_team_ids_buggy(a, b)), [1])

    def test_avg_and_best_helpers(self):
        teams = [
            (1, "A", ("x",), "AI", 10.0, 1),
            (2, "B", ("y",), "AI", 30.0, 2),
            (3, "C", ("z",), "Web", 20.0, 3),
        ]
        avg = average_score_by_track(teams)
        self.assertEqual(avg["AI"], 20.0)
        best = best_team_by_track(teams)
        self.assertEqual(best["AI"][0], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
