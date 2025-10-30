import ttkbootstrap as tk
from db import Database 
class Diario:
    def __init__(self):
        self.display=tk.Window(themename="cyborg")
        self.display.geometry("1920x1080")
        self.display.title("Login")
        self.display.state("zoomed")
        self.display.resizable(True, True)
        self.tela()
        Database.create(self)
        

    def tela(self):
        tk.Label(self.display, text="Diário Godostories", font=("Arial", 40)).place(relx=0.5, rely=0.1, anchor="center")

        self.titulo=tk.Entry(self.display, width=20, font=("Arial", 20))
        self.titulo.place(relx=0.3, rely=0.3, anchor="center")

        tk.Label(self.display, text="Título", font=("Arial", 20)).place(relx=0.15, rely=0.3, anchor="center")
        tk.Label(self.display, text="Data", font=("Arial", 20)).place(relx=0.15, rely=0.38, anchor="center")
        tk.Label(self.display, text="Conteúdo", font=("Arial", 20)).place(relx=0.15, rely=0.54, anchor="center")
        
        self.data=tk.Entry(self.display, width=20, font=("Arial", 20))
        self.data.place(relx=0.3, rely=0.38, anchor="center")
        self.conteudo=tk.Text(self.display, width=20, height=5, font=("Arial", 20))
        self.conteudo.place(relx=0.3, rely=0.54, anchor="center")

        tk.Button(self.display, text="Salvar", width=10, padding=(20, 10), command=self.atualizar).place(relx=0.26, rely=0.7, anchor="center")
        tk.Button(self.display, text="Editar", width=10, padding=(20, 10)).place(relx=0.34, rely=0.7, anchor="center")
        tk.Button(self.display, text="Excluir", width=10, padding=(20, 10)).place(relx=0.26, rely=0.77, anchor="center")
        tk.Button(self.display, text="Buscar", width=10, padding=(20, 10)).place(relx=0.34, rely=0.77, anchor="center")

        self.tree = tk.Treeview(self.display,height=25, columns=("titulo", "data", "conteudo"),show="headings")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("data", text="Data")
        self.tree.heading("conteudo", text="Conteúdo")
        self.tree.insert("", "end", values=("AAAAAAAA", "2025-09-19"))
        self.tree.place(relx=0.7, rely=0.5, anchor="center")

    def limpar_tree(self):
        ids_dos_itens = self.tree.get_children() 
    
        for item_id in ids_dos_itens:
            self.tree.delete(item_id)

    def atualizar(self):
        titulo_get = self.titulo.get()
        data_get = self.data.get()
        conteudo_get = self.conteudo.get()

        if titulo_get and data_get and conteudo_get:
            Database.insert(titulo_get, data_get, conteudo_get)
    
    def inserir(self):
        pass
        
    
    

        
    def run(self):
        self.display.mainloop()


if __name__=="__main__":
    app = Diario()
    app.run()