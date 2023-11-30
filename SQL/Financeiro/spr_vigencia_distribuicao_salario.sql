alter procedure spr_vigencia_distribuicao_salario
as begin try

	declare	@etapa_processo	varchar(max)

	drop table if exists tbl_distribuicao_salario_vigencia
	create table tbl_distribuicao_salario_vigencia
	(
		 dt_inicio				date
		,dt_fim					date
		,classificacao			varchar(100)	collate latin1_general_ci_ai
		,fl_valor_percentual	varchar(100)	collate latin1_general_ci_ai
		,valor					float
		,percentual				float
	)

	drop table if exists tbl_distribuicao_salario
	create table tbl_distribuicao_salario
	(
		 dt_calendario			date
		,classificacao			varchar(100)	collate latin1_general_ci_ai
		,fl_valor_percentual	varchar(100)	collate latin1_general_ci_ai
		,valor					float
		,percentual				float
	)
	
	insert into tbl_distribuicao_salario values
	 (	'2020-01-01'	,'Investimento'		,'percentual'	,0		,0.28	)
	,(	'2020-01-01'	,'Mensal'			,'percentual'	,0		,0.32	)
	,(	'2020-01-01'	,'Reserva geral'	,'percentual'	,0		,0.06	)
	,(	'2020-01-01'	,'Computador'		,'percentual'	,0		,0.05	)
	,(	'2020-01-01'	,'Casa'				,'percentual'	,0		,0.20	)
	,(	'2020-01-01'	,'Carro'			,'percentual'	,0		,0		)
	,(	'2020-01-01'	,'Videogame'		,'percentual'	,0		,0.05	)
	,(	'2020-01-01'	,'Presente'			,'percentual'	,0		,0.02	)
	,(	'2020-01-01'	,'Viagem'			,'percentual'	,0		,0.02	)
	,(	'2023-11-01'	,'Investimento'		,'percentual'	,0		,0.26	)
	,(	'2023-11-01'	,'Presente'			,'percentual'	,0		,0.03	)
	,(	'2023-11-01'	,'Viagem'			,'percentual'	,0		,0.03	)
	



	
	--	=================================================================================================
	set	@etapa_processo	=	'Realiza a validação de duplicidade.'
	--	=================================================================================================
	
	drop table if exists #tmp_validacao_duplicidade 
	
	select	 a.dt_calendario
			,a.classificacao
			,a.fl_valor_percentual
			,a.valor
			,a.percentual
			,id_ordem		=	row_number() over ( partition by a.classificacao, a.dt_calendario order by a.dt_calendario asc )
	into	#tmp_validacao_duplicidade
	from	tbl_distribuicao_salario	a
	



	--	=================================================================================================
	set	@etapa_processo	=	'Verifica se há duplicidade.'
	--	=================================================================================================
	
	if ( select count( 1 ) from #tmp_validacao_duplicidade where id_ordem > 1 ) = 1
		raiserror( 'Duplicidades encontradas', 16, 1 );



	--	=================================================================================================
	set	@etapa_processo	=	'Realiza a ordenação das distribuições de salário por data.'
	--	=================================================================================================
	
	drop table if exists #tmp_aux_ordenacao_distribuicao_salario

	select	 a.dt_calendario
			,a.classificacao
			,a.fl_valor_percentual
			,a.valor
			,a.percentual
			,id_ordem		=	row_number() over ( partition by a.classificacao order by a.dt_calendario asc )
	into	#tmp_aux_ordenacao_distribuicao_salario
	from	tbl_distribuicao_salario	a
	


	
	--	=================================================================================================
	set	@etapa_processo	=	'Criação da vigência.'
	--	=================================================================================================
	
	drop table if exists #tmp_aux_vigencia_distribuicao_salario

	select	 dt_inicio		=	a.dt_calendario
			,dt_fim			=	isnull( dateadd( day, -1, b.dt_calendario ), '9999-12-31' )
			,a.classificacao
			,a.fl_valor_percentual
			,a.valor
			,a.percentual
	into	#tmp_aux_vigencia_distribuicao_salario
	from	#tmp_aux_ordenacao_distribuicao_salario	a
		left join	#tmp_aux_ordenacao_distribuicao_salario		b
			on	a.classificacao	=	b.classificacao	
			and	a.id_ordem		=	b.id_ordem - 1
			


	
	--	=================================================================================================
	set	@etapa_processo	=	'Validação se tem 100% alocado na distribuição mais recente.'
	--	=================================================================================================
	
	drop table if exists #tmp_aux_validacao_distribuicao_salario_100

	select	soma_percentual	=	sum( a.percentual )
	into	#tmp_aux_validacao_distribuicao_salario_100
	from	#tmp_aux_vigencia_distribuicao_salario	a
	where	a.dt_fim	=	'9999-12-31'



	
	--	=================================================================================================
	set	@etapa_processo	=	'Verifica se tem 100% alocado na distribuição mais recente.'
	--	=================================================================================================
	
	if ( select convert( int, soma_percentual ) from #tmp_aux_validacao_distribuicao_salario_100 ) <> 1
		raiserror( 'Distribuição mais recente alocada está diferente de 100', 16, 1 )


	
	--	=================================================================================================
	set	@etapa_processo	=	'Insere os dados na tabela final.'
	--	=================================================================================================
	
	insert into tbl_distribuicao_salario_vigencia
	select	 a.dt_inicio
			,a.dt_fim	
			,a.classificacao
			,a.fl_valor_percentual
			,a.valor
			,a.percentual
	from	#tmp_aux_vigencia_distribuicao_salario	a


	

end try
begin catch

	select	@etapa_processo

end catch







