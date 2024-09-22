from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def register(name, password):
    hash_value = generate_password_hash(password)

    if not credentials_exists(name, password):
        try:
            sql = text("INSERT INTO users (name, password, role) VALUES (:name, :password, 1)")
            db.session.execute(sql, {"name":name, "password":hash_value})
            db.session.commit()
        except:
            return False

        return True

    return False

def credentials_exists(name, password):
    sql = text("SELECT id, password FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()

    if not user:
        return False

    hash_value = user.password
    return check_password_hash(hash_value, password)

def all_users():
    result = db.session.execute(text("SELECT name FROM users"))
    users = result.fetchall()
    return users
