from db import db

def get_messages(thread_id):
    sql = "SELECT users.username, messages.content, messages.sent_at FROM users, messages WHERE messages.sent_by = users.id AND messages.thread_id =:thread ORDER BY sent_at;"
    return db.session.execute(sql, {"thread":thread_id}).fetchall()

def send_message(thread_id, content, user_id):
    sql = "INSERT INTO messages (content, thread_id, sent_at, sent_by) VALUES (:content, :thread_id, NOW(), :sent_by);"
    db.session.execute(sql, {"content":content, "thread_id":thread_id, "sent_by":user_id})
    db.session.commit()