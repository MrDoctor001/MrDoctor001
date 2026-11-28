"""Task 6 — file I/O and exception handling for hackathon data.

Author: Diar (Student B)
"""

import os

from models import Hackathon, InvalidTeamError, StudentTeam, Team


def save_teams(hackathon, path="data/teams.txt"):
    """Save all teams to a text file (fields separated by ';')."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            for team in hackathon.all_teams():
                members = ",".join(team.members)
                uni = ""
                if isinstance(team, StudentTeam):
                    uni = team.university
                hour = team.submission_hour if team.submission_hour is not None else ""
                line = (
                    f"{team.team_id};{team.team_name};{members};{team.track};"
                    f"{team.score};{hour};{uni}\n"
                )
                f.write(line)
    except PermissionError as e:
        print(f"PermissionError while saving: {e}")
        raise
    else:
        print(f"Saved {len(hackathon)} teams to {path}")
    finally:
        pass


def _parse_line(line, line_no):
    parts = line.strip().split(";")
    if len(parts) not in (6, 7):
        raise ValueError(f"line {line_no}: wrong number of fields ({len(parts)})")
    team_id = int(parts[0])
    name = parts[1]
    members = [m for m in parts[2].split(",") if m]
    track = parts[3]
    score = float(parts[4])
    hour = int(parts[5]) if parts[5] != "" else None
    university = parts[6] if len(parts) == 7 else ""

    if len(members) > 5 or not (0 <= score <= 100):
        raise InvalidTeamError(
            f"line {line_no}: invalid team (members={len(members)}, score={score})"
        )

    if university:
        return StudentTeam(team_id, name, track, university, members, score, hour)
    return Team(team_id, name, track, members, score, hour)


def load_teams(path="data/teams.txt", errors_path="data/errors.log"):
    """Load teams into a Hackathon. Invalid lines go to errors.log."""
    hackathon = Hackathon()
    os.makedirs(os.path.dirname(errors_path) or ".", exist_ok=True)

    try:
        err_file = open(errors_path, "w", encoding="utf-8")
    except PermissionError as e:
        print(f"Cannot open errors log: {e}")
        raise

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    team = _parse_line(line, line_no)
                except (ValueError, InvalidTeamError) as e:
                    err_file.write(f"{line.strip()}  # {e}\n")
                    continue
                else:
                    try:
                        hackathon.add(team)
                    except ValueError as e:
                        err_file.write(f"{line.strip()}  # {e}\n")
    except FileNotFoundError:
        print(f"FileNotFoundError: {path} not found")
        raise
    except PermissionError as e:
        print(f"PermissionError while loading: {e}")
        raise
    else:
        print(f"Loaded {len(hackathon)} teams from {path}")
    finally:
        err_file.close()

    return hackathon


def write_results(hackathon, path="data/results.txt"):
    """Write leaderboard and diploma list to results.txt."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    board = hackathon.leaderboard()
    winners = hackathon.winners_by_track()

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("FINAL RESULTS\n")
            f.write("=" * 40 + "\n")
            for i, team in enumerate(board, 1):
                f.write(f"{i}. {team.team_name} ({team.track}) — {team.final_score():.1f}\n")
            f.write("\nDIPLOMAS (track winners)\n")
            f.write("=" * 40 + "\n")
            for track, team in sorted(winners.items()):
                f.write(f"Track {track}: {team.team_name} — diploma\n")
    except PermissionError as e:
        print(f"PermissionError while writing results: {e}")
        raise
    else:
        print(f"Results written to {path}")
    finally:
        print("write_results finished")


def teams_from_dataset():
    """Build a Hackathon from the shared tuple dataset."""
    from dataset import get_teams_copy

    h = Hackathon()
    for t in get_teams_copy():
        team_id, name, members, track, score, hour = t
        # mark a few as student teams
        if team_id in (2, 4, 6, 8):
            uni = {2: "AITU", 4: "NU", 6: "KBTU", 8: "SDU"}[team_id]
            h.add(StudentTeam(team_id, name, track, uni, list(members), score, hour))
        else:
            h.add(Team(team_id, name, track, list(members), score, hour))
    return h


def run_task6():
    """Save, load, write results; show error handling."""
    print("=== Task 6: File & Exception Handling ===")
    h = teams_from_dataset()
    save_teams(h, "data/teams.txt")
    loaded = load_teams("data/teams.txt", "data/errors.log")
    write_results(loaded, "data/results.txt")

    # demo invalid lines
    bad_path = "data/teams_bad.txt"
    with open(bad_path, "w", encoding="utf-8") as f:
        f.write("1;Ok Team;A,B;AI;90;10;\n")
        f.write("badline_without_enough_fields\n")
        f.write("2;Bad Score;A;Web;abc;10;\n")
        f.write("3;Too Big;A,B,C,D,E,F;AI;50;10;\n")
        f.write("4;Out Of Range;A;IoT;150;10;\n")
    print("\nLoading file with invalid lines...")
    fixed = load_teams(bad_path, "data/errors.log")
    print(f"Valid teams loaded: {len(fixed)}")
    with open("data/errors.log", "r", encoding="utf-8") as f:
        print("errors.log:")
        print(f.read())
