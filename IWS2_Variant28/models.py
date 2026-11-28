"""Task 5 — OOP classes for hackathon teams.

Author: Diar (Student B)
"""


class InvalidTeamError(Exception):
    """Raised when a team breaks hackathon rules (size or score)."""


class Team:
    def __init__(self, team_id, team_name, track, members=None, score=0.0, submission_hour=None):
        self._team_id = team_id
        self._team_name = team_name
        self._track = track
        self._members = list(members) if members else []
        self._score = float(score)
        self._submission_hour = submission_hour
        self._validate()

    def _validate(self):
        if len(self._members) > 5:
            raise InvalidTeamError(f"Team {self._team_name} has more than 5 members")
        if not (0 <= self._score <= 100):
            raise InvalidTeamError(f"Score {self._score} is outside 0–100")

    @property
    def team_id(self):
        return self._team_id

    @property
    def team_name(self):
        return self._team_name

    @property
    def track(self):
        return self._track

    @property
    def members(self):
        return tuple(self._members)

    @property
    def score(self):
        return self._score

    @property
    def submission_hour(self):
        return self._submission_hour

    def add_member(self, name):
        if not name or not str(name).strip():
            raise ValueError("Member name cannot be empty")
        if len(self._members) >= 5:
            raise InvalidTeamError("Cannot add member: team already has 5 people")
        self._members.append(str(name).strip())

    def submit(self, hour):
        hour = int(hour)
        if hour < 0 or hour > 24:
            raise ValueError("submission_hour must be between 0 and 24")
        self._submission_hour = hour

    def final_score(self, bonus=0.0):
        bonus = float(bonus)
        if bonus < 0:
            raise ValueError("bonus cannot be negative")
        total = self._score + bonus
        if total > 100:
            total = 100.0
        return total

    def to_tuple(self):
        return (
            self._team_id,
            self._team_name,
            tuple(self._members),
            self._track,
            self._score,
            self._submission_hour if self._submission_hour is not None else 0,
        )

    def __str__(self):
        hour = self._submission_hour if self._submission_hour is not None else "-"
        return (
            f"Team({self._team_id}, {self._team_name}, track={self._track}, "
            f"score={self._score}, hour={hour}, members={self._members})"
        )


class StudentTeam(Team):
    def __init__(self, team_id, team_name, track, university, members=None, score=0.0, submission_hour=None):
        self._university = university
        super().__init__(team_id, team_name, track, members, score, submission_hour)

    @property
    def university(self):
        return self._university

    def final_score(self, bonus=0.0):
        # student teams get +2 university bonus on top of the given bonus
        return super().final_score(bonus + 2.0)

    def __str__(self):
        return super().__str__() + f" university={self._university}"


class Hackathon:
    def __init__(self):
        self._teams = {}

    def add(self, team):
        if not isinstance(team, Team):
            raise TypeError("Only Team objects can be added")
        if team.team_id in self._teams:
            raise ValueError(f"team_id {team.team_id} already exists")
        self._teams[team.team_id] = team

    def remove(self, team_id):
        if team_id not in self._teams:
            raise KeyError(f"No team with id {team_id}")
        del self._teams[team_id]

    def find(self, team_id):
        return self._teams.get(team_id)

    def leaderboard(self):
        return sorted(
            self._teams.values(),
            key=lambda t: (-t.final_score(), t.submission_hour if t.submission_hour is not None else 99),
        )

    def winners_by_track(self):
        best = {}
        for team in self._teams.values():
            track = team.track
            if track not in best or team.final_score() > best[track].final_score():
                best[track] = team
        return best

    def all_teams(self):
        return list(self._teams.values())

    def __len__(self):
        return len(self._teams)


def demo_oop():
    """Build at least 6 objects and show methods."""
    print("=== Task 5: OOP ===")
    h = Hackathon()

    t1 = Team(1, "Neural Ninjas", "AI", ["Arman Bekov", "Dana Kim", "Ilya Petrov"], 92.5, 14)
    t2 = StudentTeam(2, "Byte Bandits", "Web", "AITU", ["Sara Nur", "Timur Ali"], 88.0, 11)
    t3 = Team(3, "Cloud Cats", "Mobile", ["Olzhas Rakhmet"], 76.5, 16)
    t4 = StudentTeam(4, "Pixel Pirates", "GameDev", "NU", ["Yerlan Omar", "Nina Volkova"], 81.0, 13)
    t5 = Team(5, "Secure Squad", "Cybersecurity", ["Bakyt Tolegen", "Lina Chen"], 95.0, 10)
    t6 = StudentTeam(6, "IoT Innovators", "IoT", "KBTU", ["Rustem Abyl", "Dana Kim"], 70.0, 18)

    for t in (t1, t2, t3, t4, t5, t6):
        h.add(t)

    t3.add_member("Aigerim Saduova")
    t3.submit(16)
    print(t1)
    print(t2)
    print(f"StudentTeam final_score (bonus=1): {t2.final_score(1)}")
    print(f"Team final_score (bonus=1): {t1.final_score(1)}")

    print("\nLeaderboard:")
    for i, team in enumerate(h.leaderboard(), 1):
        print(f"  {i}. {team.team_name} -> {team.final_score():.1f}")

    print("\nWinners by track:")
    for track, team in sorted(h.winners_by_track().items()):
        print(f"  {track}: {team.team_name}")

    found = h.find(5)
    print(f"\nfind(5): {found.team_name if found else None}")
    h.remove(3)
    print(f"After remove(3): {len(h)} teams")
    return h
