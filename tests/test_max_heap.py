import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structures.max_heap import MaxHeap


class FakePlayer:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return f"{self.name}: {self.score}"

    def __repr__(self):
        return f"{self.name}: {self.score}"


def test_heap_top_player():
    print("\n========== test_heap_top_player ==========")

    heap = MaxHeap(key=lambda player: player.score)

    players = [
        FakePlayer("Nick", 500),
        FakePlayer("Ryan", 900),
        FakePlayer("Chuqi", 700),
        FakePlayer("Ibrahim", 1000),
    ]

    print("Inserting players:")
    for p in players:
        print(f"  {p}")
        heap.insert(p)

    top = heap.extract_max()

    print("Extracted max:", top)

    assert top.name == "Ibrahim"
    assert top.score == 1000


def test_heap_top_n_players():
    print("\n========== test_heap_top_n_players ==========")

    heap = MaxHeap(key=lambda player: player.score)

    players = [
        FakePlayer("Nick", 500),
        FakePlayer("Ryan", 900),
        FakePlayer("Chuqi", 700),
        FakePlayer("Ibrahim", 1000),
        FakePlayer("Alex", 300),
    ]

    print("Inserting players:")
    for p in players:
        print(f"  {p}")
        heap.insert(p)

    print("\nExtracting top 3:")
    top_3 = []
    for i in range(3):
        player = heap.extract_max()
        print(f"  #{i+1}: {player}")
        top_3.append(player)

    assert top_3[0].name == "Ibrahim"
    assert top_3[1].name == "Ryan"
    assert top_3[2].name == "Chuqi"


def test_heap_peek_does_not_remove():
    print("\n========== test_heap_peek_does_not_remove ==========")

    heap = MaxHeap(key=lambda player: player.score)

    heap.insert(FakePlayer("Nick", 500))
    heap.insert(FakePlayer("Ryan", 900))

    print("Heap size before peek:", len(heap))

    top = heap.peek()

    print("Peek returned:", top)
    print("Heap size after peek:", len(heap))

    assert top.name == "Ryan"
    assert len(heap) == 2


def test_heap_empty_extract():
    print("\n========== test_heap_empty_extract ==========")

    heap = MaxHeap()

    result1 = heap.extract_max()
    result2 = heap.peek()

    print("Extract from empty heap:", result1)
    print("Peek from empty heap:", result2)

    assert result1 is None
    assert result2 is None


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
    print("\n========== RUNNING MAX HEAP TESTS ONLY ==========")

    run_test(test_heap_top_player)
    run_test(test_heap_top_n_players)
    run_test(test_heap_peek_does_not_remove)
    run_test(test_heap_empty_extract)

    print("\n========== DONE ==========")