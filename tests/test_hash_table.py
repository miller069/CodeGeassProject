import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structures.hash_table import HashTable


class FakePlayer:
    def __init__(self, username, score):
        self.username = username
        self.score = score

    def __str__(self):
        return f"{self.username}: {self.score}"

    def __repr__(self):
        return f"{self.username}: {self.score}"


def test_hash_table_insert_and_get():
    print("\n========== test_hash_table_insert_and_get ==========")

    table = HashTable()
    player = FakePlayer("nick123", 500)

    print("Inserting:", player)
    table.insert("nick123", player)

    result = table.get("nick123")
    print("Get nick123 returned:", result)

    assert result.username == "nick123"
    assert result.score == 500


def test_hash_table_contains():
    print("\n========== test_hash_table_contains ==========")

    table = HashTable()
    player = FakePlayer("ryan456", 900)

    print("Inserting:", player)
    table.insert("ryan456", player)

    print("Contains ryan456:", table.contains("ryan456"))
    print("Contains missing_user:", table.contains("missing_user"))

    assert table.contains("ryan456") is True
    assert table.contains("missing_user") is False


def test_hash_table_update_existing_key():
    print("\n========== test_hash_table_update_existing_key ==========")

    table = HashTable()

    print("Inserting nick123 score 500")
    table.insert("nick123", FakePlayer("nick123", 500))

    print("Updating nick123 score to 1000")
    table.insert("nick123", FakePlayer("nick123", 1000))

    result = table.get("nick123")

    print("Get nick123 returned:", result)
    print("Table length:", len(table))

    assert result.score == 1000
    assert len(table) == 1


def test_hash_table_default_value():
    print("\n========== test_hash_table_default_value ==========")

    table = HashTable()

    result = table.get("does_not_exist", default="not found")

    print("Get missing key returned:", result)

    assert result == "not found"


def test_hash_table_many_players():
    print("\n========== test_hash_table_many_players ==========")

    table = HashTable(capacity=8)

    print("Inserting 100 players...")

    for i in range(100):
        username = "player" + str(i)
        table.insert(username, FakePlayer(username, i * 10))

    print("Table length after insert:", len(table))

    p50 = table.get("player50")
    p99 = table.get("player99")

    print("player50 returned:", p50)
    print("player99 returned:", p99)

    assert len(table) == 100
    assert p50.score == 500
    assert p99.score == 990


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
    print("\n========== RUNNING HASH TABLE TESTS ONLY ==========")

    run_test(test_hash_table_insert_and_get)
    run_test(test_hash_table_contains)
    run_test(test_hash_table_update_existing_key)
    run_test(test_hash_table_default_value)
    run_test(test_hash_table_many_players)

    print("\n========== DONE ==========")