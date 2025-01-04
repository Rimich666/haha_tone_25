DELETE FROM users;
INSERT INTO users (expire_at, updated_on, name) VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), 'user1') RETURNING id;
SELECT id, name FROM users WHERE name = 'user1';