from data_structures.hash_table import HashTable


class AccountService:
    """Account/profile lookup backed by hand-built hash tables."""

    def __init__(self):
        self.__players_by_id = HashTable()
        self.__players_by_username = HashTable()

    def add_player(self, player):
        if not player.is_valid():
            return False
        self.__players_by_id.insert(player.get_player_id(), player)
        self.__players_by_username.insert(player.get_username(), player)
        return True

    def login(self, username):
        return self.__players_by_username.get(str(username).strip().lower())

    def get_player(self, player_id):
        return self.__players_by_id.get(player_id)

    def all_players(self):
        for _, player in self.__players_by_id.items():
            yield player
