alter procedure spr_entradas_saidas_financas
as begin try

	declare	@etapa_processo	varchar(max)

	if object_id( 'tbl_base_entradas_saidas_financas' ) is null
		create table tbl_base_entradas_saidas_financas
		(
			 dt_calendario		date
			,classificacao		varchar(100)	collate latin1_general_ci_ai
			,localizacao		varchar(500)	collate latin1_general_ci_ai
			,item				varchar(500)	collate latin1_general_ci_ai
			,banco				varchar(100)	collate latin1_general_ci_ai
			,fl_credito_debito	varchar(100)	collate latin1_general_ci_ai
			,fl_entrada_saida	varchar(100)	collate latin1_general_ci_ai
			,valor_total		float
			,qtde_parcelas		int
		)
		
	if object_id( 'tbl_base_carteira' ) is null
		create table tbl_base_carteira
		(
			 classificacao	varchar(100)	collate latin1_general_ci_ai
			,valor_total	float
		)

	if object_id( 'tbl_aux_gastos_credito' ) is null
		create table tbl_aux_gastos_credito
		(
			 dt_calendario			date
			,classificacao			varchar(100)	collate latin1_general_ci_ai
			,item					varchar(100)	collate latin1_general_ci_ai
			,banco					varchar(100)	collate latin1_general_ci_ai
			,fl_primeiro_pagamento	tinyint
			,valor_parcela			float
			,valor_total			float
			,qtde_parcelas			int
		)

		


	
	--	=================================================================================================
	set	@etapa_processo	=	'Backups'
	--	=================================================================================================
		
	drop table if exists tbl_base_entradas_saidas_financas_bkp_proc

	select	*
	into	tbl_base_entradas_saidas_financas_bkp_proc
	from	tbl_base_entradas_saidas_financas
		
	drop table if exists tbl_base_carteira_bkp_proc

	select	*
	into	tbl_base_carteira_bkp_proc
	from	tbl_base_carteira
		
	drop table if exists tbl_aux_gastos_credito_bkp_proc

	select	*
	into	tbl_aux_gastos_credito_bkp_proc
	from	tbl_aux_gastos_credito
	


	
	--	=================================================================================================
	set	@etapa_processo	=	'Tabela auxiliar de fechamento da fatura do cartão de cada banco.'
	--	=================================================================================================
		
	drop table if exists tbl_aux_vencimento_fatura_banco
	
	create table tbl_aux_vencimento_fatura_banco
	(
		 dia	int
		,banco	varchar(100)	collate latin1_general_ci_ai
	)

	insert into tbl_aux_vencimento_fatura_banco values
	 (	20	,'NuBank'			)
	,(	3	,'PicPay'			)
	

	

	--	=================================================================================================
	set	@etapa_processo	=	'Tabela auxiliar de classificação.'
	--	=================================================================================================
	
	drop table if exists #tmp_aux_classificacao

	create table #tmp_aux_classificacao
	(
		 classificacao_detalhe	varchar(100)	collate latin1_general_ci_ai
		,classificacao_agrupada	varchar(100)	collate latin1_general_ci_ai
	)
	
	insert into #tmp_aux_classificacao values
	 (	'Jogos'			,'Mensal'			)
	,(	'Livros'		,'Mensal'			)
	,(	'Rolê'			,'Mensal'			)
	,(	'Celular'		,'Mensal'			)
	,(	'Suplemento'	,'Mensal'			)
	,(	'Mensal'		,'Mensal'			)
	,(	'Empréstimo'	,'Reserva geral'	)
	,(	'Reserva geral'	,'Reserva geral'	)
	,(	'Investimento'	,'Investimento'		)
	,(	'Computador'	,'Computador'		)
	,(	'Casa'			,'Casa'				)
	,(	'Carro'			,'Carro'			)
	,(	'Videogame'		,'Videogame'		)
	,(	'Presente'		,'Presente'			)
	,(	'Viagem'		,'Viagem'			)
	



	--	=================================================================================================
	set	@etapa_processo	=	'Insere os dados de classificação na tabela de carteira.'
	--	=================================================================================================
	
	insert into tbl_base_carteira
	select	classificacao	=	b.classificacao
			,valor_total	=	0
	from	tbl_base_carteira	a
		right join	tbl_distribuicao_salario_vigencia	b
			on	a.classificacao	=	b.classificacao
	where	a.classificacao	is null


	--	=================================================================================================
	set	@etapa_processo	=	'Carrega os dados da origem.'
	--	=================================================================================================
	
	drop table if exists #tmp_entradas_saidas_financas

	select	 dt_calendario		=	convert( date,	a.dt_calendario	)
			,classificacao		=	a.classificacao	
			,localizacao		=	a.localizacao	
			,item				=	a.item			
			,banco				=	a.banco			
			,fl_credito_debito	=	a.fl_credito_debito
			,fl_entrada_saida	=	a.fl_entrada_saida
			,valor_total		=	convert( float,	replace( a.valor_total, ',', '.' ) )
			,qtde_parcelas		=	convert( int,	a.qtde_parcelas	)
	into	#tmp_entradas_saidas_financas
	from	stg_base_entradas_saidas_financas	a
	



	--	=================================================================================================
	set	@etapa_processo	=	'Insere os dados na tabela analítica.'
	--	=================================================================================================
	
	delete	a
	from	#tmp_entradas_saidas_financas	a
		join	tbl_base_entradas_saidas_financas	b
			on	a.dt_calendario		=	b.dt_calendario
			and	a.classificacao		=	b.classificacao
			and	a.localizacao		=	b.localizacao
			and	a.item				=	b.item
			and	a.banco				=	b.banco
			and	a.fl_credito_debito	=	b.fl_credito_debito
			and	a.fl_entrada_saida	=	b.fl_entrada_saida
			and	a.valor_total		=	b.valor_total
			and	a.qtde_parcelas		=	b.qtde_parcelas

	insert into tbl_base_entradas_saidas_financas
	select	 a.dt_calendario	
			,a.classificacao	
			,a.localizacao	
			,a.item			
			,a.banco			
			,a.fl_credito_debito
			,a.fl_entrada_saida
			,a.valor_total	
			,a.qtde_parcelas	
	from	#tmp_entradas_saidas_financas	a
	



	--	=================================================================================================
	set	@etapa_processo	=	'Insere novas classificações na tabela de carteira.'
	--	=================================================================================================

	insert into tbl_base_carteira
	select	 classificacao	=	isnull( b.classificacao_agrupada, a.classificacao )
			,valor_total	=	0
	from	#tmp_entradas_saidas_financas	a
		join		#tmp_aux_classificacao	b
			on	a.classificacao	=	b.classificacao_detalhe
		left join	tbl_base_carteira	c
			on	c.classificacao	=	b.classificacao_agrupada	
	where	c.classificacao	is null
		and	a.classificacao	<>	'Salário'
		and	a.classificacao	<>	'Fatura do cartão'
		


	--	=================================================================================================
	set	@etapa_processo	=	'Insere os dados de Crédito na tabela auxiliar de gastos por Crédito.'
	--	=================================================================================================

	insert into tbl_aux_gastos_credito
	select	 a.dt_calendario
			,a.classificacao
			,a.item
			,a.banco
			,fl_primeiro_pagamento	=	1
			,valor_parcela			=	( a.valor_total / a.qtde_parcelas )
			,a.valor_total
			,a.qtde_parcelas
	from	#tmp_entradas_saidas_financas	a
		left join	tbl_aux_gastos_credito	b
			on	a.dt_calendario	=	b.dt_calendario
			and	a.classificacao	=	b.classificacao
			and	a.item			=	b.item
			and	a.banco			=	b.banco
			and	a.valor_total	=	b.valor_total
			and	a.qtde_parcelas	=	b.qtde_parcelas
	where	a.fl_credito_debito	=	'Crédito'
		and	a.fl_entrada_saida	=	'Saída'
		and	b.dt_calendario		is null
		
	


	--	=================================================================================================
	set	@etapa_processo	=	'Separa os itens que serão pagos.'
	--	=================================================================================================

	drop table if exists #tmp_itens_pagos_credito

	select	 a.classificacao
			,a.valor_parcela
	into	#tmp_itens_pagos_credito
	from	tbl_aux_gastos_credito		a
		join	#tmp_entradas_saidas_financas	b
			on	a.banco					=	b.banco
		join	tbl_aux_vencimento_fatura_banco	c
			on	a.banco					=	c.banco
			and	(	day( a.dt_calendario )	<	c.dia
				or	a.fl_primeiro_pagamento	=	0
				)
	where	b.classificacao	=	'Fatura do cartão'
	
	


	--	=================================================================================================
	set	@etapa_processo	=	'Separa os itens que serão pagos.'
	--	=================================================================================================

	if( select count(1) from #tmp_entradas_saidas_financas a where a.classificacao = 'Fatura do cartão' ) > 0
	begin

		declare	@soma_itens_pagos_credito	float	=	(
			select isnull( sum( a.valor_parcela ), 0 ) from #tmp_itens_pagos_credito a
		)

		declare	@valor_total_fatura_cartao	float	=	(
			select isnull( sum( a.valor_total ), 0 ) from #tmp_entradas_saidas_financas a where a.classificacao = 'Fatura do cartão'
		)

		declare	@diferenca					float	=	@valor_total_fatura_cartao - @soma_itens_pagos_credito

		if @diferenca <> 0
		begin

			insert into #tmp_itens_pagos_credito values
			( 'Mensal', @diferenca )

		end
	
	end



	--	=================================================================================================
	set	@etapa_processo	=	'Atualiza os dados de parcelas restantes.'
	--	=================================================================================================

	update	a
	set		a.qtde_parcelas	=	a.qtde_parcelas - 1
	from	tbl_aux_gastos_credito		a
		join	#tmp_entradas_saidas_financas	b
			on	a.banco		=	b.banco
		join	tbl_aux_vencimento_fatura_banco	c
			on	a.banco					=	c.banco
			and	(	day( a.dt_calendario )	<	c.dia
				or	a.fl_primeiro_pagamento	=	0
				)
	where	b.classificacao	=	'Fatura do cartão'
	



	--	=================================================================================================
	set	@etapa_processo	=	'Atualiza a flag de primeiro pagamento.'
	--	=================================================================================================

	update	a
	set		a.fl_primeiro_pagamento	=	0
	from	tbl_aux_gastos_credito		a
		join	#tmp_entradas_saidas_financas	b
			on	a.banco		=	b.banco
		join	tbl_aux_vencimento_fatura_banco	c
			on	a.banco					=	c.banco
	where	b.classificacao	=	'Fatura do cartão'
	



	--	=================================================================================================
	set	@etapa_processo	=	'Deleta os gastos no cartão que já foram pagas todas as parcelas.'
	--	=================================================================================================

	delete	a
	from	tbl_aux_gastos_credito		a
	where	a.qtde_parcelas	=	0
	



	--	=================================================================================================
	set	@etapa_processo	=	'Soma os valores a serem subtraídos da carteira do Crédito.'
	--	=================================================================================================
	
	drop table if exists #tmp_valores_saidas_credito
	
	select	 classificacao	=	b.classificacao_agrupada
			,valor_total	=	sum( a.valor_parcela )
	into	#tmp_valores_saidas_credito
	from	#tmp_itens_pagos_credito	a
		join	#tmp_aux_classificacao	b
			on	a.classificacao	=	b.classificacao_detalhe
	group by b.classificacao_agrupada



	--	=================================================================================================
	set	@etapa_processo	=	'Subtrai os valores de pagamento de fatura no cartão de suas respectivas classificações.'
	--	=================================================================================================

	update	a
	set		a.valor_total	=	a.valor_total	-	b.valor_total
	from	tbl_base_carteira	a
		join	#tmp_valores_saidas_credito	b
			on	a.classificacao	=	b.classificacao
			



	--	=================================================================================================
	set	@etapa_processo	=	'Soma os valores a serem subtraídos da carteira.'
	--	=================================================================================================
	
	drop table if exists #tmp_valores_saidas
	
	select	 classificacao	=	b.classificacao_agrupada
			,valor_total	=	sum( a.valor_total )
	into	#tmp_valores_saidas
	from	#tmp_entradas_saidas_financas	a
		join	#tmp_aux_classificacao	b
			on	a.classificacao	=	b.classificacao_detalhe
	where	a.fl_entrada_saida	=	'Saída'
		and	a.fl_credito_debito	<>	'Crédito'
		and	a.classificacao		<>	'Fatura do cartão'
	group by b.classificacao_agrupada




	--	=================================================================================================
	set	@etapa_processo	=	'Subtrai os valores de pagamento de suas respectivas classificações.'
	--	=================================================================================================

	update	a
	set		a.valor_total	=	a.valor_total	-	b.valor_total
	from	tbl_base_carteira	a
		join	#tmp_valores_saidas	b
			on	b.classificacao	=	a.classificacao
		



	--	=================================================================================================
	set	@etapa_processo	=	'Soma os valores a serem adicionados na carteira.'
	--	=================================================================================================
	
	drop table if exists #tmp_valores_entradas
	
	select	 classificacao	=	b.classificacao_agrupada
			,valor_total	=	sum( a.valor_total )
	into	#tmp_valores_entradas
	from	#tmp_entradas_saidas_financas	a
		join	#tmp_aux_classificacao	b
			on	a.classificacao	=	b.classificacao_detalhe
	where	a.fl_entrada_saida	=	'Entrada'
		and	a.classificacao		<>	'Salário'
	group by b.classificacao_agrupada





	--	=================================================================================================
	set	@etapa_processo	=	'Soma os valores de entradas em suas respectivas classificações.'
	--	=================================================================================================

	update	a
	set		a.valor_total	=	a.valor_total	+	b.valor_total
	from	tbl_base_carteira	a
		join	#tmp_valores_entradas	b
			on	a.classificacao	=	b.classificacao
	



	--	=================================================================================================
	set	@etapa_processo	=	'Soma os valores do salário a serem adicionados na carteira.'
	--	=================================================================================================
	
	drop table if exists #tmp_valores_entradas_salario
	
	select	 a.dt_calendario
			,classificacao	=	'Salário'
			,valor_total	=	sum( a.valor_total )
	into	#tmp_valores_entradas_salario
	from	#tmp_entradas_saidas_financas	a
	--		join	#tmp_aux_classificacao	b
	--			on	a.classificacao	=	b.classificacao_detalhe
	where	a.fl_entrada_saida	=	'Entrada'
		and	a.classificacao		=	'Salário'
	group by a.dt_calendario




	--	=================================================================================================
	set	@etapa_processo	=	'Calcula a distribuição de salário com valores percentuais.'
	--	=================================================================================================
	
	update	a
	set		a.valor_total	=	a.valor_total + ( sum( b.valor_total ) * c.percentual )
	from	tbl_base_carteira	a
		join	#tmp_valores_entradas_salario	b
			on	b.classificacao		=	'Salário'
		join	tbl_distribuicao_salario_vigencia	c
			on	b.dt_calendario	between	c.dt_inicio and c.dt_fim
			and	c.classificacao		=	a.classificacao
	where	c.fl_valor_percentual	=	'percentual'




	--	=================================================================================================
	set	@etapa_processo	=	'Calcula a distribuição de salário com valores percentuais.'
	--	=================================================================================================

	truncate table stg_base_entradas_saidas_financas


end try
begin catch

	select	@etapa_processo

end catch






