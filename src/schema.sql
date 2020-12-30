-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS "order";

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
    address     TEXT,
    google_map  TEXT
);

INSERT INTO settings (store_name, footer_desc, main_header, main_desc, phone, email, address, google_map)
values ('SOSE', 'Edit this message in the admin panel', 'Welcome to the SOSE!',
        'Welcome to the SOSE - the Simple Online Store Engine. The first thing you need to do ' ||
        'is click on the <a class="link-primary" href="/register">registration</a> link and register' ||
        ' the new user. Know - the first registered user becomes the administrator.<br />Enjoy &#128521;',
        'Edit this in the admin panel', 'Edit this in the admin panel', 'Edit this in the admin panel',
        '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d577057.9432268722!2d37.52868910483382!3d55.59970604003887!2m' ||
        '3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x414ab8b638d07bbb%3A0xc7782fe44582cb2!2z0YPQuy4g0JPRg9C00LrQvtCy0LAsIDIxLCDQltGD0' ||
        'LrQvtCy0YHQutC40LksINCc0L7RgdC60L7QstGB0LrQsNGPINC-0LHQuy4sIDE0MDE4Ng!5e0!3m2!1sru!2sru!4v1609313076306!5m2!1sru!2sru"
                width="800" height="600" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>');

CREATE TABLE product
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    price       NUMERIC NOT NULL,
    header      TEXT,
    instruction TEXT,
    info        TEXT
);

CREATE TABLE "order"
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id INTEGER,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT,
    items_count INTEGER,
    total_price NUMERIC
)