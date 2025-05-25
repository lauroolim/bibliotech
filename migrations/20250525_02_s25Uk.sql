-- 
-- depends: 20250525_01_GIb7K

ALTER TABLE books ADD COLUMN isbn VARCHAR(20) NOT NULL UNIQUE;

CREATE INDEX idx_books_isbn ON books(isbn);