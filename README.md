# SACIMBot
Bot criado pela SACIM para facilitar o acesso a informações do JupiterWeb e do ICMC.

**Índice**

1. [Informações Gerais](#informações-gerais)
2. [Contribuições](#contribuições)
3. [Arquivos e Organização Geral do Repositório](#arquivos-e-organização-geral-do-repositório)
4. [Makefile](#makefile)
5. [Considerações Finais e Futuro](#considerações-finais-e-futuro)

## 1. Informações Gerais
O Bot é feito em Python 3.12.3 e utiliza a biblioteca `pyTelegramBotAPI` para integrar com a API oficial do Telegram. Ele também utiliza algumas outras bibliotecas, que podem ser consultadas em [requirements.txt](requirements.txt).

Adicionalmente, utilizamos o `ruff 0.16.8` como linter (cujas regras estão em [.ruff.toml](.ruff.toml)) e o `pre-commit 4.6.2` para executá-lo antes de cada commit (ver [.pre-commit-config.yaml](.pre-commit-config.yaml)).

Atualmente, o Bot roda em um container Docker instalado em um dos PCs da Salinha da SACIM (*Ubuntu 24.04.5 LTS*). Um objetivo futuro é conseguirmos uma VM própria para ele!

Caso queira nos contactar, ficaremos felizes em interagir por e-mail: `sacim (dot) caaso (at) gmail (dot) com`.

## 2. Contribuições
Sinta-se livre para contribuir com o Bot da forma como queira! Por enquanto, não temos diretrizes claras de nomenclatura de commits e branches, então aceitamos sugestões!

Se quiser sugestões do que melhorar ou implementar no Bot, confira na seção [Considerações Finais e Futuro](#considerações-finais-e-futuro).

## 3. Arquivos e Organização Geral do Repositório
Para além de conter os arquivos essenciais para o funcionamento do Bot, o repositório também dispõe de (*quase*) todos os programas utilizados para coletar dados do sistema Júpiter, do site do ICMC e de alguns outros portais da USP. É importante mencionar que **todas as informações** coletadas pelos programas do repositório são públicas e acessíveis sem a necessidade de login ou conexão a redes privadas.

### Coleta de dados
A coleta de dados é feita (por enquanto) de forma não periódica. Isso significa que é necessário rodar os programas manualmente e que o processo de atualizar as informações coletadas não é automático (veja mais sobre o [Makefile](#makefile)).

Ela é dividida nas etapas de **scraping** e **parsing**, cujos programas estão dispostos em [/scraper](/scraper). Todos os dados estão salvos em arquivos `.json` e em um Banco de Dados `sqlite`, ambos mantidos em uma pasta ignorada chamada `/dados`. A estrutura dessa pasta (bem como de outras pastas ignoradas) pode ser vista em [Organização das Pastas Ocultas](#organização-das-pastas-ocultas).

- **Scraping**: Acesso e obtenção do conteúdo das páginas no formato HTML e subsequente escrita em arquivos `.json`. Isso é feito nos programas dispostos em [/scraper/collectors](/scraper/collectors). **IMPORTANTE**: para evitar um uso anti-ético dos dados coletados no site do ICMC, os scrapers referentes a eles foram omitidos do repositório.
- **Parsing**: Leitura dos dados dos arquivos `.json` criados na etapa anterior e povoamento/atualização das tabelas do Banco de Dados. Isso é feito no arquivo [/scraper/parsers.py](/scraper/parsers.py).

Essa conversão (HTML para `.json` e `.json` para BD) é feita por meio das entidades (classes) dispostas em [/entidades](/entidades). Essas estruturas permitem organizar semanticamente os dados coletados e facilitar sua compreensão.

### Banco de dados
Todos os programas referentes à manipulação do arquivo de Banco de Dados `sqlite` (leitura e escrita) estão na pasta [/db](/db). Apesar do próprio arquivo do BD (`dados/dados.db`) não está no repositório, é possível reconstrui-lo quase totalmente com base nos comandos dispostos no [Makefile](Makefile) e nos esquemas das tabelas em [db/esquemas.txt](db/esquemas.txt).

### Bot
O Bot em questão roda a partir do programa principal [SacimBot.py](SacimBot.py) com o `TOKEN` salvo em um arquivo `.env` privado. Caso queira testar o Bot, recomendo criar um Bot próprio no Telegram - basta interagir com o Bot `@BotFather` que o Telegram mantém.

Para o Bot funcionar, ele precisa realizar duas funções:

- Registrar todos os comandos (/) que ele possui, isto é, definir o que o Bot deve fazer quando alguém enviar um comando para ele.
- Registrar todos os *listeners* (chamados aqui de *queries*) de interações, isto é, definir o que o Bot deve fazer quando alguém interagir com ele (apesar de significar mais que isso, no contexto do Bot, interprete interações como **clique de botões**).

A partir disso, o funcionamento do Bot se resume em executar alguma função quando alguém enviar algum comando e quando alguém clicar em algum botão. Os textos de mensagens enviadas pelo Bot estão em [/bot/textos](/bot/textos/).

#### Comandos
Todos os comandos registrados no Bot estão dispostos na pasta [/bot/comandos/](/bot/comandos/). Os comandos que **não precisam** acessar o Banco de Dados estão todos listados em [/bot/comandos/estaticos.py](/bot/comandos/estaticos.py). Os demais estão agrupados em alguns arquivos `.py` de acordo com sua temática.

Por meio de um `decorador` (disposto em [/bot/entidades/comando.py](/bot/entidades/comando.py)), os comandos da pasta de comandos são lidos e armazenados em uma lista `COMANDOS_BOT` e em um dicionário `COMANDOS_FUNCS` (ambos também no mesmo programa acima). A lista serve para enviar à API do Telegram os comandos a serem cadastrados no menu do Bot (quando se digita `/` no chat), já o dicionário é para relacionar o nome do comando à sua função. É no arquivo [/bot/loader.py](/bot/loader.py) que todos os arquivos na pasta de comandos são importados e devidamente registrados.

Quando um comando é enviado pelo usuário, ele passa no handler global declarado no `loader.py` e executa a função declarada na pasta `comandos`. As funções, essencialmente, respondem o usuário com alguma mensagem. Quando a mensagem **não tem botões**, o procedimento se encerra aí. Porém, caso a mensagem contenha botões, é criada uma instância de alguma classe filha de `MsgComBotoesDinamicos` (declaradas em [/bot/entidades/mensagem.py](/bot/entidades/mensagem.py)), que gerencia toda e qualquer mensagem com botões dinâmicos enviada pelo bot (o termo *dinâmico* é necessário porque existem botões de `URL` no Telegram, que *não emitem interações*).

#### Mensagem com botões dinâmicos (queries)
No Bot, utilizamos duas classificações para essas mensagens: as **mensagens de menu**, que contêm uma classe `Menu` ([/bot/entidades/menu.py](/bot/entidades/menu.py)), e as **mensagens de resultados**, que contêm uma classe `Resultado` ([/bot/entidades/resultados.py](/bot/entidades/resultados.py)):

- **Mensagens de menu**: São mensagens que contêm um menu navegável, como se fossem páginas de um mesmo site. Exemplos: as informações de uma pessoa, de uma pesquisa ou de uma disciplina.
- **Mensagens de resultados**: É a mensagem de uma lista de resultados de uma busca, que possui a paginação entre os itens e permite acessar um resultado específico. Exemplos: quando mais de um resultado é encontrado ao usar o `/nomedisc` ou `/pessoa`.

Os botões dessas mensagens são gerados por métodos das classes declaradas em [/bot/entidades/botao.py](/bot/entidades/botao.py). Cada um deles possui uma string de *callback* utilizada pelo Bot para identificar o que ele deve fazer. Adotamos uma padronização dessas strings nos métodos declarados em [/bot/entidades/callback.py](/bot/entidades/callback.py). Essas strings são argumentos das *queries* registradas em [/bot/query.py](/bot/query.py), que atualizam as mensagens ou realizam outras ações mediante o clique de um botão.

#### Arquivos
Os documentos enviados por alguns comandos do Bot (como o `/cal2026` e o `/matriculas`) estão dispostos em [/arquivos](/arquivos/), em uma subpasta oculta `/docs`.

### Outros arquivos importantes

- Em [/constantes.py](/constantes.py) estão todas as constantes, redes sociais e links dos scrapers utilizados pelo repositório.
- Em [/changelog.json](/changelog.json) está uma lista de objetos que representam as versões do Bot (*hard-codadas*) enviadas pelo comando `/versoes`.
- Em [/bot/comandos_uteis.txt](/bot/comandos_uteis.txt) está uma lista dos comandos mais úteis do Bot. Serve para adicionar uma estrelinha no menu do Bot no Telegram.

### Organização das pastas ocultas

- **`/dados`**:
    - `json/`
        - `discs/`, `ofcs/` e `reqs/`
            - Arquivos `n.json` em que n corresponde ao código de uma unidade do Júpiter.
        - `comissoes.json`
        - `cursos.json`
        - `lista_pessoas.json`
        - `pesquisas.json`
        - `pessoas.json`
    - `dados.db`: Banco de Dados
- **`scraper/collectors/icmc/`**
    - `lista_pessoa.py`: Coleta a lista de pessoas no ICMC Pessoas.
    - `pesquisa.py`: Coleta as áreas de pesquisa no ICMC Pesquisas.
    - `pessoa.py`: Coleta as informações individuais de uma pessoa.
- **`arquivos/docs/`**
    - `calendario2026.pdf`
    - `calendario2027.pdf`
    - `matriculas.pdf`

## 4. Makefile
O arquivo [Makefile](/Makefile) dispõe de um comando para rodar o Bot (`make run`) e uma série de comandos para realizar o scraping dos dados:

- Os comandos da forma `c_xx` realizam a coleta dos dados (etapa do *scraping*) e escrevem nos JSON.
- Os comandos da forma `p_xx` realizam o tratamento dos dados (etapa do *parsing*): leem do JSON e escrevem no BD.
- O comando `db` executa todos os comandos da forma `p_xx`.
- Os comandos da forma `xx` executam as operações `c_xx` e `p_xx` diretamente.

## Considerações Finais e Futuro
Caso você tenha quaisquer dúvidas a respeito do funcionamento do Bot, pode entrar em contato conosco via e-mail (`sacim (dot) caaso (at) gmail (dot) com`) ou pelos contatos dos Desenvolvedores listados no comando `/start`.

A seguir, uma lista de melhorias e sugestões de novas funcionalidades que podem ser implementadas:

- **Scraper das disciplinas do Sistema Janus de Pós Graduação**
- **Scraper das grades curriculares dos cursos da USP**
- **Scraper do Calendário Escolar, das grades horárias dos cursos e de outros arquivos importantes**
- **Melhoria de comentários no Código, na legibilidade e deste README**
- **Simplificações de algumas funções**
- **Automatização da coleta dos dados, isto é, executá-los de forma periódica**
- **Organizar melhor as constantes, talvez separar em vários arquivos**
- **Comando para listar os oferecimentos de qualquer docente da USP**
- **Informações sobre o Aloja, o PAPFE, o GAPsi, o CAASO, a Gráfica do ICMC, a Diretoria, o STI, a Prefeitura do Campus, etc.**
- **Informações sobre Grupos de Extensão**

Bom código!

**SACIM 2026**
