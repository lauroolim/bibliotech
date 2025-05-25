-- 
-- depends: 20250525_01_GIb7K

CREATE SCHEMA IF NOT EXISTS bibliotech;

CREATE SEQUENCE bibliotech.users_id_seq;
CREATE SEQUENCE bibliotech.employees_id_seq;
CREATE SEQUENCE bibliotech.books_id_seq;
CREATE SEQUENCE bibliotech.loans_id_seq;
CREATE SEQUENCE bibliotech.fines_id_seq;
CREATE SEQUENCE bibliotech.authors_id_seq;


CREATE TABLE bibliotech.authors (
    id INTEGER PRIMARY KEY DEFAULT nextval('bibliotech.authors_id_seq'),
    full_name VARCHAR(100) NOT NULL
);

CREATE TABLE bibliotech.users (
    id INTEGER PRIMARY KEY DEFAULT nextval('bibliotech.users_id_seq'),
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT uk_users_email UNIQUE (email), -- candidata 
    CONSTRAINT uk_users_username UNIQUE (username) -- candidata 
);

CREATE TABLE bibliotech.employees (
    id INTEGER PRIMARY KEY DEFAULT nextval('bibliotech.employees_id_seq'),
    username VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE,
    hired_at DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT uk_employee_cpf UNIQUE (cpf) -- candidata 
);

CREATE TABLE bibliotech.books (
    id INTEGER PRIMARY KEY DEFAULT nextval('bibliotech.books_id_seq'),
    title VARCHAR(200) NOT NULL,
    isbn VARCHAR(20) NOT NULL,
    publish_year INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_books_isbn UNIQUE (isbn), -- candidata 
    CONSTRAINT ck_books_year CHECK (publish_year <= EXTRACT(YEAR FROM CURRENT_DATE)) 
);

-- books-authors (N:M) 
CREATE TABLE bibliotech.books_authors (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES bibliotech.books(id),
    FOREIGN KEY (author_id) REFERENCES bibliotech.authors(id),
    PRIMARY KEY (book_id, author_id) -- primária composta 
);

CREATE TABLE bibliotech.loans (
    id INTEGER PRIMARY KEY DEFAULT nextval('bibliotech.loans_id_seq'),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expected_return_date DATE NOT NULL,
    returned_at DATE,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'encerrado', 'atrasado')), 
    FOREIGN KEY (book_id) REFERENCES bibliotech.books(id),
    FOREIGN KEY (user_id) REFERENCES bibliotech.users(id),
    FOREIGN KEY (employee_id) REFERENCES bibliotech.employees(id),
    CONSTRAINT ck_loans_dates CHECK (expected_return_date > created_at::DATE) 
);

CREATE TABLE bibliotech.fines (
    id INTEGER PRIMARY KEY DEFAULT nextval('bibliotech.fines_id_seq'),
    loan_id INTEGER NOT NULL,
    value DECIMAL(10,2) NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE,
    payed_at DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'pago', 'cancelado')), 
    CONSTRAINT ck_fines_value CHECK (value > 0),
    FOREIGN KEY (loan_id) REFERENCES bibliotech.loans(id)
);
