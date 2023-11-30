from usuarios import Usuarios
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import pyodbc


class Application:
    
    def __init__( self, master = None ):

        opcaoClassificacao              = ['Mensal', 'Livros', 'Jogos', 'Rolê', 'Celular', 'Empréstimo', 'Fatura do cartão', 'Salário',
                                            'Suplemento', 'Investimento', 'Reserva geral', 'Computador', 'Casa', 'Carro', 'Videogame', 'Presente', 'Viagem']
        opcaoClassificacaoOrdenada      = sorted( opcaoClassificacao )
        opcaoSelecionadaClassificacao   = StringVar()

        opcaoBanco                      =   [ 'NuBank', 'PicPay', 'Itaú', 'Players Bank', 'Méliuz', 'Mercado Pago', 'PagBank']
        opcaoBancoOrdenada              = sorted( opcaoBanco )
        opcaoSelecionadaBanco           = StringVar()

        opcaoCreditoDebito              = [ 'Crédito', 'Débito' ]
        opcaoCreditoDebitoOrdenada      = sorted( opcaoCreditoDebito )
        opcaoSelecionadaCreditoDebito   = StringVar()
        
        opcaoEntradaSaida               = [ 'Entrada', 'Saída' ]
        opcaoEntradaSaidaOrdenada       = sorted( opcaoEntradaSaida )
        opcaoSelecionadaEntradaSaida    = StringVar()

        selected_date   = StringVar()

        self.fonte = ( "Verdana", "8" )
    
        self.container1             = Frame( master )
        self.container1["padx"]     = 20
        self.container1["pady"]     = 5
        self.container1.pack()

        self.container2             = Frame( master )
        self.container2["padx"]     = 20
        self.container2["pady"]     = 5
        self.container2.pack()

        self.container3             = Frame( master )
        self.container3["padx"]     = 20
        self.container3["pady"]     = 5
        self.container3.pack()
        
        self.container4             = Frame( master )
        self.container4["padx"]     = 20
        self.container4["pady"]     = 5
        self.container4.pack()
        
        self.container5             = Frame( master )
        self.container5["padx"]     = 20
        self.container5["pady"]     = 5
        self.container5.pack()
        
        self.container6             = Frame( master )
        self.container6["padx"]     = 20
        self.container6["pady"]     = 5
        self.container6.pack()
        
        self.container7             = Frame( master )
        self.container7["padx"]     = 20
        self.container7["pady"]     = 5
        self.container7.pack()
        
        self.container8             = Frame( master )
        self.container8["padx"]     = 20
        self.container8["pady"]     = 5
        self.container8.pack()
        
        self.container9             = Frame( master )
        self.container9["padx"]     = 20
        self.container9["pady"]     = 5
        self.container9.pack()
        
        self.container10            = Frame( master )
        self.container10["padx"]    = 20
        self.container10["pady"]    = 5
        self.container10.pack()
        
        self.container11            = Frame( master )
        self.container11["padx"]    = 20
        self.container11["pady"]    = 5
        self.container11.pack()
        
        self.container12            = Frame( master )
        self.container12["padx"]     = 20
        self.container12["pady"]     = 5
        self.container12.pack()
    
        self.titulo         = Label( self.container1, text = "Informe os dados:" )
        self.titulo["font"] = ( "Calibri", "9", "bold" )
        self.titulo.pack()
    
        self.lbl_dt_calendario = Label( self.container2, text = "Data:", font = self.fonte, width = 10 )
        self.lbl_dt_calendario.pack( side = LEFT )

        self.txt_dt_calendario           = DateEntry(self.container2, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy', textvariable=selected_date)
        self.txt_dt_calendario["width"]  = 10
        self.txt_dt_calendario["font"]   = self.fonte
        self.txt_dt_calendario.pack( side = LEFT )
    
        self.lbl_classificacao = Label( self.container3, text = "Classificação:", font = self.fonte, width = 10 )
        self.lbl_classificacao.pack( side = LEFT )
    
        self.txt_classificacao = ttk.Combobox( self.container3, font = self.fonte, width = 10, textvariable = opcaoSelecionadaClassificacao, values = opcaoClassificacaoOrdenada )
        self.txt_classificacao.pack( side = LEFT )
    
        self.lbl_localizacao = Label( self.container4, text = "Localização:", font = self.fonte, width = 10 )
        self.lbl_localizacao.pack( side = LEFT )
    
        self.txt_localizacao            = Entry( self.container4 )
        self.txt_localizacao["width"]   = 25
        self.txt_localizacao["font"]    = self.fonte
        self.txt_localizacao.pack( side = LEFT )
    
        self.lbl_item   = Label( self.container5, text = "Item:", font = self.fonte, width = 10 )
        self.lbl_item.pack( side = LEFT )
    
        self.txt_item           = Entry( self.container5 )
        self.txt_item["width"]  = 25
        self.txt_item["font"]   = self.fonte
        self.txt_item.pack( side = LEFT )
    
        self.lbl_banco = Label( self.container6, text = "Banco:", font = self.fonte, width = 10 )
        self.lbl_banco.pack( side = LEFT )
    
        self.txt_banco = ttk.Combobox( self.container6, font = self.fonte, width = 10, textvariable = opcaoSelecionadaBanco, values = opcaoBancoOrdenada )
        self.txt_banco.pack( side = LEFT )
    
        self.lbl_fl_credito_debito   = Label( self.container7, text = "Credito ou Debito?", font = self.fonte, width = 20 )
        self.lbl_fl_credito_debito.pack( side = LEFT )
    
        self.txt_fl_credito_debito = ttk.Combobox( self.container7, font = self.fonte, width = 10, textvariable = opcaoSelecionadaCreditoDebito, values = opcaoCreditoDebitoOrdenada )
        self.txt_fl_credito_debito.pack( side = LEFT )

        self.lbl_fl_entrada_saida   = Label( self.container8, text = "Entrada ou Saida?", font = self.fonte, width = 20 )
        self.lbl_fl_entrada_saida.pack( side = LEFT )
    
        self.txt_fl_entrada_saida = ttk.Combobox( self.container8, font = self.fonte, width = 10, textvariable = opcaoSelecionadaEntradaSaida, values = opcaoEntradaSaidaOrdenada )
        self.txt_fl_entrada_saida.pack( side = LEFT )

        self.lbl_valor_total   = Label( self.container9, text = "Valor total:", font = self.fonte, width = 20 )
        self.lbl_valor_total.pack( side = LEFT )
    
        self.txt_valor_total           = Entry( self.container9 )
        self.txt_valor_total["width"]  = 25
        self.txt_valor_total["font"]   = self.fonte
        self.txt_valor_total.pack( side = LEFT )
    
        self.lbl_qtde_parcelas   = Label( self.container10, text = "Qtde de parcelas:", font = self.fonte, width = 20 )
        self.lbl_qtde_parcelas.pack( side = LEFT )
    
        self.txt_qtde_parcelas           = Entry( self.container10 )
        self.txt_qtde_parcelas["width"]  = 25
        self.txt_qtde_parcelas["font"]   = self.fonte
        self.txt_qtde_parcelas.pack( side = LEFT )

        self.bntInsert              = Button( self.container11, text = "Inserir", font = self.fonte, width = 12 )
        self.bntInsert["command"]   = self.inserirUsuario
        self.bntInsert.pack ( side = LEFT )
    
        self.lbl_msg         = Label( self.container12, text="" )
        self.lbl_msg["font"] = ( "Verdana", "9", "italic" )
        self.lbl_msg.pack()
    
    
    def inserirUsuario( self ):
        """
        user = Usuarios()
    
        user.dt_calendario      = self.txt_dt_calendario.get()
        user.classificacao      = self.txt_classificacao.get()
        user.localizacao        = self.txt_localizacao.get()
        user.item               = self.txt_item.get()
        user.banco              = self.txt_banco.get()
        user.fl_credito_debito  = self.txt_fl_credito_debito.get()
        user.fl_entrada_saida   = self.txt_fl_entrada_saida.get()
        user.valor_total        = self.txt_valor_total.get()
        user.qtde_parcelas      = self.txt_qtde_parcelas.get()
    
        self.lbl_msg["text"] = user.insertUser()
        """
        self.txt_dt_calendario.delete( 0, END )
        self.txt_classificacao.delete( 0, END )
        self.txt_localizacao.delete( 0, END )
        self.txt_item.delete( 0, END )
        self.txt_banco.delete( 0, END )
        self.txt_fl_credito_debito.delete( 0, END )
        self.txt_fl_entrada_saida.delete( 0, END )
        self.txt_valor_total.delete( 0, END )
        self.txt_qtde_parcelas.delete( 0, END )
    

    # Função que é chamada quando o botão é clicado
    def selecionar_data():
        # Cria uma nova janela
        top = Toplevel(root)

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
        
root = Tk()
Application( root )
root.mainloop()