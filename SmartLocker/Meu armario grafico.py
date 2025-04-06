from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk

class Armario:
    def __init__(self, id_armario, esta_ocupado=False, id_usuario=None):
        self.__id_armario = id_armario
        self.__esta_ocupado = esta_ocupado
        self.__id_usuario = id_usuario

    def get_id_armario(self):
        return self.__id_armario
    
    def get_esta_ocupado(self):
        return self.__esta_ocupado
    
    def get_id_usuario(self):
        return self.__id_usuario
    
    def set_id_armario(self, id_armario):
        self.__id_armario = id_armario
    
    def set_esta_ocupado(self, esta_ocupado):
        self.__esta_ocupado = esta_ocupado
    
    def set_id_usuario(self, id_usuario):
        self.__id_usuario = id_usuario
    
    def adicionar_usuario(self, id_usuario):
        if not self.__esta_ocupado:
            self.__esta_ocupado = True
            self.__id_usuario = id_usuario
            return True
        return False
    
    def remover_usuario_armario(self):
        if self.__esta_ocupado:
            self.__esta_ocupado = False
            self.__id_usuario = None
            return True
        return False

class Usuario:
    def __init__(self, id_usuario, nome):
        self.__id_usuario = id_usuario
        self.__nome = nome

    def get_id_usuario(self):
        return self.__id_usuario
    
    def get_nome(self):
        return self.__nome
    
    def set_id_usuario(self, id_usuario):
        self.__id_usuario = id_usuario
    
    def set_nome(self, nome):
        self.__nome = nome

class SistemaDearmario:
    def __init__(self):
        self.__dicionario_armarios = {}
        self.__dicionario_usuarios = {}
        self.__arquivo_armarios = 'armarios.txt'
        self.carregar_dados()

    def criar_armario(self, id_armario):
        if id_armario not in self.__dicionario_armarios:
            self.__dicionario_armarios[id_armario] = Armario(id_armario)
            self.salvar_dados() 
            return True
        return False

    def excluir_armario(self, id_armario):
        if id_armario in self.__dicionario_armarios:
            del self.__dicionario_armarios[id_armario]
            self.salvar_dados()  
            return True
        return False

    def adicionar_usuario(self, id_usuario, nome):
        if id_usuario not in self.__dicionario_usuarios:
            self.__dicionario_usuarios[id_usuario] = Usuario(id_usuario, nome)
            self.salvar_dados() 
            return True 
        return False

    def excluir_usuario(self, id_usuario):
        if id_usuario in self.__dicionario_usuarios:
            del self.__dicionario_usuarios[id_usuario]
            self.salvar_dados()  
            return True
        return False

    def associar_usuario_ao_armario(self, id_usuario, id_armario):
        if id_usuario in self.__dicionario_usuarios and id_armario in self.__dicionario_armarios:
            if self.__dicionario_armarios[id_armario].adicionar_usuario(id_usuario):
                self.salvar_dados()  
                return True
            return False

    def liberar_armario(self, id_armario):
        if id_armario in self.__dicionario_armarios:
            if self.__dicionario_armarios[id_armario].remover_usuario_armario():
                self.salvar_dados()  
                return True
        return False

    def salvar_dados(self):
        try:
            with open(self.__arquivo_armarios, 'w') as arquivo: 
                # Primeiro salva os dados dos armários 
                arquivo.write("ARMARIOS:\n") # Marca o início do texto dos armarios
                for armario in self.__dicionario_armarios.values(): # Percorre por todos os armário que estao dentro do dicionário
                     # Salva o ID do armário, se está ocupado e o ID do usuário associado (se tiver, se não é false, padrao)
                    arquivo.write(f'{armario.get_id_armario()},{armario.get_esta_ocupado()},{armario.get_id_usuario()}\n')
                
                # Depois salva os dados dos usuários
                arquivo.write("\nUSUARIOS:\n")  # Marca o ininicio dos usuarios
                for usuario in self.__dicionario_usuarios.values(): # Mesma coisa que acima dos armarios
                    # Salva o ID e o nome do usuário
                    arquivo.write(f'{usuario.get_id_usuario()},{usuario.get_nome()}\n')
                    
        except FileNotFoundError:  
            with open(self.__arquivo_armarios, 'w'):
                print("Arquivo não encontrado, mas foi criado.") 

    def carregar_dados(self):
        try:
            with open(self.__arquivo_armarios, 'r') as arquivo:  
                conteudo = arquivo.read().splitlines() # ele le o conteudo do arquivo e divide em várias linhas, uma para cada linha do texto

                # varivel para ajudar a saber qual parte do arquivos estamos (armarios ou usuarios)
                leitura_armarios = False # Começamos não lendo armários
                leitura_usuarios = False # E nem lendo usuários ainda
                
                for linha in conteudo:
                    # Se a linha estiver escrita "ARMARIOS:", significa que apartir dai vamos ver os dados de armaios
                    if linha == "ARMARIOS:":
                        leitura_armarios = True
                        leitura_usuarios = False
                    
                    # Mesma coisa que o armario
                    elif linha == "USUARIOS:":
                        leitura_armarios = False
                        leitura_usuarios = True
                    
                     # leitura parte armario
                    elif leitura_armarios:
                        if linha.strip() and len(linha.strip().split(',')) == 3:
                            id_armario, esta_ocupado, id_usuario = linha.strip().split(',')
                            armario = Armario(id_armario, esta_ocupado == 'True', id_usuario if id_usuario != 'None' else None)
                            self.__dicionario_armarios[id_armario] = armario  
                   
                    # leitura parte usuario
                    elif leitura_usuarios:
                        # Verifica se a linha tem duas partes, porque o usuário tem apenas ID e nome
                        if linha.strip() and len(linha.strip().split(',')) == 2:
                            id_usuario, nome = linha.strip().split(',')  # Divide a linha em duas partes
                            # Criei um novo usuário com esses dados
                            usuario = Usuario(id_usuario, nome)
                            self.__dicionario_usuarios[id_usuario] = usuario  
        except FileNotFoundError:
            pass
        
        

