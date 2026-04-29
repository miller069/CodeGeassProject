import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from platform_server.leaderboard_service import LeaderboardService
from platform_server.account_service import AccountService


# ---------------- FAKE MODELS ----------------

class FakeSession:
    def __init__(self, player_id, game_id, score, session_id):
        self.player_id = player_id
        self.game_id = game_id
        self.score = score
        self.session_id = session_id

    def get_player_id(self):
        return self.player_id

    def get_game_id(self):
        return self.game_id

    def get_score(self):
        return self.score

    def get_session_id(self):
        return self.session_id

    def is_valid(self):
        return True


class FakePlayer:
    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username

    def get_player_id(self):
        return self.player_id

    def get_username(self):
        return self.username

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.username} ({self.player_id})"


# ---------------- LEADERBOARD TESTS ----------------

def test_leaderboard_top_n():
    print("\n========== test_leaderboard_top_n ==========")

    service = LeaderboardService()

    sessions = [
        FakeSession("p1", "game1", 500, "s1"),
        FakeSession("p2", "game1", 900, "s2"),
        FakeSession("p3", "game1", 700, "s3"),
        FakeSession("p4", "game1", 1000, "s4"),
    ]

    print("Recording sessions:")
    for s in sessions:
        print(f"  {s.player_id} score={s.score}")
        service.record_session(s)

    top = service.get_top_n("game1", 3)

    print("\nTop 3:")
    names = []
    for entry in top:
        print(f"  {entry.player_id} score={entry.score}")
        names.append(entry.player_id)

    assert names[0] == "p4"
    assert names[1] == "p2"
    assert names[2] == "p3"


def test_leaderboard_range():
    print("\n========== test_leaderboard_range ==========")

    service = LeaderboardService()

    sessions = [
        FakeSession("p1", "game1", 500, "s1"),
        FakeSession("p2", "game1", 900, "s2"),
        FakeSession("p3", "game1", 700, "s3"),
        FakeSession("p4", "game1", 1000, "s4"),
        FakeSession("p5", "game1", 650, "s5"),
    ]

    for s in sessions:
        service.record_session(s)

    result = service.get_score_range("game1", 500, 800)

    print("\nRange 500–800:")
    names = []
    for entry in result:
        print(f"  {entry.player_id} score={entry.score}")
        names.append(entry.player_id)

    assert "p1" in names
    assert "p3" in names
    assert "p5" in names
    assert "p2" not in names
    assert "p4" not in names


def test_leaderboard_rank():
    print("\n========== test_leaderboard_rank ==========")

    service = LeaderboardService()

    sessions = [
        FakeSession("p1", "game1", 500, "s1"),
        FakeSession("p2", "game1", 900, "s2"),
        FakeSession("p3", "game1", 700, "s3"),
    ]

    for s in sessions:
        service.record_session(s)

    rank = service.get_rank("game1", "p2")

    print("\nRank for p2:", rank)

    assert rank == 0 or rank == 1  # depending on implementation


# ---------------- ACCOUNT TESTS ----------------

def test_account_add_and_login():
    print("\n========== test_account_add_and_login ==========")

    service = AccountService()

    p1 = FakePlayer("p1", "nick")
    p2 = FakePlayer("p2", "ryan")

    print("Adding players:")
    print(p1)
    print(p2)

    service.add_player(p1)
    service.add_player(p2)

    result = service.login("nick")

    print("\nLogin result:", result)

    assert result.get_player_id() == "p1"


def test_account_lookup_by_id():
    print("\n========== test_account_lookup_by_id ==========")

    service = AccountService()

    p1 = FakePlayer("p1", "nick")
    service.add_player(p1)

    result = service.get_player("p1")

    print("\nLookup p1:", result)

    assert result.get_username() == "nick"


def test_account_all_players():
    print("\n========== test_account_all_players ==========")

    service = AccountService()

    players = [
        FakePlayer("p1", "nick"),
        FakePlayer("p2", "ryan"),
        FakePlayer("p3", "alex"),
    ]

    for p in players:
        service.add_player(p)

    print("\nAll players:")
    count = 0
    for p in service.all_players():
        print(" ", p)
        count += 1

    assert count == 3


# ---------------- RUNNER ----------------

def run_test(test_function):
    try:
        test_function()
        print(f"✅ {test_function.__name__} PASSED")
    except AssertionError:
        print(f"❌ {test_function.__name__} FAILED")
    except Exception as e:
        print(f"❌ {test_function.__name__} ERROR")
        print("Error:", e)


if __name__ == "__main__":
    print("\n========== RUNNING SERVICE TESTS ==========")

    run_test(test_leaderboard_top_n)
    run_test(test_leaderboard_range)
    run_test(test_leaderboard_rank)

    run_test(test_account_add_and_login)
    run_test(test_account_lookup_by_id)
    run_test(test_account_all_players)

    print("\n========== DONE ==========")