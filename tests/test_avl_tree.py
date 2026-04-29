import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structures.avl_tree import AVLTree


class FakePlayer:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return f"{self.name}: {self.score}"

    def __repr__(self):
        return f"{self.name}: {self.score}"


def print_players(label, result):
    print("\n" + label)

    items = []
    for player in result:
        items.append(player)
        print(f"  {player.name} - {player.score}")

    if len(items) == 0:
        print("  EMPTY")

    return items


def test_avl_range_query_scores():
    print("\n========== test_avl_range_query_scores ==========")

    tree = AVLTree()

    players = [
        FakePlayer("Nick", 500),
        FakePlayer("Ryan", 900),
        FakePlayer("Chuqi", 700),
        FakePlayer("Ibrahim", 1000),
        FakePlayer("Alex", 300),
        FakePlayer("Maya", 650),
    ]

    print("\nInserting players:")
    for player in players:
        print(f"  inserting {player.name} - {player.score}")
        tree.insert(player.score, player)

    result = tree.range_query(500, 800)
    printed = print_players("Range query 500 to 800 returned:", result)

    names = []
    for player in printed:
        names.append(player.name)

    print("\nNames found:", names)
    print("Expected: Nick, Chuqi, Maya")
    print("Should NOT include: Ryan, Ibrahim, Alex")

    assert "Nick" in names
    assert "Chuqi" in names
    assert "Maya" in names
    assert "Ryan" not in names
    assert "Ibrahim" not in names
    assert "Alex" not in names


def test_avl_inorder_sorted():
    print("\n========== test_avl_inorder_sorted ==========")

    tree = AVLTree()

    players = [
        FakePlayer("A", 50),
        FakePlayer("B", 20),
        FakePlayer("C", 70),
        FakePlayer("D", 10),
        FakePlayer("E", 40),
    ]

    print("\nInserting players:")
    for player in players:
        print(f"  inserting {player.name} - {player.score}")
        tree.insert(player.score, player)

    result = tree.inorder()
    printed = print_players("Inorder returned:", result)

    scores = []
    for player in printed:
        scores.append(player.score)

    print("\nScores found:", scores)
    print("Expected scores:", [10, 20, 40, 50, 70])

    assert scores == [10, 20, 40, 50, 70]


def test_avl_duplicate_scores():
    print("\n========== test_avl_duplicate_scores ==========")

    tree = AVLTree()

    p1 = FakePlayer("Nick", 700)
    p2 = FakePlayer("Ryan", 700)
    p3 = FakePlayer("Chuqi", 900)

    print("\nInserting duplicate scores:")
    print(f"  inserting {p1.name} - {p1.score}")
    tree.insert(p1.score, p1)

    print(f"  inserting {p2.name} - {p2.score}")
    tree.insert(p2.score, p2)

    print(f"  inserting {p3.name} - {p3.score}")
    tree.insert(p3.score, p3)

    result = tree.range_query(700, 700)
    printed = print_players("Range query 700 to 700 returned:", result)

    names = []
    for player in printed:
        names.append(player.name)

    print("\nNames found:", names)
    print("Expected: Nick, Ryan")
    print("Should NOT include: Chuqi")

    assert "Nick" in names
    assert "Ryan" in names
    assert "Chuqi" not in names


def test_avl_empty_range_query():
    print("\n========== test_avl_empty_range_query ==========")

    tree = AVLTree()

    result = tree.range_query(100, 200)
    printed = print_players("Empty range query returned:", result)

    print("\nExpected length: 0")
    print("Actual length:", len(printed))

    assert len(result) == 0


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
    print("\n========== RUNNING AVL TESTS ONLY ==========")

    run_test(test_avl_range_query_scores)
    run_test(test_avl_inorder_sorted)
    run_test(test_avl_duplicate_scores)
    run_test(test_avl_empty_range_query)

    print("\n========== DONE ==========")