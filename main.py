import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import date

class BackEnd():
    def conecta_db(self):
        #conecta ao banco
        self.conn = sqlite3.connect("colaboradores.db")
        #o cursor permite andarmos dentro do banco de dados
        self.cursor = self.conn.cursor()

    def desconecta_db(self):
        # desconecta o banco de dados
        self.conn.close()

    def cria_tabela(self):
        #chama o banco de dados
        self.conecta_db()
        #vamos alterar ou criar entao chamamos o cursor
        self.cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS USERS (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, 
            Username TEXT NOT NULL, 
            Email TEXT NOT NULL, 
            Pass TEXT NOT NULL,
            Conf_pass TEXT NOT NULL
            );
        """)
        self.conn.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS MATERIAIS ( 
        ITEM TEXT NOT NULL, 
        OSR INTEGER PRIMARY KEY
        );""")
        self.conn.commit()

        self.desconecta_db()
    def verifica_login(self):
        #referenciando variaveis
        self.user_email = self.username_login_entry.get()
        self.pass_log = self.pass_login_entry.get()
        #CHAMANDO BD
        self.conecta_db()
        #Entrando no BD
        self.cursor.execute("""
        SELECT * FROM USERS WHERE Email = ? AND Pass = ?
        """, (self.user_email, self.pass_log))
        #Percorrendo BD para achar variaveis
        self.verifica_dados = self.cursor.fetchone()
        try:
            
            if(self.user_email=="" or self.pass_log ==""):
                messagebox.showwarning(title='ERRO', message='Preencha todos os campos! ')
            elif(self.verifica_dados is not None and self.user_email == self.verifica_dados[2] and self.pass_log == self.verifica_dados[3]):
                messagebox.showinfo(title="CONECTADO", message="LOGIN FEITO COM SUCESSO!")
                self.desconecta_db()
                self.menu()

        except Exception as e:
            messagebox.showerror(title="ERRO!", message="USUARIO / SENHA INCORRETOS \nOU\n"
                "COLABORADOR NAO REGISTRADO! ")

            self.desconecta_db()
    def cadastro_user(self):
        #Recebendo dados para jogar na tabela!
        self.username = self.username_cadastro_entry.get()
        self.email = self.email_entry.get()
        self.pass_bd  = self.pass_cadastro_entry.get()
        self.conf_pass = self.pass_conf_entry.get()
        #Testa as entradas do usuario, so liberando o cadastro se tudo estiver ok
        try:
            if (self.username == "" or self.email =="" or self.pass_bd == "" or self.conf_pass == ""):
                messagebox.showwarning(title='ERRO', message='Preencha todos os campos!')
            elif(len(self.username) < 4):
                messagebox.showwarning(title='ERRO!', message='O Username deve conter no MINIMO 4 CARACTERES.')
            elif(len(self.pass_bd) < 4):
                messagebox.showwarning(title='ERRO!', message='A senha deve conter MAIS de 4 CARACTERES.')
            elif(self.pass_bd != self.conf_pass):
                messagebox.showwarning(title='ERRO!', message='As senhas nao sao IGUAIS! ')
            else:
                # 1- Devemos Chamar o bd
                self.conecta_db()
                # Converter dados para a tabela USERS
                self.cursor.execute("""
                        INSERT INTO USERS(Username, Email, Pass, Conf_pass)
                        VALUES (?, ?, ?, ?)""", (self.username, self.email, self.pass_bd, self.conf_pass))
                #estamos comitando para o bd os dados recebidos
                self.conn.commit()
                messagebox.showinfo(title='SISTEMA DE CADASTRO!', message=f"SEJA MUITO BEM VINDO ! {self.username}!\n"
                f" Seu Cadastro Foi Realizado Com Sucesso!")
                self.desconecta_db()


        except:
            messagebox.showwarning(title='ERRO!', message='ERRO ao cadastrar usuario !\n Tente novamente! \n Se o '
            'ERRO continuar contate o SUPORTE DE TI!!!')
            self.desconecta_db()

    def retirando(self):
         #criar um variavel que receba os itens
         self.os_bd = self.os_menu.get()
         self.item_bd = self.item_menu.get()
         #CHAMAR BD
         self.conecta_db()
         # referenciar oq vamos adicionar
         self.cursor.execute("""
         INSERT INTO MATERIAIS (ITEM, OSR) 
         VALUES (?,?)""", (self.item_bd, self.os_bd))
         self.conn.commit()
         messagebox.showinfo(title='Retirada', message='Item retirado com sucesso! ')
         self.desconecta_db()
         print(f'O item retirado foi {self.item_bd}, que segue a OSR {self.os_bd}')


