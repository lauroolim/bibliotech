import psycopg2

def test_user_status():
    conn = psycopg2.connect(
        host='db',
        database='bibliotech', 
        user='admin',
        password='root',
        port=5432
    )
    
    cur = conn.cursor()
    
    # Verificar alguns usuários específicos
    cur.execute("SELECT id, username, is_active FROM bibliotech.users WHERE id IN (183, 184, 185) ORDER BY id")
    users = cur.fetchall()
    
    print("=== ESTADO ATUAL NO BANCO ===")
    for user in users:
        print(f"User {user[0]} ({user[1]}): is_active = {user[2]}")
    
    # Desativar usuário 183 diretamente
    print("\n=== DESATIVANDO USER 183 ===")
    cur.execute("UPDATE bibliotech.users SET is_active = FALSE WHERE id = 183")
    conn.commit()
    
    # Verificar novamente
    cur.execute("SELECT id, username, is_active FROM bibliotech.users WHERE id = 183")
    result = cur.fetchone()
    print(f"User 183 após update: is_active = {result[2]}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_user_status()