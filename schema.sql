--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: fine_status; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.fine_status AS ENUM (
    'pendente',
    'pago'
);


ALTER TYPE public.fine_status OWNER TO admin;

--
-- Name: loan_status; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.loan_status AS ENUM (
    'ativo',
    'encerrado'
);


ALTER TYPE public.loan_status OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: _yoyo_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_log (
    id character varying(36) NOT NULL,
    migration_hash character varying(64),
    migration_id character varying(255),
    operation character varying(10),
    username character varying(255),
    hostname character varying(255),
    comment character varying(255),
    created_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_log OWNER TO admin;

--
-- Name: _yoyo_migration; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_migration (
    migration_hash character varying(64) NOT NULL,
    migration_id character varying(255),
    applied_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_migration OWNER TO admin;

--
-- Name: _yoyo_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_version (
    version integer NOT NULL,
    installed_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_version OWNER TO admin;

--
-- Name: books; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.books (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    isbn character varying(20) NOT NULL
);


ALTER TABLE public.books OWNER TO admin;

--
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.books_id_seq OWNER TO admin;

--
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    cpf character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active character varying(20) NOT NULL,
    email character varying(20) NOT NULL,
    password character varying(64) NOT NULL
);


ALTER TABLE public.employees OWNER TO admin;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.employees_id_seq OWNER TO admin;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: fines; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.fines (
    id integer NOT NULL,
    loan_id integer NOT NULL,
    value double precision NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status public.fine_status DEFAULT 'pendente'::public.fine_status NOT NULL
);


ALTER TABLE public.fines OWNER TO admin;

--
-- Name: fines_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.fines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fines_id_seq OWNER TO admin;

--
-- Name: fines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.fines_id_seq OWNED BY public.fines.id;


--
-- Name: loans; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.loans (
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deadline timestamp without time zone NOT NULL,
    return_date timestamp without time zone NOT NULL,
    book_id integer NOT NULL,
    user_id integer NOT NULL,
    employee_id integer NOT NULL,
    status public.loan_status DEFAULT 'ativo'::public.loan_status NOT NULL
);


ALTER TABLE public.loans OWNER TO admin;

--
-- Name: loans_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.loans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.loans_id_seq OWNER TO admin;

--
-- Name: loans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.loans_id_seq OWNED BY public.loans.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.users OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: yoyo_lock; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.yoyo_lock (
    locked integer DEFAULT 1 NOT NULL,
    ctime timestamp without time zone,
    pid integer NOT NULL
);


ALTER TABLE public.yoyo_lock OWNER TO admin;

--
-- Name: books id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: fines id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.fines ALTER COLUMN id SET DEFAULT nextval('public.fines_id_seq'::regclass);


--
-- Name: loans id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.loans ALTER COLUMN id SET DEFAULT nextval('public.loans_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: _yoyo_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public._yoyo_log (id, migration_hash, migration_id, operation, username, hostname, comment, created_at_utc) FROM stdin;
78d7c042-3904-11f0-9d04-0242ac150003	80510822f0581325b712dfa4614052dccd909c3bee347dcd8f8984ad4e9593b4	20250525_03_BBWHd	apply	root	34c4ffb35c69	\N	2025-05-25 01:06:21.860821
6d9af548-3907-11f0-a59c-0242ac150003	033148d44d6c2cce568ba85a9c3be4fe1c67d92bf0f0ac7ba7f593416cb8640f	20250525_04_pRpsc	apply	root	34c4ffb35c69	\N	2025-05-25 01:27:31.502097
bfe65b62-3907-11f0-8b93-0242ac150003	6f39f33f4f8d6421026653b39bb2611c6281a9dd6d44a0923a22bdeb268e5641	20250525_05_oHOaC	apply	root	34c4ffb35c69	\N	2025-05-25 01:29:49.560924
74ac3634-390d-11f0-a966-0242ac150003	f6f8a5a4daeffb151945c2a96640d33a74f5fc134ab424d1a85da35a1ef8e470	20250525_06_kp2Rh	apply	root	34c4ffb35c69	\N	2025-05-25 02:10:40.331814
de03ac12-3911-11f0-86c2-0242ac150003	6b7cd74298c6c50a96a6d656fc1cf76ad989fdf2a08371a3492b268533caa54b	20250525_07_RKXvR	apply	root	34c4ffb35c69	\N	2025-05-25 02:42:15.051546
\.


--
-- Data for Name: _yoyo_migration; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public._yoyo_migration (migration_hash, migration_id, applied_at_utc) FROM stdin;
80510822f0581325b712dfa4614052dccd909c3bee347dcd8f8984ad4e9593b4	20250525_03_BBWHd	2025-05-25 01:06:21.868241
033148d44d6c2cce568ba85a9c3be4fe1c67d92bf0f0ac7ba7f593416cb8640f	20250525_04_pRpsc	2025-05-25 01:27:31.508676
6f39f33f4f8d6421026653b39bb2611c6281a9dd6d44a0923a22bdeb268e5641	20250525_05_oHOaC	2025-05-25 01:29:49.567794
f6f8a5a4daeffb151945c2a96640d33a74f5fc134ab424d1a85da35a1ef8e470	20250525_06_kp2Rh	2025-05-25 02:10:40.337571
6b7cd74298c6c50a96a6d656fc1cf76ad989fdf2a08371a3492b268533caa54b	20250525_07_RKXvR	2025-05-25 02:42:15.057763
\.


--
-- Data for Name: _yoyo_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public._yoyo_version (version, installed_at_utc) FROM stdin;
2	2025-05-25 00:52:35.372608
\.


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.books (id, title, author, created_at, isbn) FROM stdin;
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.employees (id, username, cpf, created_at, is_active, email, password) FROM stdin;
3	admin	12345678901	2025-05-25 02:46:24.285781	true	admin@bibliotech.com	a115236c51dd5498e7683f79d9de387c842f70c258f69719855184ed54ecea56
5	admin	12345678910	2025-05-25 02:49:35.804884	true	admin@bibliotech.com	f67cac44e560c6cfdef77e10b85dffe816b0870bd9dccb9f892d8ed8158d7875
\.


--
-- Data for Name: fines; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.fines (id, loan_id, value, created_at, status) FROM stdin;
\.


--
-- Data for Name: loans; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.loans (id, created_at, deadline, return_date, book_id, user_id, employee_id, status) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, username, password, email, created_at) FROM stdin;
1	testuser_20250524165203	securehash123	test_20250524165203@example.com	2025-05-24 16:52:03.638536
2	testuser_20250524165850	securehash123	test_20250524165850@example.com	2025-05-24 16:58:50.302601
3	teste1	a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3	teste@teste.com	2025-05-24 17:00:40.65733
4	teste2	a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3	teste2@teste.com	2025-05-24 19:15:38.888219
5	teste3	a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3	teste3@teste.com	2025-05-24 19:39:48.233885
6	teste5	a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3	teste5@teste.com	2025-05-24 23:08:44.206202
7	criadonaareadeadmin	a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3	teste7@teste.com	2025-05-25 04:28:19.428968
\.


--
-- Data for Name: yoyo_lock; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.yoyo_lock (locked, ctime, pid) FROM stdin;
\.


--
-- Name: books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.books_id_seq', 1, false);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.employees_id_seq', 5, true);


--
-- Name: fines_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.fines_id_seq', 1, false);


--
-- Name: loans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.loans_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- Name: _yoyo_log _yoyo_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_log
    ADD CONSTRAINT _yoyo_log_pkey PRIMARY KEY (id);


--
-- Name: _yoyo_migration _yoyo_migration_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_migration
    ADD CONSTRAINT _yoyo_migration_pkey PRIMARY KEY (migration_hash);


--
-- Name: _yoyo_version _yoyo_version_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_version
    ADD CONSTRAINT _yoyo_version_pkey PRIMARY KEY (version);


--
-- Name: books books_isbn_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_isbn_key UNIQUE (isbn);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: fines fines_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.fines
    ADD CONSTRAINT fines_pkey PRIMARY KEY (id);


--
-- Name: loans loans_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_pkey PRIMARY KEY (id);


--
-- Name: employees unique_employees_cpf; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT unique_employees_cpf UNIQUE (cpf);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: yoyo_lock yoyo_lock_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.yoyo_lock
    ADD CONSTRAINT yoyo_lock_pkey PRIMARY KEY (locked);


--
-- Name: idx_books_isbn; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_books_isbn ON public.books USING btree (isbn);


--
-- Name: fines fines_loan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.fines
    ADD CONSTRAINT fines_loan_id_fkey FOREIGN KEY (loan_id) REFERENCES public.loans(id);


--
-- Name: loans loans_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id);


--
-- Name: loans loans_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- Name: loans loans_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

