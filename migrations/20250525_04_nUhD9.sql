-- 
-- depends: 20250525_03_MRkwN

ALTER TABLE bibliotech.employees ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE bibliotech.employees ADD COLUMN email VARCHAR(255) NOT NULL;