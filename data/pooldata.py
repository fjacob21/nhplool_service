from .players import Players

class PoolData(object):

    def __init__(self, store):
        self._store = store
        self._players = Players(self._store)

    @property
    def players(self):
        return self._players
