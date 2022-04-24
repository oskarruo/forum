from db import db

def get_topics():
    return db.session.execute("SELECT topic, count(threads), max(created_at) FROM topics LEFT JOIN threads ON topics.id = threads.topic_id GROUP BY topic;").fetchall()
    
def get_topicid(topic):
    sql = "SELECT id FROM topics WHERE topic=:topic"
    return db.session.execute(sql, {"topic":topic}).fetchone()