# vai abrir nossa tela
class App(ctk.CTk, BackEnd):
    # da inicio e tudo tem que esta aqui dentro
    def __init__(self):
        super().__init__()
        self.ConfigTela()
        self.tela_de_login()
        self.cria_tabela()
        self.username_cadastro_entry = None


    #Front AND !
    def ConfigTela(self):
        self.geometry("700x400")
        self.title("SISTEMA DE LOGIN PCP")
        self.resizable(False, False)
    # funcao para criar e modelar img
    def tela_de_login(self):
        #declarando img
        self.img = PhotoImage(file="transferir.png")
        #Chamando a imagem em uma Label
        self.label_img = ctk.CTkLabel(self, text=None, image=self.img)
        #moldando
        self.label_img.grid(row=1, column=0, padx=10)
        #Criando titulo
        self.title = ctk.CTkLabel(self, text="LOGIN SISTEMA PCP", font=("Century Gothic bold", 14))
        #posicionando o title
        self.title.grid(row=0, column=0, pady=10, padx=10)

        #Criando um Frame
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        #pocisionando
        self.frame_login.place(x=350, y=10)

        #Criando e colocando Wiggets no frame de login
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faca o seu login".upper(), font=("Arial", 22))
        #posicionando
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        #caixa de login
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome: ", font=("Century Gothic bold", 16),
        corner_radius=15, border_color="Green")
        #posicionando
        self.username_login_entry.grid(row=1, column=0, pady=10, padx=10)
        #caixa de senha
        self.pass_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu senha", font=("Century Gothic bold", 16),
        corner_radius=15, border_color="Green", show="*")
        #posicionando
        self.pass_login_entry.grid(row=2, column=0, pady=10, padx=10)
        #criando um check box para senha
        self.see_pass = ctk.CTkCheckBox(self.frame_login, text="Clique para ver senha", font=("Century Gothic bold", 12))
        #posicionando
        self.see_pass.grid(row=3, column=0, pady=10, padx=10)
        #criando um botao
        self.button_login = ctk.CTkButton(self.frame_login, width=300, fg_color="Green", text="LOGIN",
        font=("Century Gothic bold", 16), corner_radius=20, command=self.verifica_login)
        #posicionar
        self.button_login.grid(row=4, column=0, pady=10, padx=10)
        #cadastro text
        self.span = ctk.CTkLabel(self.frame_login, text="Cadastre-se logo abaixo!".upper(), font=("Century Gothic bold", 16))
        #posicionando text cads
        self.span.grid(row=5, column=0, pady=10, padx=10)
        #Criando button cad
        self.button_cadastro = ctk.CTkButton(self.frame_login, width=300,fg_color="Green",
        text="CADASTRO", font=("Century Gothic bold", 16), corner_radius=20, command=self.tela_de_cadastro)
        #posicionando
        self.button_cadastro.grid(row=6, column=0, pady=10, padx=10)

    def tela_de_cadastro(self):
        # Remover o formulario de login
        self.frame_login.place_forget()
        #Criando um Frame_cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        #posicionando
        self.frame_cadastro.place(x=350, y=10)
        # criando Title de cadastro
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="cadastro".upper(),
        font=("Arial Black", 22))
        # posicionando
        self.lb_title.grid(row=0, column=0, pady=5, padx=10)
        # widgets da tela de cadastro !
        # cadastro nome
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300,
        placeholder_text="Seu nome para o cadastro: ", font=("Arial", 16), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, pady=5, padx=10)
        #caixa para email
        self.email_entry = ctk.CTkEntry(self.frame_cadastro, width=300,
        placeholder_text="Digite seu melhor EMAIL:", font=("Arial", 15), corner_radius=15)
        #posiciona
        self.email_entry.grid(row=2, column=0, pady=5, padx=10)
        # senha cadastro
        self.pass_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300,
        placeholder_text="Digite uma senha: ", font=("Arial", 15), corner_radius=15, show="*")
        #posicionando
        self.pass_cadastro_entry.grid(row=3, column=0, pady=5, padx=10)
        #confirma senha
        self.pass_conf_entry = ctk.CTkEntry(self.frame_cadastro, width=300,
        placeholder_text="Confirme sua senha: ", font=("Arial", 15), corner_radius=15, show="*")
        #posiciona
        self.pass_conf_entry.grid(row=4, column=0, pady=5, padx=10)
        # criando um check box para senha
        self.see_pass_cad = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver senha",
        font=("Century Gothic bold", 12))
        # posicionando
        self.see_pass_cad.grid(row=5, column=0, pady=5, padx=10)
        # criando botoes
        self.button_cad= ctk.CTkButton(self.frame_cadastro, width=300,
        text="cadastrar".upper(), fg_color='Green', font=('Arial', 16), corner_radius=20,
        command=self.cadastro_user)
        # posicionar
        self.button_cad.grid(row=6, column=0, pady=5, padx=10)
        self.button_return = ctk.CTkButton(self.frame_cadastro, width=300,
        text="retornar menu".upper(), fg_color='Green', font=('Arial', 16), corner_radius=20,
        command=self.tela_de_login)
        #posicionar
        self.button_return.grid(row=7, column=0, pady=5, padx=10)

    def delete_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.pass_cadastro_entry.delete(0, END)
        self.pass_conf_entry.delete(0, END)

    def delete_login(self):
        self.username_login_entry.delete(0, END)
        self.pass_login_entry.delete(0, END)

    def menu(self):
        #vamos comecar removendo a tela de login e abrir nossa tela de menu !
        self.frame_login.place_forget()
        #criano meu frame menu
        self.menu_frame = ctk.CTkFrame(self, width=350, height=380)
        #posicionano menu_frame
        self.menu_frame.place(x=350, y=10)
        #title menu
        self.menu_title = ctk.CTkLabel(self.menu_frame, text='menu'.upper(), font=('Arial Black', 22))
        #posicionando
        self.menu_title.grid(row=0, column=0, pady=5, padx=10)
        #Qual o numero da OS que esta sendo retirada a peca
        self.os_menu = ctk.CTkEntry(self.menu_frame, width=300, placeholder_text='Numero da OSR: ',
        font=('Arial', 15), corner_radius=15)
        #posicionando
        self.os_menu.grid(row=1, column=0, pady=5, padx=10)
        #Item que esta sendo retirado
        self.item_menu = ctk.CTkEntry(self.menu_frame, width=300, placeholder_text='Qual o item? : ',
        font=("Arial", 15), corner_radius=15)
        #posicionano
        self.item_menu.grid(row=2, column=0, pady=5, padx=10)
        #botao para registrar saida de materiais
        self.register_mt = ctk.CTkButton(self.menu_frame, width=300, text='Registrar retirada!'.upper(),
        font=('Arial Black', 14), corner_radius=15, command=self.retirando)
        #posicionando
        self.register_mt.grid(row=3, column=0, pady=5, padx=10)
        #Botao para retornar ao menu !
        self.logout = ctk.CTkButton(self.menu_frame, width=300, text='logout'.upper(),
        font=('Arial', 15), corner_radius=15, command=self.tela_de_login)
        #posicionando
        self.logout.grid(row=4, column=0, pady=5, padx=10)





if __name__ == "__main__":
    app = App()
    app.mainloop()

'''elif(self.user in self.verifica_dados and self.pass_log in self.verifica_dados):
                messagebox.showinfo(title="CONECTADO", message="LOGIN FEITO COM SUCESSO!")
                self.desconecta_db()
                self.menu()'''