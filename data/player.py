import hashlib

def pswcheck(player, psw):
    players = stores.get().restore('players', 1)
    hname = userhash(player)
    if hname not in players:
        return False
    hpsw = pswhash(player, psw)
    return hpsw == players[hname]['psw']


class Player(object):
    salt = 'superhero'
    TABLE_NAME = "player"

    def userhash(name):
        hash = hashlib.sha256()
        hash.update((Player.salt + name).encode())
        return hash.hexdigest()

    def pswhash(name, psw):
        hash = hashlib.sha256()
        hash.update((Player.salt + name + psw).encode())
        return hash.hexdigest()

    def __init__(self, id, store):
        self._store_obj = store
        self._id = id
        self._name = ""
        self._email = ""
        self._admin = False
        self._last_login = ""
        self._password = ""

    def _restore(self):
        data = self._store_obj.restore(Player.TABLE_NAME, self._id)
        self._name = data["name"]
        self._email = data["email"]
        self._admin = data["admin"]
        self._last_login = data["last_login"]
        self._password = data["password"]

    def _store(self):
        data = self.serialize()
        self._store_obj.store(Player.TABLE_NAME, self._id, data)

    def serialize(self):
        result = {}
        result["id"] = self._id
        result["name"] = self._name
        result["email"] = self._email
        result["admin"] = self._admin
        result["last_login"] = self._last_login
        result["password"] = self._password
        return result

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        self._restore()
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._store()

    @property
    def email(self):
        self._restore()
        return self._email

    @email.setter
    def email(self, value):
        self._email = value
        self._store()

    @property
    def admin(self):
        self._restore()
        return self._admin

    @admin.setter
    def admin(self, value):
        self._admin = value
        self._store()

    @property
    def last_login(self):
        self._restore()
        return self._last_login

    @property
    def password(self):
        self._restore()
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
        self._store()

    def set_password(self, password):
        self._password = Player.pswhash(self.name, password)
        self._store()

    def login(self, password):
        pswhash = Player.pswhash(self.name, password)
        if self.password == pswhash:
            self.update_last_login()
            return True
        return False

    def update_last_login(self):
        self._last_login = now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self._store()
