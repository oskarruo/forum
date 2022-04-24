from db import db

def get_messages(thread_id):
    sql = "SELECT messages.sent_by, messages.id, users.username, messages.content, messages.sent_at, messages.modified FROM users, messages WHERE messages.sent_by = users.id AND messages.thread_id =:thread AND messages.visible > 0 ORDER BY messages.sent_at;"
    return db.session.execute(sql, {"thread":thread_id}).fetchall()

def send_message(thread_id, content, user_id):
    sql = "INSERT INTO messages (content, thread_id, sent_at, sent_by, modified, visible) VALUES (:content, :thread_id, NOW(), :sent_by, 0, 1);"
    db.session.execute(sql, {"content":content, "thread_id":thread_id, "sent_by":user_id})
    db.session.commit()

def get_content(message_id):
    sql = "SELECT id, content FROM messages WHERE id=:message_id;"
    return db.session.execute(sql, {"message_id":message_id}).fetchone()

def edit_message(message_id, content):
    sql = "UPDATE messages SET content=:content, modified = 1 WHERE id=:message_id"
    db.session.execute(sql, {"content":content, "message_id":message_id})
    db.session.commit()

def delete_message(message_id):
    sql = "UPDATE messages SET visible = 0 WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()