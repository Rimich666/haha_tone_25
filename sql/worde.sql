DELETE FROM words;
INSERT INTO words (expire_at, updated_on, ru, de) VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), 'слово1', 'word1') RETURNING id, ru, de;
SELECT id, ru, de FROM words WHERE ru = 'слово1' and de = 'word1';
