INSERT INTO user_lists (expire_at, updated_on, user_id, name) VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), 2, 'слово') RETURNING id;

SELECT name FROM (SELECT DISTINCT * FROM
    (VALUES ('Агатовый серый'), ('Ализариновый красный'), ('Амарантовый')) AS X(color))
    as l
    RIGHT JOIN colors
    ON l.color = colors.name
    WHERE color ISNULL


SELECT id as word_id, 7 list_id
        FROM words
        INNER JOIN
            (SELECT DISTINCT * FROM
                (VALUES
                    ('das buch', 'книга'),
                    ('das fahrrad', 'велосипед'),
                    ('das fahrrad', 'велосипедист'),
                    ('das_buch', 'книга'),
                    ('das fieber', 'жар высокая температура'),
                    ('der nachmittag', 'время после полудня')) AS X(de, ru))
            as l
        ON (words.de = l.de AND words.ru = l.ru);