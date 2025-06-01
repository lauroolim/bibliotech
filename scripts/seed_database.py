from faker import Faker
import psycopg2
from datetime import date, timedelta
import random
fake = Faker('pt_BR')

DB_CONFIG = {
    'host': 'db',  
    'database': 'bibliotech',
    'user': 'admin',
    'password': 'root',
    'port': 5432
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erro ao conectar no banco: {e}")
        exit(1)

def clear_database(conn):
    cur = conn.cursor()
    print("Limpando dados existentes...")
    
    tables = [
        'bibliotech.fines',
        'bibliotech.loans', 
        'bibliotech.books_authors',
        'bibliotech.books',
        'bibliotech.users',
        'bibliotech.employees',
        'bibliotech.authors'
    ]
    
    for table in tables:
        cur.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE")
    
    conn.commit()
    cur.close()
    print("Dados limpos!")

def generate_unique_username(used_usernames):
    while True:
        username = fake.user_name()
        if username not in used_usernames:
            used_usernames.add(username)
            return username

def generate_unique_email(used_emails):
    while True:
        email = fake.email()
        if email not in used_emails:
            used_emails.add(email)
            return email

def generate_unique_isbn(used_isbns):
    while True:
        isbn = fake.isbn13()
        if isbn not in used_isbns:
            used_isbns.add(isbn)
            return isbn

def generate_unique_cpf(used_cpfs):
    while True:
        cpf = fake.cpf().replace('.', '').replace('-', '')
        if cpf not in used_cpfs:
            used_cpfs.add(cpf)
            return cpf

def seed_all_data(conn):
    cur = conn.cursor()
    
    used_usernames = set()
    used_emails = set()
    used_isbns = set()
    used_cpfs = set()
    
    print("Inserindo autores...")
    authors = []
    for _ in range(50):
        cur.execute("INSERT INTO bibliotech.authors (full_name) VALUES (%s) RETURNING id", (fake.name(),))
        authors.append(cur.fetchone()[0])
    
    print("👥 Inserindo usuários...")
    users = []
    for i in range(100):
        username = generate_unique_username(used_usernames)
        email = generate_unique_email(used_emails)
        
        cur.execute("""
            INSERT INTO bibliotech.users (username, password, email, phone, created_at, is_active) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """, (username, fake.password(), email, fake.phone_number(), fake.date_between(start_date='-2y'), True))
        users.append(cur.fetchone()[0])
    
    print("Inserindo funcionários...")
    employees = []
    for i in range(10):
        username = generate_unique_username(used_usernames)
        email = generate_unique_email(used_emails)
        cpf = generate_unique_cpf(used_cpfs)
        hired_date = fake.date_between(start_date='-3y')
        
        cur.execute("""
            INSERT INTO bibliotech.employees (username, cpf, created_at, hired_at, password, is_active, email) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (username, cpf, hired_date, hired_date, fake.password(), True, email))
        employees.append(cur.fetchone()[0])
    
    print("Inserindo livros...")
    books = []
    for _ in range(200):
        isbn = generate_unique_isbn(used_isbns)
        
        cur.execute("""
            INSERT INTO bibliotech.books (title, isbn, publish_year) 
            VALUES (%s, %s, %s) RETURNING id
        """, (fake.catch_phrase(), isbn, fake.year()))
        book_id = cur.fetchone()[0]
        books.append(book_id)
        
        book_authors = random.sample(authors, random.randint(1, 3))
        for author_id in book_authors:
            cur.execute("INSERT INTO bibliotech.books_authors (book_id, author_id) VALUES (%s, %s)", (book_id, author_id))
    
    print("Inserindo empréstimos...")
    loans = []
    used_book_user_pairs = set()  
    
    for _ in range(150):
        attempts = 0
        while attempts < 50: 
            user_id = random.choice(users)
            book_id = random.choice(books)
            
            if (user_id, book_id) not in used_book_user_pairs:
                used_book_user_pairs.add((user_id, book_id))
                break
            attempts += 1
        
        employee_id = random.choice(employees)
        created_at = fake.date_time_between(start_date='-6m')
        expected_return = created_at.date() + timedelta(days=14)
        
        if random.random() < 0.7:
            returned_at = fake.date_between(start_date=expected_return - timedelta(days=5), end_date=expected_return + timedelta(days=10))
            status = 'encerrado'
        else:
            returned_at = None
            status = 'atrasado' if expected_return < date.today() else 'ativo'
        
        cur.execute("""
            INSERT INTO bibliotech.loans (created_at, expected_return_date, returned_at, book_id, user_id, employee_id, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (created_at, expected_return, returned_at, book_id, user_id, employee_id, status))
        loans.append(cur.fetchone()[0])
    
    print("Inserindo multas...")
    for loan_id in loans:
        if random.random() < 0.3:  
            value = round(random.uniform(5.0, 50.0), 2)
            status = random.choice(['pendente', 'pago', 'cancelado'])
            payed_at = fake.date_this_month() if status == 'pago' else None
            
            cur.execute("INSERT INTO bibliotech.fines (loan_id, value, status, payed_at) VALUES (%s, %s, %s, %s)", 
                       (loan_id, value, status, payed_at))
    
    conn.commit()
    cur.close()
    
    return len(authors), len(users), len(employees), len(books), len(loans)

def main():
    print("Iniciando seed do banco de dados...")
    conn = get_db_connection()
    
    clear = input("Limpar dados existentes? (y/N): ").lower()
    if clear in ['y', 'yes', 's', 'sim']:
        clear_database(conn)
    
    try:
        authors, users, employees, books, loans = seed_all_data(conn)
        
        print("\nSeed concluído!")
        print(f"Resumo:")
        print(f"   - {authors} autores")
        print(f"   - {users} usuários") 
        print(f"   - {employees} funcionários")
        print(f"   - {books} livros")
        print(f"   - {loans} empréstimos")
        
    except Exception as e:
        print(f"Erro: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()