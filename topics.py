from db import db

def get_topics():
    return db.session.execute("SELECT topics.id, topic, count(threads), max(created_at) FROM topics LEFT JOIN threads ON threads.visible > 0 AND threads.topic_id = topics.id WHERE topics.visible > 0 GROUP BY topics.id ORDER BY topics.id;").fetchall()
    
def get_topicid(topic):
    sql = "SELECT id FROM topics WHERE topic=:topic;"
    return db.session.execute(sql, {"topic":topic}).fetchone()

def create_topic(topic):
    sql = "INSERT INTO topics(topic, visible) VALUES (:topic, 1);"
    db.session.execute(sql, {"topic":topic})
    db.session.commit()

def topic_visible(topic_id):
    sql = "SELECT visible FROM topics WHERE id=:id;"
    return db.session.execute(sql, {"id":topic_id}).fetchone()

def delete_topic(topic_id):
    sql = "UPDATE topics SET visible = 0 WHERE id=:topic_id;"
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.commit()

def get_topic_id(thread_id):
    sql = "SELECT topics.id FROM topics, threads WHERE threads.topic_id = topics.id AND threads.id=:thread_id;"
    return db.session.execute(sql, {"thread_id":thread_id}).fetchone()
