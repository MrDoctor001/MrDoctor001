"""Task 1 — tuples, sets and dictionaries for hackathon teams.

Author: Diar (Student A)
"""

from dataset import ALL_TRACKS, get_teams_copy


def build_team_dict(teams=None):
    """Map team_id -> team tuple."""
    if teams is None:
        teams = get_teams_copy()
    result = {}
    for team in teams:
        result[team[0]] = team
    return result


def unique_participants(teams=None):
    """All unique participant names (set)."""
    if teams is None:
        teams = get_teams_copy()
    names = set()
    for team in teams:
        for member in team[2]:
            names.add(member)
    return names


def dual_membership(teams=None):
    """Participants who appear in more than one team."""
    if teams is None:
        teams = get_teams_copy()
    count = {}
    for team in teams:
        for member in team[2]:
            count[member] = count.get(member, 0) + 1
    violators = set()
    for name, n in count.items():
        if n >= 2:
            violators.add(name)
    return violators


def tracks_without_submissions(teams=None, all_tracks=None):
    """Tracks that have no team submissions."""
    if teams is None:
        teams = get_teams_copy()
    if all_tracks is None:
        all_tracks = ALL_TRACKS
    used = set()
    for team in teams:
        used.add(team[3])
    return all_tracks - used


def average_score_by_track(teams=None):
    """Average score for each track."""
    if teams is None:
        teams = get_teams_copy()
    totals = {}
    counts = {}
    for team in teams:
        track = team[3]
        score = team[4]
        totals[track] = totals.get(track, 0.0) + score
        counts[track] = counts.get(track, 0) + 1
    averages = {}
    for track in totals:
        averages[track] = totals[track] / counts[track]
    return averages


def best_team_by_track(teams=None):
    """Best team (highest score) for each track."""
    if teams is None:
        teams = get_teams_copy()
    best = {}
    for team in teams:
        track = team[3]
        if track not in best or team[4] > best[track][4]:
            best[track] = team
    return best


def run_task1():
    """Print Task 1 results."""
    teams = get_teams_copy()
    team_dict = build_team_dict(teams)
    print("=== Task 1: Tuples, Sets, Dictionaries ===")
    print(f"Teams in dictionary: {len(team_dict)}")
    print(f"Unique participants ({len(unique_participants(teams))}):")
    for name in sorted(unique_participants(teams)):
        print(f"  - {name}")
    print(f"\nRule violations (in 2+ teams): {dual_membership(teams)}")
    print(f"Tracks with no submissions: {tracks_without_submissions(teams)}")
    print("\nAverage score by track:")
    for track, avg in sorted(average_score_by_track(teams).items()):
        print(f"  {track}: {avg:.2f}")
    print("\nBest team per track:")
    for track, team in sorted(best_team_by_track(teams).items()):
        print(f"  {track}: {team[1]} (score={team[4]})")
