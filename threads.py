from db import db

def get_threads(topic):
    sql = "SELECT threads.id, threads.threadname FROM threads, topics WHERE topics.topic=:topic AND topics.id = threads.topic_id;"
    return db.session.execute(sql, {"topic":topic}).fetchall()
    
def get_threadinfo(thread_id):
    sql = "SELECT id, threadname FROM threads WHERE id=:thread_id;"
    return db.session.execute(sql, {"thread_id":thread_id}).fetchone()

def create_thread(topic_id, user, threadname):
    sql = "INSERT INTO threads(topic_id, created_by, threadname, created_at) VALUES (:topic_id, :created_by, :threadname, NOW());"
    db.session.execute(sql, {"topic_id":topic_id, "created_by":user, "threadname":threadname})
    db.session.commit()
    sql2 = "SELECT id FROM threads WHERE topic_id=:topic_id AND created_by=:created_by AND threadname=:threadname ORDER BY created_at DESC;"
    return db.session.execute(sql2, {"topic_id":topic_id, "created_by":user, "threadname":threadname}).fetchone()