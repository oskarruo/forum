from db import db
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username;"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone() 
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.id
            session["user_name"] = username
            session["user_logged"] = 1
            return True
        else:
            return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users(username, password) VALUES(:username, :password);"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_logged"]

def islogged():
    try:
        session["user_name"]
        return True
    except:
        return abort(403)

def username_exists(username):
    sql = "SELECT username FROM users WHERE username=:username;"
    result = db.session.execute(sql, {"username":username}).fetchone()
    if result == None:
        return False
    else:
        return True