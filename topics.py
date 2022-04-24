from db import db

def get_topics():
    return db.session.execute("SELECT topic, count(threads), max(created_at) FROM topics LEFT JOIN threads ON threads.visible > 0 AND threads.topic_id = topics.id WHERE topics.visible > 0 GROUP BY topics.id ORDER BY topics.id;").fetchall()
    
def get_topicid(topic):
    sql = "SELECT id FROM topics WHERE topic=:topic;"
    return db.session.execute(sql, {"topic":topic}).fetchone()

def create_topic(topic):
    sql = "INSERT INTO topics(topic, visible) VALUES (:topic, 1);"
    db.session.execute(sql, {"topic":topic})
    db.session.commit()

def topic_visible(topic):
    sql = "SELECT visible FROM topics WHERE topic=:topic;"
    return db.session.execute(sql, {"topic":topic}).fetchone()

def delete_topic(topic):
    sql = "UPDATE topics SET visible = 0 WHERE topic=:topic;"
    db.session.execute(sql, {"topic":topic})
    db.session.commit()