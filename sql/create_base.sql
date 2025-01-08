DROP TABLE IF EXISTS user_words;
DROP TABLE IF EXISTS user_lists;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS colors;


CREATE TABLE IF NOT EXISTS users
(
    id serial NOT NULL,
    expire_at Datetime NOT NULL,
    updated_on Datetime,
    name Utf8,
    INDEX idx_words GLOBAL UNIQUE ON (name),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS words
(
    id serial NOT NULL,
    expire_at Datetime NOT NULL,
    updated_on Datetime,
    ru Utf8,
    de Utf8,
    file_path Utf8,
    audio_id Utf8,
    INDEX idx_words GLOBAL UNIQUE ON (ru, de),

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS colors
(
    id serial NOT NULL,
    name utf8,
    hex String,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS user_lists
(
    id serial NOT NULL,
    expire_at Datetime NOT NULL,
    updated_on Datetime,
    user_id Int64,
    name utf8,
    INDEX idx_words GLOBAL UNIQUE ON (user_id, name),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS user_words
(
    id serial NOT NULL,
    list_id Int64,
    word_id Int64,
    INDEX idx_words GLOBAL UNIQUE ON (list_id, word_id),
    PRIMARY KEY (id)
);
