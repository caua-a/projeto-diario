import sqlite3

class Database:
    def __init__(self, nome_banco="database.sqlite"):
        self.conn = sqlite3.connect(nome_banco)
        self.cursor = self.conn.cursor()


    def cria_tb(self):
        self.cursor.execute("""create table if not exists diario(
                            id integer primary key,
                            titulo text not null,
                            data date not null, 
                            conteudo text not null);
                                    """)
        self.conn.commit()
    
    def inserir_dados_db(self, titulo, data, conteudo):
        self.cursor.execute("""insert into diario(titulo, data, conteudo)
                            values (?, ?, ?);""", (titulo, data, conteudo))
        self.conn.commit()


    def listar_entrada_tb(self):
        try:
            self.cursor.execute("""select id, titulo, data, conteudo from diario order by id desc;""")
            entrada=self.cursor.fetchall()
        except sqlite3.Error:
            print(f"Erro ao listar entrada{sqlite3.Error}")
            entrada=None
        finally:
            self.conn.commit()
        return entrada
    


    def atualizar_entrada_db(self, id, titulo, data, conteudo):
        self.cursor.execute("""
            UPDATE diario SET titulo = ?, data = ?, conteudo = ? WHERE id = ?
        """, (titulo, data, conteudo, id))
        self.conn.commit()
    
    def exluir_dados(self, id_selecionado):
        self.cursor.execute("""delete from diario where id = ? ;""", (id_selecionado))
        self.conn.commit()