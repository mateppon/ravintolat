from flask import session, request, abort
import secrets
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def user_permission(form_token):
        if session.get("csrf_token") != form_token:
            return False
        return True


def is_admin():
    return session.get("user_role") == 2


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
    sql = text("SELECT id, password, role FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()

    if not user:
        return False

    if user.role == 2:
        if user.password == password:
            session["csrf_token"] = secrets.token_hex(16)
            session["user_role"] = user.role
            session["user_id"] = user.id
            return True

    hash_value = user.password

    if check_password_hash(hash_value, password):
        session["user_id"] = user.id
        session["user_role"] = user.role
        session["csrf_token"] = secrets.token_hex(16)
        return True

    return False

def all_users():
    result = db.session.execute(text("SELECT name FROM users"))
    users = result.fetchall()
    return users

