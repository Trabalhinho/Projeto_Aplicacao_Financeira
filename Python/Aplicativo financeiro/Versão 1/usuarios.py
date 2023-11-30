import pyodbc

class Usuarios(object):


    def __init__( self, dt_calendario = "", classificacao = "", localizacao = "", item = "", banco = "", fl_credito_debito = "", fl_entrada_saida = "", valor_total = "", qtde_parcelas = "" ):
        self.info = {}
        self.dt_calendario      =   dt_calendario     
        self.classificacao      =   classificacao     
        self.localizacao        =   localizacao       
        self.item               =   item              
        self.banco              =   banco             
        self.fl_credito_debito  =   fl_credito_debito 
        self.fl_entrada_saida   =   fl_entrada_saida  
        self.valor_total        =   valor_total       
        self.qtde_parcelas      =   qtde_parcelas     

    def insertUser( self ):

        try:

            conn = pyodbc.connect('Driver={SQL Server};'
                  r'Server=localhost\SQLEXPRESS;'
                  'Database=FINANCEIRO;'
                  'Trusted_Connection=yes;') #integrated security

            cursor = conn.cursor()

            SQLCommand = ("insert into stg_base_entradas_saidas_financas ( "
                        " dt_calendario     "
		                ",classificacao     "
		                ",localizacao       "
		                ",item              "
		                ",banco             "
		                ",fl_credito_debito "
		                ",fl_entrada_saida  "
		                ",valor_total       "
		                ",qtde_parcelas     "
            ")"
            "values"
            "('" + self.dt_calendario + "', '" + self.classificacao + "', '" + self.localizacao + "', '" + 
            self.item + "', '" + self.banco + "', '" + self.fl_credito_debito + "', '" + 
            self.fl_entrada_saida + "', '" + self.valor_total + "', '" + self.qtde_parcelas + "' )"
            )

            #Processing Query    
            cursor.execute( SQLCommand )

            conn.commit()
            print("Data Successfully Inserted")   
            conn.close()

            return "Usuário cadastrado com sucesso!"
        except:
            return "Ocorreu um erro na inserção do usuário"



        


        