import datetime
import hashlib
import random
import string

sessions = {}

def pw_hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def login_check(session_id):
    if session_id not in sessions:
        return False
    if sessions[session_id]["expire"] < datetime.datetime.now():
        del(sessions[session_id])
        return False

    session_renew(session_id)
    return sessions[session_id]["user_id"]


def session_create(user_id):
    session_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    sessions[session_id] = {
        "user_id": user_id,
        "expire": datetime.datetime.now() + datetime.timedelta(minutes=30)
    }
    return session_id, sessions[session_id]["expire"]


def session_renew(session_id):
    if sessions[session_id]["expire"] < datetime.datetime.now():
        return False
    sessions[session_id]["expire"] = datetime.datetime.now() + datetime.timedelta(minutes=30)
    return True