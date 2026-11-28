"""Shared hackathon dataset for Variant 28.

Author: Diar (Student A / Student B — solo)
"""

# All tracks that were announced for the hackathon
ALL_TRACKS = {"AI", "Web", "Mobile", "IoT", "Cybersecurity", "GameDev", "Blockchain"}

# At least 12 teams: (team_id, team_name, members, track, score, submission_hour)
# Note: "Aigerim Saduova" is in two teams on purpose (rule violation for Task 1)
TEAMS = [
    (1, "Neural Ninjas", ("Arman Bekov", "Dana Kim", "Ilya Petrov"), "AI", 92.5, 14),
    (2, "Byte Bandits", ("Sara Nur", "Timur Ali", "Masha Ivanova", "Ken Zhou"), "Web", 88.0, 11),
    (3, "Cloud Cats", ("Olzhas Rakhmet", "Aigerim Saduova"), "Mobile", 76.5, 16),
    (4, "Pixel Pirates", ("Yerlan Omar", "Nina Volkova", "Sam Lee"), "GameDev", 81.0, 13),
    (5, "Secure Squad", ("Bakyt Tolegen", "Lina Chen", "Pavel Smirnov"), "Cybersecurity", 95.0, 10),
    (6, "IoT Innovators", ("Dana Kim", "Rustem Abyl"), "IoT", 70.0, 18),
    (7, "Web Wizards", ("Aigerim Saduova", "Jon Park", "Elena Mir"), "Web", 84.5, 12),
    (8, "AI Avengers", ("Fariza Zul", "Max Brown", "Alice Wong", "Dias Nurlan"), "AI", 91.0, 15),
    (9, "Mobile Monkeys", ("Kai Nakamura", "Sofia Rakhim"), "Mobile", 67.0, 17),
    (10, "Hack Heroes", ("Arman Bekov", "Vera Sol", "Tom Hardy"), "Cybersecurity", 89.5, 11),
    (11, "Data Dragons", ("Zhanel Kairat", "Chris Evans", "Maya Singh"), "AI", 78.0, 19),
    (12, "Frontend Foxes", ("Lina Chen", "Omar Hassan"), "Web", 73.5, 20),
    (13, "Robot Rangers", ("Ilya Petrov", "Nurlan Sayan", "Kate Moss"), "IoT", 82.0, 14),
    (14, "Quest Crew", ("Sam Lee", "Bakyt Tolegen"), "GameDev", 69.0, 21),
]


def get_teams_copy():
    """Return a shallow copy of the teams list."""
    return list(TEAMS)