class Minhainterface:
    def __init__(self):
        self.sistema = SistemaDearmario() # Instancia o sistema
        self.janela = Tk()  # Criação da janela principal
        self.janela.title("Sistema de armários")
        self.janela.geometry("800x700")
        self.menubar = Menu(self.janela) # Barra de menus
        self.janela.config(menu=self.menubar)
        self.opcoes_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Clique aqui para abrir as opções", menu=self.opcoes_menu)
        self.opcoes_menu.add_command(label="Adicionar Armário", command=self.add_armario)
        self.opcoes_menu.add_command(label="Excluir Armário", command=self.ex_armario)
        self.opcoes_menu.add_command(label="Adicionar Usuário", command=self.add_usuario)
        self.opcoes_menu.add_command(label="Excluir Usuário", command=self.ex_usuario)
        self.opcoes_menu.add_command(label="Associar armario e usuario", command=self.associar_armarioEusuario)
        self.opcoes_menu.add_command(label="Liberar armario", command=self.liberar_armario)
        self.opcoes_menu.add_command(label="Sair", command=self.sair)

        self.frame_tabelas = Frame(self.janela)  # Frame das tabelas que aparece na janela principal
        self.frame_tabelas.pack(pady=20)

        # Tabela de armarios que aparece na janela principal
        self.treeview_armarios = ttk.Treeview(self.frame_tabelas, columns=("ID", "Ocupado", "ID Usuario"), show="headings")
        self.treeview_armarios.heading("ID", text="ID Armario")
        self.treeview_armarios.heading("Ocupado", text="Ocupado")
        self.treeview_armarios.heading("ID Usuario", text="ID Usuario")
        self.treeview_armarios.pack()

        # Tabela de usuarios da janela principal
        self.treeview_usuarios = ttk.Treeview(self.frame_tabelas, columns=("ID", "Nome"), show="headings")
        self.treeview_usuarios.heading("ID", text="ID Usuario")
        self.treeview_usuarios.heading("Nome", text="Nome")
        self.treeview_usuarios.pack()

        self.atualizar_tabelas()    # atualiza as tabelas sozinho visualmente.

    def JanelaPOP_UP(self, mensagem):
        return simpledialog.askstring("Entrada", mensagem) # Solicita input via pop-up

    def mostrar_mensagem_popup(self, titulo, mensagem, erro=False):
        if erro:
            messagebox.showerror(titulo, mensagem) # Exibe mensagem de erro
        else:
            messagebox.showinfo(titulo, mensagem) # Exibe mensagem de sucesso ou outra coisa

    def add_armario(self):
        id_armario = self.JanelaPOP_UP("Digite o ID do Armario:")
        if id_armario and id_armario.isdigit():
            if self.sistema.criar_armario(id_armario):
                self.mostrar_mensagem_popup("Sucesso", "Armario foi adicionado.")
                self.atualizar_tabelas()
            else:
                self.mostrar_mensagem_popup("Falha", "ID ja existe, digite outro.", erro=True)
        else:
            self.mostrar_mensagem_popup("Erro", "ID do armario é aceito somente numeros.", erro=True)
    
    def ex_armario(self):
        id_armario = self.JanelaPOP_UP("Digite o ID do Armario para excluir:")
        if id_armario and id_armario.isdigit():
            if self.sistema.excluir_armario(id_armario):
                self.mostrar_mensagem_popup("Sucesso", "Armario excluido.")
                self.atualizar_tabelas()
            else:
                self.mostrar_mensagem_popup("Falha", "Armario não foi encontrado.", erro=True)
        else:
            self.mostrar_mensagem_popup("Erro", "ID do armario deve ser um numero.", erro=True)
    
    def add_usuario(self):
        id_usuario = self.JanelaPOP_UP("Digite o ID do Usuario:")
        nome_usuario = self.JanelaPOP_UP("Digite o nome do usuario:")
        
        # Verifica se os dois os dados foram informados antes de chamar o metodo
        if id_usuario.isdigit() and nome_usuario.isalpha():
            if self.sistema.adicionar_usuario(id_usuario, nome_usuario):
                self.mostrar_mensagem_popup("Sucesso", "Usuario foi adicionado.")
                self.atualizar_tabelas()
            else:
                self.mostrar_mensagem_popup("Falha", "ID de usuario já existe.", erro=True)
        else:
            self.mostrar_mensagem_popup("Erro", "ID do usuario deve ser um numero e o nome deve conter apenas letras.", erro=True)
    
    def ex_usuario(self):
        id_usuario = self.JanelaPOP_UP("Digite o ID do Usuario para excluir:")
        if self.sistema.excluir_usuario(id_usuario):
            self.mostrar_mensagem_popup("Sucesso", "Usuario excluído.")
            self.atualizar_tabelas()
        else:
            self.mostrar_mensagem_popup("Falha", "Usuario não foi encontrado.", erro=True)

    def associar_armarioEusuario(self):
        id_usuario = self.JanelaPOP_UP("Digite o ID do usuario:")
        id_armario = self.JanelaPOP_UP("Digite o ID do armário:")
        if self.sistema.associar_usuario_ao_armario(id_usuario, id_armario):
            self.mostrar_mensagem_popup("Sucesso", "Usuario associado ao armario.")
            self.atualizar_tabelas()
        else:
            self.mostrar_mensagem_popup("Falha", "Não foi possível associar o usuário ao armario.", erro=True)

    def liberar_armario(self):
        id_armario = self.JanelaPOP_UP("Digite o ID do Armario para liberar:")
        if self.sistema.liberar_armario(id_armario):
            self.mostrar_mensagem_popup("Sucesso", "Armario foi liberado.")
            self.atualizar_tabelas()
        else:
            self.mostrar_mensagem_popup("Falha", "Não foi possível liberar o armario.", erro=True)

    def atualizar_tabelas(self):
        # Atualiza tabela de armários
        for i in self.treeview_armarios.get_children():
            self.treeview_armarios.delete(i)
        for armario in self.sistema._SistemaDearmario__dicionario_armarios.values():
            self.treeview_armarios.insert("", "end", values=(armario.get_id_armario(), armario.get_esta_ocupado(), armario.get_id_usuario()))

        # Atualiza tabela de usuários
        for i in self.treeview_usuarios.get_children():
            self.treeview_usuarios.delete(i)
        for usuario in self.sistema._SistemaDearmario__dicionario_usuarios.values():
            self.treeview_usuarios.insert("", "end", values=(usuario.get_id_usuario(), usuario.get_nome()))

    def sair(self):
        self.janela.quit()

# Criando a interface
app = Minhainterface() # Cria a instância da interface
app.janela.mainloop() 
