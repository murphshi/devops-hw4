-- 02_seed.sql (SQLite)

PRAGMA foreign_keys = ON;

DELETE FROM note;
DELETE FROM app_user;

DELETE FROM sqlite_sequence WHERE name IN ('note', 'app_user');

INSERT INTO app_user (email, display_name) VALUES
  ('alice@example.com', 'Alice'),
  ('bob@example.com', 'Bob');

INSERT INTO note (user_id, title, body) VALUES
  (1, 'Staging seed note 1', 'This is seeded data for staging environment.'),
  (1, 'Staging seed note 2', 'Second seeded note for Alice.'),
  (2, 'Bob staging note', 'Seeded note for Bob.');

