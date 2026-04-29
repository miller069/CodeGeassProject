from data_structures.hash_table import HashTable
from data_structures.avl_tree import AVLTree
from data_structures.max_heap import MaxHeap
from data_structures.arraylist import ArrayList


class LeaderboardEntry:
    def __init__(self, player_id, game_id, score, session):
        self.player_id = player_id
        self.game_id = game_id
        self.score = score
        self.session = session

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "game_id": self.game_id,
            "score": self.score,
            "session_id": self.session.get_session_id(),
        }


class GameLeaderboard:
    def __init__(self):
        self.score_heap = MaxHeap(key=lambda entry: entry.score)
        self.score_tree = AVLTree()
        self.best_score_by_player = HashTable()

    def insert_session(self, session):
        old_best = self.best_score_by_player.get(session.get_player_id())
        if old_best is None or session.get_score() > old_best.score:
            entry = LeaderboardEntry(
                session.get_player_id(),
                session.get_game_id(),
                session.get_score(),
                session,
            )
            self.best_score_by_player.insert(session.get_player_id(), entry)
            self.score_heap.insert(entry)
            self.score_tree.insert(entry.score, entry)

    def top_n(self, n):
        result = ArrayList()
        heap_copy = self.score_heap.copy()
        count = 0
        while count < n and len(heap_copy) > 0:
            entry = heap_copy.extract_max()
            # Skip stale heap entries when a player later sets a better score.
            current_best = self.best_score_by_player.get(entry.player_id)
            if current_best is entry:
                result.append(entry)
                count += 1
        return result

    def score_range(self, low, high):
        return self.score_tree.range_query(low, high)

    def rank_for_player(self, player_id):
        entry = self.best_score_by_player.get(player_id)
        if entry is None:
            return None
        return self.score_tree.rank_of_key_descending(entry.score)


class LeaderboardService:
    """Maintains one AVL tree and one max heap per game leaderboard."""

    def __init__(self):
        self.__boards_by_game = HashTable()

    def __get_or_create_board(self, game_id):
        board = self.__boards_by_game.get(game_id)
        if board is None:
            board = GameLeaderboard()
            self.__boards_by_game.insert(game_id, board)
        return board

    def record_session(self, session):
        if not session.is_valid():
            return False
        self.__get_or_create_board(session.get_game_id()).insert_session(session)
        return True

    def get_top_n(self, game_id, n=10):
        board = self.__boards_by_game.get(game_id)
        if board is None:
            return ArrayList()
        return board.top_n(n)

    def get_score_range(self, game_id, low, high):
        board = self.__boards_by_game.get(game_id)
        if board is None:
            return ArrayList()
        return board.score_range(low, high)

    def get_rank(self, game_id, player_id):
        board = self.__boards_by_game.get(game_id)
        if board is None:
            return None
        return board.rank_for_player(player_id)
