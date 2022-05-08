from db import db

def get_threads(topic_id):
    sql = "SELECT threads.id, threads.threadname, sum(messages.visible), max(sent_at) FROM topics, threads LEFT JOIN messages ON messages.thread_id = threads.id WHERE topics.id = threads.topic_id AND topics.id=:topic_id AND threads.visible > 0 GROUP BY threads.id;"
    return db.session.execute(sql, {"topic_id":topic_id}).fetchall()

def get_threadinfo(thread_id):
    sql = "SELECT id, threadname, created_by, name_modified FROM threads WHERE id=:thread_id;"
    return db.session.execute(sql, {"thread_id":thread_id}).fetchone()

def create_thread(topic_id, user, threadname):
    sql = "INSERT INTO threads(topic_id, created_by, threadname, created_at, name_modified, visible) VALUES (:topic_id, :created_by, :threadname, TO_CHAR(NOW() :: TIMESTAMP, 'dd.mm.yyyy klo hh24.mi.ss'), 0, 1);"
    db.session.execute(sql, {"topic_id":topic_id, "created_by":user, "threadname":threadname})
    db.session.commit()
    sql2 = "SELECT id FROM threads WHERE topic_id=:topic_id AND created_by=:created_by AND threadname=:threadname ORDER BY created_at DESC;"
    return db.session.execute(sql2, {"topic_id":topic_id, "created_by":user, "threadname":threadname}).fetchone()

def edit_title(thread_id, title):
    sql = "UPDATE threads SET threadname=:title, name_modified = 1 WHERE id=:thread_id"
    db.session.execute(sql, {"title":title, "thread_id":thread_id})
    db.session.commit()

def delete_thread(thread_id):
    sql = "UPDATE threads SET visible = 0 WHERE id=:thread_id"
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()

def thread_visible(thread_id):
    sql = "SELECT visible FROM threads WHERE id=:thread_id"
    return db.session.execute(sql, {"thread_id":thread_id}).fetchone()
