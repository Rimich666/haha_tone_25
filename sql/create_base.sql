DROP TABLE IF EXISTS user_words;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS users;

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
    binary_payload String, -- backtick symbol ` could be used to escape special characters
    ru Utf8,
    de Utf8,
    file_path Utf8,
    audio_id Utf8,
    INDEX idx_words GLOBAL UNIQUE ON (ru, de),

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS user_words
(
    id serial NOT NULL,
    user_id Int64,
    word_id Int64,
    INDEX idx_words GLOBAL UNIQUE ON (user_id, word_id),
    PRIMARY KEY (id)
);