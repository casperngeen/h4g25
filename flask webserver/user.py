from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, password, isadmin):
        """
        Function to initialize user

        Args:
            id_ (int): unique id for each user
            name (str): username
            password (str): password of user
            isadmin (int): 0 for not admin, 1 for admin
        """
        self.id = id_
        self.name = name
        self.password = password
        self.isadmin = isadmin

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], password=user[2], isadmin=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, password, isadmin):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, password, isadmin) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, password, isadmin),
        )
        db.commit()