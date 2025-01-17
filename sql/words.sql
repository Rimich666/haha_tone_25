DELETE FROM words;
INSERT INTO words (expire_at, updated_on, ru, de) VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), 'слово1', 'word1') RETURNING id, ru, de;
SELECT id, ru, de FROM words WHERE ru = 'слово1' and de = 'word1';


INSERT INTO words (de, ru, expire_at, updated_on)
SELECT l.de as de, l.ru as ru, l.expire as expire_at, l.updated as updated_on
FROM words
    RIGHT JOIN
        (SELECT DISTINCT * FROM
            (VALUES
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das buch'), Utf8('книга')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das fahrrad'), Utf8('велосипед')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das fahrrad'), Utf8('велосипедист')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das_buch'), Utf8('книга')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das fieber'), Utf8('жар высокая температура')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('der nachmittag'), Utf8('время после полудня'))) AS X(expire, updated, de, ru))
        as l
    ON (words.de = l.de AND words.ru = l.ru)
WHERE id ISNULL
RETURNING id, de;


DELETE FROM words WHERE id IN (909, 910, 911, 912);

INSERT INTO words (de, ru, expire_at, updated_on, file_path)
SELECT l.de as de, l.ru as ru, l.expire as expire_at, l.updated as updated_on, l.file as file_path
FROM words
    RIGHT JOIN
        (SELECT DISTINCT * FROM
            (VALUES
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das buch'), Utf8('книга'), Utf8('file')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das fahrrad'), Utf8('велосипед'), Utf8('file')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das fahrrad'), Utf8('велосипедист'), Utf8('file')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das fahrrad'), Utf8('велосипедистка'), Utf8('file')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das buch'), Utf8('книжка'), Utf8('file')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das buch'), Utf8('книжечка'), Utf8('file')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('das fieber'), Utf8('жар высокая температура'), Utf8('file')),
                (CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('der nachmittag'), Utf8('время после полудня'), Utf8('file'))) AS X(expire, updated, de, ru, file))
        as l
    ON (words.de = l.de AND words.ru = l.ru)
WHERE id ISNULL
RETURNING id, de;

INSERT INTO audio (de, file_path)
    SELECT DISTINCT de, file_path FROM
        (VALUES
            (Utf8('das buch'), Utf8('das_buch')),
            (Utf8('das fahrrad'), Utf8('das_fahrrad')),
            (Utf8('das fieber'), Utf8('das_fieber')),
            (Utf8('der nachmittag'), Utf8('der_nachmittag'))) AS X(de, file_path)

SELECT l.de FROM audio
RIGHT JOIN
    (SELECT DISTINCT de FROM
        (VALUES
            (Utf8('das buch')),
            (Utf8('das fahrrad')),
            (Utf8('das fahrra')),
            (Utf8('das fahr')),
            (Utf8('das fieber')),
            (Utf8('der nachmittag'))) AS X(de)) as l
ON audio.de = l.de
WHERE file_path ISNULL;