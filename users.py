from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def login(username, password):
    sql = "SELECT id, password, role FROM users WHERE username=:username;"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone() 
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.id
            session["user_name"] = username
            session["user_role"] = user.role
            session["csrf_token"] = token_hex(16)
            return True
        else:
            return False

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users(username, password, role) VALUES(:username, :password, :role);"
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def role_required(role):
    if role > session.get("user_role", 0):
        return abort(403)
    return True

def role():
    try:
        return session.get("user_role")
    except:
        return False

def username_exists(username):
    sql = "SELECT username FROM users WHERE username=:username;"
    result = db.session.execute(sql, {"username":username}).fetchone()
    if result == None:
        return False
    else:
        return True

def allow_edit(message_id):
    sql = "SELECT sent_by FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id}).fetchone()
    if result.sent_by != session.get("user_id"):
        return abort(403)

def allow_thread_edit(thread_id):
    sql = "SELECT created_by FROM threads WHERE id=:thread_id"
    result = db.session.execute(sql, {"thread_id":thread_id}).fetchone()
    if result.created_by != session.get("user_id"):
        return abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
