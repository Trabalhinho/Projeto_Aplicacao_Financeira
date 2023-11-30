from inserir_Dados_Banco import inserir_Dados
import tkinter
import tkinter.messagebox
import customtkinter
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
from tkinter import *

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        opcaoClassificacao              = ['Mensal', 'Livros', 'Jogos', 'Rolê', 'Celular', 'Empréstimo', 'Fatura do cartão', 'Salário',
                                            'Suplemento', 'Investimento', 'Reserva geral', 'Computador', 'Casa', 'Carro', 'Videogame', 'Presente', 'Viagem']
        opcaoClassificacaoOrdenada      = sorted( opcaoClassificacao )

        opcaoBanco                      =   [ 'NuBank', 'PicPay', 'Itaú', 'Players Bank', 'Méliuz', 'Mercado Pago', 'PagBank']
        opcaoBancoOrdenada              = sorted( opcaoBanco )

        selected_date   = StringVar()

        ###########################################################
        # Configurações da janela
        ###########################################################
        self.title("Aplicativo financeiro")
        self.geometry(f"{1300}x{780}")

        fonte_customizada = customtkinter.CTkFont(family="arial", size=14)

        ###########################################################
        # Configurações da grade do layout (4x4)
        ###########################################################
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        ###########################################################
        # Criação da barra lateral 
        ###########################################################
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Guias", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Entradas/Saídas", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Empréstimos", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Modo de exibição:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Escala de UI:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        ###########################################################
        # Linha 0 Coluna 1
        ###########################################################
        
        # Cria o frame para escolhas
        self.grupo_linha_0_coluna_1 = customtkinter.CTkFrame(self)
        self.grupo_linha_0_coluna_1.grid(row=0, column=1, padx=(20, 10), pady=(20, 0), sticky="nsew")

        # Calendário
        self.label_calendario = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_1, text="Data", font=fonte_customizada)
        self.label_calendario.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="sw")
        self.calendario = DateEntry(self.grupo_linha_0_coluna_1, date_pattern='dd/MM/yyyy', width=15, font=fonte_customizada, 
                                           #fieldbackground='#f9c821', foreground='#111111', background='#999999',
                                           textvariable=selected_date)
        self.calendario.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        
        # Cria as opções de classificação
        self.label_opcao_classificacao = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_1, text="Classificação", font=fonte_customizada)
        self.label_opcao_classificacao.grid(row=2, column=0, columnspan=1, padx=10, pady=(20, 10), sticky="sw")
        self.opcao_classificacao = customtkinter.CTkOptionMenu(self.grupo_linha_0_coluna_1, dynamic_resizing=False, width=200,
                                                               values=opcaoClassificacaoOrdenada, font=fonte_customizada)
        self.opcao_classificacao.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

        # Cria as opções de banco
        self.label_opcao_banco = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_1, text="Banco", font=fonte_customizada)
        self.label_opcao_banco.grid(row=4, column=0, columnspan=1, padx=10, pady=(20, 10), sticky="sw")
        self.opcao_banco = customtkinter.CTkOptionMenu(self.grupo_linha_0_coluna_1, dynamic_resizing=False, width=200,
                                                               values=opcaoBancoOrdenada, font=fonte_customizada)
        self.opcao_banco.grid(row=5, column=0, padx=10, pady=10, sticky="nw")
        
        # Classifica se é entrada ou saída
        self.var_radio_entrada_saida = tkinter.StringVar(value="Entrada")
        self.label_radio_entrada_saida = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_1, text="Entrada ou Saída?", font=fonte_customizada)
        self.label_radio_entrada_saida.grid(row=6, column=0, columnspan=1, padx=10, pady=(20, 10), sticky="sw")
        self.btn_1_radio_entrada_saida = customtkinter.CTkRadioButton(master=self.grupo_linha_0_coluna_1, variable=self.var_radio_entrada_saida, 
                                                                      value="Entrada", text="Entrada", font=fonte_customizada)
        self.btn_1_radio_entrada_saida.grid(row=7, column=0, pady=10, padx=10, sticky="nw")
        self.btn_2_radio_entrada_saida = customtkinter.CTkRadioButton(master=self.grupo_linha_0_coluna_1, variable=self.var_radio_entrada_saida, 
                                                                      value="Saída", text="Saída", font=fonte_customizada)
        self.btn_2_radio_entrada_saida.grid(row=8, column=0, pady=10, padx=10, sticky="nw")

        # Classifica se é crédito ou débito
        self.var_radio_credito_debito = tkinter.StringVar(value="Débito")
        self.label_radio_credito_debito = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_1, text="Débito ou Crédito?", font=fonte_customizada)
        self.label_radio_credito_debito.grid(row=9, column=0, columnspan=1, padx=10, pady=(20, 10), sticky="sw")
        self.btn_1_radio_credito_debito = customtkinter.CTkRadioButton(master=self.grupo_linha_0_coluna_1, variable=self.var_radio_credito_debito, 
                                                                       value="Débito", text="Débito", font=fonte_customizada)
        self.btn_1_radio_credito_debito.grid(row=10, column=0, pady=10, padx=10, sticky="nw")
        self.btn_2_radio_credito_debito = customtkinter.CTkRadioButton(master=self.grupo_linha_0_coluna_1, variable=self.var_radio_credito_debito, 
                                                                       value="Crédito", text="Crédito", font=fonte_customizada)
        self.btn_2_radio_credito_debito.grid(row=11, column=0, pady=10, padx=10, sticky="nw")

        ###########################################################
        # Linha 0 Coluna 2
        ###########################################################
        
        # Cria o frame para textos
        self.grupo_linha_0_coluna_2 = customtkinter.CTkFrame(self)
        self.grupo_linha_0_coluna_2.grid(row=0, column=2, padx=(10, 10), pady=(20, 0), sticky="nsew")

        # Define a entrada para localização
        self.label_entrada_localizacao = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_2, text="Localização", font=fonte_customizada)
        self.label_entrada_localizacao.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="sw")
        self.entrada_localizacao = customtkinter.CTkEntry(self.grupo_linha_0_coluna_2, placeholder_text="Exemplo: UOL",
                                                          width=300, font=fonte_customizada)
        self.entrada_localizacao.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

        # Define a entrada para item
        self.label_entrada_item = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_2, text="Item", font=fonte_customizada)
        self.label_entrada_item.grid(row=2, column=1, columnspan=1, padx=10, pady=(20, 10), sticky="w")
        self.entrada_item = customtkinter.CTkTextbox(self.grupo_linha_0_coluna_2, bg_color='#343638',
                                                   width=300, height=150, font=fonte_customizada)
        self.entrada_item.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Define a entrada para valor
        self.label_entrada_valor = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_2, text="Valor", font=fonte_customizada)
        self.label_entrada_valor.grid(row=4, column=1, columnspan=1, padx=10, pady=(20, 10), sticky="sw")
        self.entrada_valor = customtkinter.CTkEntry(self.grupo_linha_0_coluna_2, placeholder_text="R$", width=300, font=fonte_customizada)
        self.entrada_valor.grid(row=5, column=1, padx=10, pady=10, sticky="nw")

        # Define a entrada para quantidade de parcelas
        self.label_entrada_parcela = customtkinter.CTkLabel(master=self.grupo_linha_0_coluna_2, text="Quantidade de parcelas", font=fonte_customizada)
        self.label_entrada_parcela.grid(row=6, column=1, columnspan=1, padx=10, pady=(20, 10), sticky="w")
        self.entrada_parcela = customtkinter.CTkEntry(self.grupo_linha_0_coluna_2, placeholder_text="Parcelas", width=300, font=fonte_customizada)
        self.entrada_parcela.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        ###########################################################
        # Linha 1 Coluna 2
        ###########################################################
        
        # Cria o frame para textos
        self.grupo_linha_1_coluna_2 = customtkinter.CTkFrame(self, fg_color="transparent")
        self.grupo_linha_1_coluna_2.grid(row=1, column=2, padx=(10, 10), pady=(20, 0), sticky="nsew")

        # create main entry and button
        self.checkbox_criar_outro = customtkinter.CTkCheckBox(master=self.grupo_linha_1_coluna_2, text="Criar outro", font=fonte_customizada)
        self.checkbox_criar_outro.grid(row=1, column=1, pady=(20, 0), padx=20, sticky="ne")

        self.btn_inserir_dados = customtkinter.CTkButton(master=self.grupo_linha_1_coluna_2, fg_color="transparent", border_width=2, 
                                                         text="Inserir dados", text_color=("gray10", "#DCE4EE"), font=fonte_customizada,
                                                         command=self.inserir_dados_funcao)
        self.btn_inserir_dados.grid(row=1, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        ###########################################################
        # Define os valores padrão
        ###########################################################
        
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.opcao_classificacao.set("Mensal")
        self.opcao_banco.set("NuBank")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("Em construção")

    # Função para selecionar a data
    def selecionar_data():
        # Cria uma nova janela
        top = Toplevel(app)

        # Cria um objeto de calendário
        calendario = Calendar(top, selectmode='day', date_pattern='dd/MM/yyyy')

        # Função que é chamada quando uma data é selecionada
        def set_data():
            selected_date.set(calendario.selection_get())
            top.destroy()

        # Cria um botão para selecionar a data
        botao = ttk.Button(top, text="Selecionar data", command=set_data)

        # Exibe o calendário e o botão
        calendario.pack( pady = 10 )
        botao.pack( pady = 10 )
        
    # Função para chamar o script de inserção dos dados no banco
    def inserir_dados_funcao( self ):
        
        dados = inserir_Dados()
    
        dados.dt_calendario      = self.calendario.get()
        dados.classificacao      = self.opcao_classificacao.get()
        dados.localizacao        = self.entrada_localizacao.get()
        dados.item               = self.entrada_item.get("0.0", "end")
        dados.banco              = self.opcao_banco.get()
        dados.fl_credito_debito  = self.var_radio_credito_debito.get()
        dados.fl_entrada_saida   = self.var_radio_entrada_saida.get()
        dados.valor_total        = self.entrada_valor.get()
        dados.qtde_parcelas      = self.entrada_parcela.get()
    
        print(dados.insert())
        
        if self.checkbox_criar_outro.get() == 1:
            self.entrada_item.delete( "0.0", "end" )
            self.entrada_valor.delete( 0, END )
        
        else:
            self.calendario.delete( 0, END )
            self.opcao_classificacao.set("Mensal")
            self.entrada_localizacao.delete( 0, END )
            self.entrada_item.delete( "0.0", "end" )
            self.opcao_banco.set("NuBank")
            self.var_radio_credito_debito.set( "Débito" )
            self.var_radio_entrada_saida.set( "Entrada" )
            self.entrada_valor.delete( 0, END )
            self.entrada_parcela.delete( 0, END )
    


if __name__ == "__main__":
    app = App()
    app.mainloop()