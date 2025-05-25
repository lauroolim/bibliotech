-- 
-- depends: 20250525_05_oHOaC

ALTER TABLE employees ADD CONSTRAINT unique_employees_cpf UNIQUE (cpf);
