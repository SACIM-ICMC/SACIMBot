PYTHON = python3

# COLETAS
c_listpess:
	@echo "Realizando COLETA de icmc/pessoas para lista_pessoas.json"
	@$(PYTHON) -m scraper.collectors.lista_pessoa
c_pess:
	@echo "Realizando COLETA de icmc/pessoas com lista_pessoas.json para pessoas.json"
	@$(PYTHON) -m scraper.collectors.pessoa
c_comiss:
	@echo "Realizando COLETA de comissões para comissoes.json"
	@$(PYTHON) -m scraper.collectors.comissao
c_curso:
	@echo "Realizando COLETA de cursos para cursos.json"
	@$(PYTHON) -m scraper.collectors.cursos
c_pesq:
	@echo "Realizando COLETA de icmc/pesquisa para pesquisas.json"
	@$(PYTHON) -m scraper.collectors.pesquisa
c_disc: # ATENÇÃO: DEMORADO
	@echo "Realizando COLETA de disciplinas para discs/.json"
	@$(PYTHON) -m scraper.collectors.disciplina
c_req:  # ATENÇÃO: DEMORADO
	@echo "Realizando COLETA de requisitos para reqs/.json"
	@$(PYTHON) -m scraper.collectors.requisito
c_oferecs:  # ATENÇÃO: DEMORADO
	@echo "Realizando COLETA de oferecimentos para oferecs/.json"
	@$(PYTHON) -m scraper.collectors.oferecimento

# TRATAMENTOS
p_pess:
	@echo "Realizando TRATAMENTO de pessoas.json para dados.db"
	@$(PYTHON) -m scraper.parsers pessoa
p_comiss:
	@echo "Realizando TRATAMENTO de comissoes.json para dados.db"
	@$(PYTHON) -m scraper.parsers comissao
p_curso:
	@echo "Realizando TRATAMENTO de cursos.json para dados.db"
	@$(PYTHON) -m scraper.parsers cursos
p_pesq:
	@echo "Realizando TRATAMENTO de pesquisas.json para dados.db"
	@$(PYTHON) -m scraper.parsers pesquisa
p_disc:
	@echo "Realizando TRATAMENTO de discs/.json para dados.db"
	@$(PYTHON) -m scraper.parsers disciplina
p_req:
	@echo "Realizando TRATAMENTO de reqs/.json para dados.db"
	@$(PYTHON) -m scraper.parsers requisito
p_oferecs:
	@echo "Realizando TRATAMENTO de oferecs/.json para dados.db"
	@pyt$(PYTHON)hon3 -m scraper.parsers oferecimento

# PIPELINES DE COLETAS + TRATAMENTOS
pess: c_listpess c_pess p_pess
comiss: c_comiss p_comiss
curso: c_curso p_curso
pesq: c_pesq p_pesq
disc: c_disc p_disc # ATENÇÃO: DEMORADO
req: c_req p_req # ATENÇÃO: DEMORADO
oferecs: c_oferecs p_oferecs # ATENÇÃO: DEMORADO

# GERAR DB
db: p_pess p_comiss p_curso p_pesq p_disc p_req p_oferecs

# Executa o bot
run:
	@$(PYTHON) -m SacimBot