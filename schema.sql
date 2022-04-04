CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE topic (
    id SERIAL PRIMARY KEY,
    topic TEXT UNIQUE
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    threadname TEXT,
    topic_id INTEGER,
    created_at TIMESTAMP,
    created_by INTEGER
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER,
    sent_at TIMESTAMP,
    content TEXT,
    sent_by INTEGER
);
