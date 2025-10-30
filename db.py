import sqlite3

class Database:
    def __init__(self, nome_banco="database.sqlite"):
        self.conn = sqlite3.connect(nome_banco)
        self.cursor = self.conn.cursor()


    def create(self):
        self.cursor.execute("""create table if not exists diario(
                            id integer autoincrement primary key,
                            titulo text not null unique,
                            data date not null,
                            conteudo text not null)
""")
        self.conn.commit()
    
    def insert(self, titulo, data, conteudo):
        self.cursor.execute("""insert into diario(titulo, data, conteudo)
                            values (?, ?, ?) """, (titulo, data, conteudo))
        self.conn.commit