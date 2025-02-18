SELECT DISTINCT * FROM (VALUES ('das buch'), ('das fahrrad'), ('das fieber'), ('der nachmittag')) AS X(de);
SELECT word FROM (SELECT words.de as base, l.de as word
    FROM words
    RIGHT JOIN
        (SELECT DISTINCT * FROM
            (VALUES
                ('das buch*'),
                ('das fahrrad_'),
                ('das buch'),
                ('das fahrrad'),
                ('das fieber'),
                ('der nachmittag')
            ) AS X(de))
        as l
    ON (words.de = l.de)) as list_words
    WHERE base ISNULL;

SELECT word, index FROM (SELECT words.de as base, l.de as word, l.index as index
    FROM words
    RIGHT JOIN
        (SELECT DISTINCT * FROM
            (VALUES
                (1, 'das buch'), (2, 'das fahrrad'), (3, 'das fieber'), (4, 'der nachmittag')) AS X(index, de))
        as l
    ON (words.de = l.de)) as list_words
    WHERE base ISNULL;

SELECT new_words.de as de, new_words.ru as ru, new_words.index as index, words.file_path as file
    FROM (SELECT de, ru, index FROM (SELECT words.de as base, l.de as de, l.ru as ru, l.index as index
        FROM words
        RIGHT JOIN
            (SELECT DISTINCT * FROM
                (VALUES
                    (1, 'das buch', 'книга'),
                    (2, 'das fahrrad', 'велосипед'),
                    (5, 'das fahrrad', 'велосипедист'),
                    (6, 'das_buch', 'книга'),
                    (3, 'das fieber', 'жар высокая температура'),
                    (4, 'der nachmittag', 'время после полудня')) AS X(index, de, ru))
            as l
        ON (words.de = l.de AND words.ru = l.ru)) as list_words
        WHERE list_words.base ISNULL) as new_words
    LEFT JOIN words
    ON new_words.de = words.de;

SELECT id
        FROM words
        INNER JOIN
            (SELECT DISTINCT * FROM
                (VALUES
                    (1, 'das buch', 'книга'),
                    (2, 'das fahrrad', 'велосипед'),
                    (5, 'das fahrrad', 'велосипедист'),
                    (6, 'das_buch', 'книга'),
                    (3, 'das fieber', 'жар высокая температура'),
                    (4, 'der nachmittag', 'время после полудня')) AS X(index, de, ru))
            as l
        ON (words.de = l.de AND words.ru = l.ru);

SELECT id FROM user_lists WHERE user_id in
(SELECT id FROM users WHERE name = 'EFE76D1449413314CDB750CCB4D3562A2F85DB599A5A465E98C494888474FE13')
AND name = 'Майский зеленый';

SELECT ru, de, file_path, ids.id as id, audio_id FROM words
RIGHT JOIN
    (SELECT word_id as id, audio_id FROM user_words WHERE list_id = 1) as ids
ON words.id = ids.id;