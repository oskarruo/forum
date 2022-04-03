from db import db

def get_topics():
    return db.session.execute("SELECT topic FROM topics;").fetchall()
    
def get_topicid(topic):
    sql = "SELECT id FROM topics WHERE topic=:topic"
    return db.session.execute(sql, {"topic":topic}).fetchone()