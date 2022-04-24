CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT UNIQUE,
    visible INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    threadname TEXT,
    topic_id INTEGER,
    created_at TIMESTAMP,
    created_by INTEGER,
    name_modified INTEGER,
    visible INTEGER
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER,
    sent_at TIMESTAMP,
    content TEXT,
    sent_by INTEGER,
    modified INTEGER,
    visible INTEGER
);
