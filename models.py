import sqlite3

# Configure SQLite database
# dbb = sqlite3.connect("claims.db")
# db = dbb.cursor()


class usersDB:
    def __init__(self, conn):
        self.id = ''
        self.conn = conn
        self.c = conn.cursor()

    # INSERT the new user into users db
    def register_user(self, username, hash):
        sql = "INSERT INTO users (username, hash) VALUES (?, ?)"
        self.c.execute(sql, (username, hash))
        self.conn.commit()

    def set_id(self, id):
        self.id = id

    # change password
    def update_password(self, hash):
        self.c.execute("UPDATE users SET hash = :hash WHERE id = :id", {"hash": hash, "id": self.id})
        self.conn.commit()

class messageDB:
    def __init__(self, user_id, conn):
        self.conn = conn
        self.id = user_id
        self.c = conn.cursor()

    # get list messages of user
    def get_messages(self):
        self.c.execute("SELECT * FROM messages WHERE user_id = :id", {"id": self.id})
        return self.c.fetchone()

    # add new message to the messages list of user
    def add_message(self, **kwargs):
        sql = "INSERT INTO messages (message, title, category) VALUES (?, ?)"
        self.c.execute(sql, **kwargs)
        self.conn.commit()

    def edit_message(self, message):
        self.c.execute("UPDATE messages SET message = :message WHERE id = :id", {"message": message, "id": self.id})
        self.conn.commit()

class addressesDB:
    def __init__(self, conn):
        self.id = ''
        self.conn = conn
        self.c = conn.cursor()

    # get list of addresses
    def getAllAddresses(self):
        self.c.execute("SELECT * FROM addresses")
        return self.c.fetchone()

    # add new message to the messages list of user
    def add_address(self, **kwargs):
        sql = "INSERT INTO addresses (...) VALUES (?, ?)"
        self.c.execute(sql, **kwargs)
        self.conn.commit()

    def edit_address(self, address):
        self.c.execute("UPDATE addresses SET address = :address WHERE id = :id", {"address": address, "id": self.id})
        self.conn.commit()
