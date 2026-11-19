INSERT INTO accounts (id, email, normalized_email) VALUES
  ('a1', 'Alice@example.com', 'alice@example.com'),
  ('a2', 'ALICE@example.com', 'alice@example.com'),
  ('a3', 'legacy-no-normalized@example.com', NULL),
  ('a4', 'other@example.com', NULL);
