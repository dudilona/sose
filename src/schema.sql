-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS settings;

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

CREATE TABLE settings
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name  TEXT,
    footer_desc TEXT,
    main_header TEXT,
    main_desc   TEXT,
    phone       TEXT,
    email       TEXT,
    address     TEXT
);

INSERT INTO settings (store_name, footer_desc, main_header, main_desc, phone, email, address)
values ('SOSE', 'Edit this message in the admin panel', 'Welcome to the SOSE!', 'Welcome to the SOSE - the Simple Online Store Engine. ' ||
'The first thing you need to do is click on the <a class="link-primary" href="/register">registration</a> link and register the new user. ' ||
'Know - the first registered user becomes the administrator.<br />Enjoy &#128521;', 'Edit this in the admin panel', 'Edit this in the admin panel', 'Edit this in the admin panel');