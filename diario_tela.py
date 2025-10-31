import ttkbootstrap as tk
import db
class Diario:
    def __init__(self):
        self.display=tk.Window(themename="cyborg")
        self.display.geometry("1920x1080")
        self.display.title("Login")
        self.display.state("zoomed")
        self.display.resizable(True, True)
        self.tela()
        self.db_manager = db.Database()
        self.db_manager.cria_tb()
        self.carregar_dados()
        

    def tela(self):
        tk.Label(self.display, text="Diário Godostories", font=("Arial", 40)).place(relx=0.5, rely=0.1, anchor="center")

        self.titulo=tk.Entry(self.display, width=20, font=("Arial", 20))
        self.titulo.place(relx=0.3, rely=0.3, anchor="center")

        tk.Label(self.display, text="Título", font=("Arial", 20)).place(relx=0.15, rely=0.3, anchor="center")
        tk.Label(self.display, text="Data", font=("Arial", 20)).place(relx=0.15, rely=0.38, anchor="center")
        tk.Label(self.display, text="Conteúdo", font=("Arial", 20)).place(relx=0.15, rely=0.54, anchor="center")
        
        self.data=tk.DateEntry(self.display, bootstyle="info")
        self.data.place(relx=0.3, rely=0.38, anchor="center", width=455)
        self.conteudo=tk.Text(self.display, width=20, height=5, font=("Arial", 20))
        self.conteudo.place(relx=0.3, rely=0.54, anchor="center")
        self.buscar=tk.Entry(self.display, width=20,font=("arial", 20))
        self.buscar.place(relx=0.7, rely=0.2, anchor="center")

        tk.Button(self.display, text="Salvar", width=10, padding=(20, 10), command=self.salvar).place(relx=0.26, rely=0.7, anchor="center")
        tk.Button(self.display, text="Editar", width=10, padding=(20, 10), command=self.editar).place(relx=0.34, rely=0.7, anchor="center")
        tk.Button(self.display, text="Excluir", width=10, padding=(20, 10), command=self.excluir).place(relx=0.26, rely=0.77, anchor="center")
        tk.Button(self.display, text="Buscar", width=4, padding=(20, 10), command=self.buscar).place(relx=0.86, rely=0.2, anchor="center")

        self.tree = tk.Treeview(self.display,height=25, columns=("titulo", "data", "conteudo"),show="headings")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("titulo", text="Título")
        self.tree.heading("data", text="Data")
        self.tree.heading("conteudo", text="Conteúdo")
        self.tree.place(relx=0.7, rely=0.6, anchor="center")
        self.tree.bind('<<TreeviewSelect>>', self.selecionar_item)


    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        entradas = self.db_manager.listar_entrada_tb()
        if entradas:
            for i in entradas:
                db_id = i[0]
                colunas=i[1:]
                self.tree.insert(parent="", index="end",iid=db_id, values=colunas)
            print("Atualização certa")
        else:
            print("Sem atualização")
                
        

    def salvar(self):
        titulo = self.titulo.get()
        data = self.data.get_date()
        conteudo = self.conteudo.get("1.0", tk.END + "-1c")

        if titulo and conteudo:
            self.db_manager.inserir_dados_db(titulo, data, conteudo)
            print("nova entrada salva com sucesso!")
            self.carregar_dados()
            self.limpar_campos()
        else:
            print("preencha todos os campos antes de salvar")

    


    def selecionar_item(self, event):
        self.limpar_campos()
        item_selecionado_id = self.tree.focus()  # pega o iid (que agora é o id do banco)

        if item_selecionado_id:
            self.id_selecionado = int(item_selecionado_id)
            valores = self.tree.item(item_selecionado_id, "values")

            self.titulo.insert(0, valores[0])
            self.data.entry.delete(0, tk.END)
            self.data.entry.insert(0, valores[1])
            self.conteudo.insert("1.0", valores[2])
        else:
            self.id_selecionado = None

    def excluir(self):
            if not hasattr(self, 'id_selecionado') or not self.id_selecionado:
                print("Nenhum item selecionado")
                return  
            self.db_manager.excluir_dados(self.id_selecionado)
            self.carregar_dados()

    def editar(self):
        if not hasattr(self, 'id_selecionado') or not self.id_selecionado:
            print("Nenhum item selecionado")
            return

        titulo_editado = self.titulo.get()
        data_editada = self.data.get_date()
        conteudo_editado = self.conteudo.get("1.0", tk.END + "-1c") 

        if titulo_editado and conteudo_editado:
            self.db_manager.atualizar_entrada_db(self.id_selecionado, titulo_editado, data_editada, conteudo_editado)
            print(f"ID {self.id_selecionado} atualizado ")
        else:
            print("Os campos estão vazios")
            
        self.carregar_dados()

    def limpar_campos(self):
         self.titulo.delete(0, tk.END)
         self.conteudo.delete('1.0', tk.END)
         self.data.entry.delete(0, tk.END)
    
    def buscar(self):
            
        termo = self.titulo.get().strip()  # usa o campo de título como filtro

        # limpa a Treeview antes de mostrar resultados
        for item in self.tree.get_children():
            self.tree.delete(item)

        # se não digitou nada, recarrega todos os dados
        if not termo:
            self.carregar_dados()
            return

        # filtra os dados que já estão no banco
        resultados = self.db_manager.listar_entrada_tb()
        resultados_filtrados = [r for r in resultados if termo.lower() in r[1].lower()]

        for r in resultados_filtrados:
            self.tree.insert(parent="", index="end", iid=r[0], values=r[1:])

        print(f"{len(resultados_filtrados)} resultado(s) encontrado(s).")

    def run(self):
        self.display.mainloop()


if __name__=="__main__":
    app = Diario()
    app.run()