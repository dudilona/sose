-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;

CREATE TABLE user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hash     TEXT        NOT NULL,
    fullname TEXT        NOT NULL,
    phone    TEXT        NOT NULL,
    email    TEXT        NOT NULL,
    address  TEXT,
    is_admin INTEGER DEFAULT 0
);