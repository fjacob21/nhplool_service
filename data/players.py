from .player import Player

class Players(object):

    def __init__(self, store):
        self._store = store

    def _restore(self):
        self._players = {}
        players = self._store.get_rows_id(Player.TABLE_NAME)
        for player_id in players:
            player = self._store.restore(Player.TABLE_NAME, player_id)
            print("player", players)
            self._players[player["id"]] = Player(player["id"], self._store)

    def serialize(self):
        self._restore()
        result = {"players": []}
        for player in self._players.values():
            result["players"].append(player.serialize())
        return result

    def add(self, name, email, password, admin=False):
        self._restore()
        id = Player.userhash(name)
        self._players[id] = Player(id, self._store)
        self._players[id].name = name
        self._players[id].email = email
        self._players[id].admin = admin
        self._players[id].set_password(password)
        return self._players[id]

    def import_player(self, id, name, email, password, admin=False):
        self._restore()
        self._players[id] = Player(id, self._store)
        self._players[id].name = name
        self._players[id].email = email
        self._players[id].admin = admin
        self._players[id].password = password
        return self._players[id]

    def get_name(self, name):
        self._restore()
        for player in self._players.values():
            if player.name == name:
                return player
        return None

    def delete(self, id):
        self._store.delete_row(Player.TABLE_NAME, id)

    def get(self, id):
        self._restore()
        for player in self._players.values():
            if player.id == id:
                return player
        return None

    def get_all(self):
        self._restore()
        return self._players
