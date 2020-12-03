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
