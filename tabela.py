import sqlite3
import bcrypt
from funcoes import psycopg2

conexao = sqlite3.connect("Clientes.db")

cursor = conexao.cursor()

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS Cliente(
            ID_Cliente INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Carimbo TEXT,
            Autorizo TEXT NOT NULL,
            Cpf TEXT NOT NULL UNIQUE,
            Nome TEXT NOT NULL,
            Cep TEXT NOT NULL,
            Endereco TEXT NOT NULL,
            Complemento TEXT NOT NULL,
            Bairro TEXT NOT NULL,
            Cidade TEXT NOT NULL,
            Uf TEXT NOT NULL,
            Nascimento TEXT NOT NULL,
            Idade INTEGER NOT NULL,
            Email TEXT NOT NULL,
            Telefone TEXT,
            Contato TEXT,
            Pagamento TEXT NOT NULL,
            Origem TEXT
            )
    """
)

#    conn = psycopg2.connect("dbname=meubanco user=meuuser password=1234")


cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL 
            
        );
    """                
)

    # Cria hash da senha inicial

password = "Meire1369"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


    # Insere usuário admin se não existir
cursor.execute("""
        INSERT INTO usuarios (username, password_hash)
        VALUES (?, ?)
        ON CONFLICT (username) DO NOTHING;
    """, ("Meire", hashed)
)

conexao.commit()
conexao.close()
cursor.close()
