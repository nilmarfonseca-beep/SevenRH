import sqlite3

conexao = sqlite3.connect("Clientes.db")


cursor = conexao.cursor()

cursor.execute(
    """
        CREATE TABLE Cliente(
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

cursor.close()
