from enum import StrEnum

from telebot.formatting import hbold, hcode, hitalic, hlink

from bot.utils import formatar_email
from constantes import Biblio, EmailsGrad, EmailsICMC, LinksInfos, LinksInvite, Museu, RedesSACIM
from entidades.changelog import Versao


class TxtInfos(StrEnum):
    BIBLIO = (
        f"{hbold('Biblioteca Achille Bassi')}\n"
        "BLOCO 2 - ICMC\n"
        "Segunda a sexta-feira: das 8h às 21h30min\n"
        "Sábado: das 9h às 12h\n"
        "\n"
        f"{hbold('E-mail:')} {formatar_email(Biblio.EMAIL)}\n"
        f"{hbold('Atendimento Online:')} {hlink(Biblio.LIVECHAT, Biblio.LIVECHAT)}\n"
        f"{hbold('Whatsapp:')} {Biblio.WHATS}\n"
    )

    CARTILHAS = (
        f"🖤📓 {hbold('Cartilhas SACIM 2026')}\n"
        "\n"
        f"Confira os materiais completos {hlink('aqui', LinksInfos.CARTILHAS_SACIM)}.\n"
    )

    EDUROAM = (
        f"ℹ️ {hbold('Como configuar a eduroam no seu dispositivo?')}\n"
        "\n"
        f"Confira o tutorial {hlink('aqui', LinksInfos.GUIA_EDUROAM)}.\n"
    )

    GRAD = (
        f"{hbold('Horários de atendimento presencial do Serviço de Graduação do ICMC')}\n"
        "Segunda à Sexta: 09h às 11h e 14h às 16h\n"
        "Adicionalmente, às Terças e Quintas: 18h às 19h\n"
        "\n"
        f"{hbold('E-mails:')}\n"
        f"- BCC: {formatar_email(EmailsGrad.BCC)}\n"
        f"- BSI: {formatar_email(EmailsGrad.BSI)}\n"
        f"- BECD: {formatar_email(EmailsGrad.BECD)}\n"
        f"- BCDados: {formatar_email(EmailsGrad.BCDADOS)}\n"
        f"- BMA/LMA: {formatar_email(EmailsGrad.BMA_LMA)}\n"
        f"- BMACC: {formatar_email(EmailsGrad.BMACC)}\n"
        f"- EngComp/Lic: {formatar_email(EmailsGrad.EC_LCE)}\n"
        f"- Estágio: {formatar_email(EmailsGrad.ESTAGIO)}\n"
        f"- Comunidade externa ao ICMC: {formatar_email(EmailsGrad.COMUN_EXT)}\n"
    )

    MUSEU = (
        f"{hbold('Museu de Computação Prof. Odelar Leite Linhares')}\n"
        "BLOCO 4 - ICMC\n"
        "Segunda a sexta-feira: das 08h às 19h\n"
        "Sábado: das 08h às 12h\n"
        "Verificar nos feriados\n"
        "\n"
        f"{hbold('E-mail:')} {formatar_email(Museu.EMAIL)}\n"
        f"{hbold('Site:')} {hlink(Museu.SITE, Museu.SITE)}\n"
        f"{hbold('Whatsapp:')} {Museu.WHATS}\n"
    )

    PRINTER = (
        f"🖨️ {hbold('Impressora da Pró-Aluno')}\n"
        "\n"
        f"🏠 {hbold('Salas')}: ICMC {hcode('1-105')} no Campus 1, {hcode('EC-002')} no Campus 2\n"
        f"#️⃣ {hbold('Cotas de impressão por semestre')}: {hcode('100')}\n"
        "\n"
        f"1) Para solicitar uma impressão, o usuário {hbold('DEVE')} estar em uma rede USP (eduroam ou VPN USP), mas {hbold('NÃO PRECISA')} estar fisicamente presente na sala.\n"
        f"2) Acessar o site {hlink(LinksInfos.PRINTER, LinksInfos.PRINTER)} e logar com seu NUSP e senha única.\n"
        f"3) Selecionar em qual impressora (Campus 1 ou 2) deseja imprimir.\n"
        f"4) Realizar o upload do arquivo a ser impresso (o sistema de seleção de quantidade de cópias e páginas NÃO FUNCIONA) e buscá-lo.\n"
        "\n"
        f"🚨 {hbold('ATENÇÃO')}: A impressora imprime automaticamente todas as folhas em preto-branco e frente-verso.\n"
    )

    RESERVAS = (
        f"ℹ️ {hbold('Como reservar salas em nome de grupos de extensão no ICMC?')}\n"
        "\n"
        f"1) Confira as salas disponíveis na data e horário desejado no {hlink('Intranet', LinksInfos.INTRANET_SALAS)} (acessar pela eduroam ou VPN USP).\n"
        f"2) Com a sala em mente, preencha {hlink('este formulário', LinksInfos.RESERVAS)} e aguarde a confirmação por e-mail.\n"
        "\n"
        f"OBS.: Reservas dos auditórios {hitalic('Fernão e Fávaro')}, bem como do {hitalic('Hiperespaço (vão da biblioteca)')}, devem ser feitas pelo e-mail: {formatar_email(EmailsICMC.EVENTOS)}"
    )

    VPN = (
        f"ℹ️ {hbold('Como configuar a FortiClient VPN (VPN USP) no seu dispositivo?')}\n"
        "\n"
        f"Confira o tutorial {hlink('aqui', LinksInfos.GUIA_VPN)}.\n"
    )


class TxtSACIM(StrEnum):
    HINO = f"""
🟡 {hbold("Hino do CAASO")} ⚫

Nós somos lá de São Carlos
viemos aqui pra zonear
No esporte nós somos bosta,
nosso negócio é a cachaça!

E mesmo que nós não ganhe,
que nós apanhe, vamos brindar
A comida dá diarréia
e as pessoas dão gonorréia!!!

A pinga queremos com limão
As pessoas com muito mais tesão!
Porém se a USP amada precisar da macacada,
Puta merda que cagada!

1  2  3  4

Como é legal
calcular a integral!
Mesmo sem grafite
calculamos o limite!

Amor de graça
pela cachaça…
Não há quem possa
com a turma nossa:

Engenharia U-S-P
CAASO, CAASO,
Botando pra fudê!

Engenharia U-S-P
CAASO, CAASO,
Botando pra fudê!

Ô FEDERAAAAL
Xupa!
Ô FEDERUUUPAAA
Vai pra puta que pariu,
í, ó!!!
"""

    INVITES = (
        f"💬 {hbold('Links de invite de grupos:')}\n"
        "\n"
        f"⚠️ {hlink('SACIM Avisos', LinksInvite.SACIM_AVISOS)}\n"
        f"🫂 {hlink('Super Família ICMC', LinksInvite.SUPERFAMILIA)}\n"
        f"🚨 {hlink('Assaltos - Matemática', LinksInvite.ASSALTOS)}\n"
        f"🛍️ {hlink('Super Feirão ICMC', LinksInvite.SUPERFEIRAO)}\n"
        f"🏪 {hlink('Promoções de Mercados', LinksInvite.PROMOCOES)}\n"
        f"🍽️ {hlink('Restaurantes', LinksInvite.RESTAURANTES)}\n"
    )

    REDES = (
        f"💛 {hbold('Redes:')}\n"
        "\n"
        f"📷 {hbold('Instagram:')} {hlink(RedesSACIM.INSTAGRAM, RedesSACIM.URL_INSTAGRAM)}\n"
        f"✉️ {hbold('E-mail institucional:')} {formatar_email(RedesSACIM.EMAIL_ICMC)}\n"
        f"✉️ {hbold('E-mail secundário:')} {formatar_email(RedesSACIM.EMAIL_GMAIL)}\n"
        f"🔗 {hbold('Linktree:')} {hlink(RedesSACIM.LINKTREE, RedesSACIM.URL_LINKTREE)}\n"
        f"🌐 {hbold('Site:')} {hlink(RedesSACIM.SITE, RedesSACIM.URL_SITE)}\n"
        "\n"
        "~ Gestão 2026"
    )

    START = (
        f"💛🤖 {hbold('SACIMBot')}\n"
        "\n"
        "Bot criado pela SACIM para facilitar o acesso a informações do JupiterWeb e do ICMC.\n"
        "Utilize /help para saber mais sobre os comandos!\n"
        "\n"
        f"{hbold('Reclamações, dúvidas e sugestões?')} Contate-nos!\n"
        f"🔗 {hbold('Instagram:')} {hlink(RedesSACIM.INSTAGRAM, RedesSACIM.URL_INSTAGRAM)}\n"
        f"🔗 {hbold('E-mail:')} {formatar_email(RedesSACIM.EMAIL_GMAIL)}\n"
        "\n"
        f"{hbold('Créditos')}:\n"
        "@gusvidigal\n"
        "@PedroTiago025\n"
        "@bielcomp24\n"
        "iudee\n"
        f"Quer ajudar a fazer o bot? Saiba mais em /repo.\n"
        "\n"
        "~ Gestão 2026"
    )

    HELP = (
        f"💛🤖 Comandos do {hbold('SACIMBot')}\n"
        "Em ⭐ estão os mais úteis!\n"
        "\n"
        f"🟡 {hbold('Geral')}\n"
        "⭐ /start (ou /sobre, /about): Informações gerais sobre o Bot.\n"
        "⭐ /help (ou /ajuda): Informações gerais sobre os comandos do Bot.\n"
        "/repo (ou /github): Como ajudar no desenvolvimento do Bot.\n"
        "/versao (ou /changelog): Atualizações do Bot ao longo do tempo.\n"
        "/invites: Links de grupos do Telegram.\n"
        "/redes: Redes sociais da SACIM.\n"
        "\n"
        f"📚 {hbold('Materiais')}\n"
        "/cal2026: Calendário Escolar de 2026.\n"
        "/cal2027: Calendário Escolar de 2027.\n"
        "/cartilha: Cartilhas de cursos da SACIM 2026.\n"
        "\n"
        f"🌐 {hbold('Buscas')}\n"
        "⭐ /pessoa [nome]: Informações de uma pessoa (exceto alunos) do ICMC.\n"
        "⭐ /nomedisc [nome]: Informações de uma disciplina pelo nome.\n"
        "/disc [código]: Informações de uma disciplina pelo código.\n"
        "/comissao [nome]: Mandatos de uma comissão do ICMC.\n"
        "/email [nome]: E-mail de uma pessoa (exceto alunos) do ICMC.\n"
        "/pesquisa [nome]: Informações de um grupo de pesquisa do ICMC.\n"
        "/sala [nome]: Sala de uma pessoa do ICMC.\n"
        "\n"
        f"ℹ️ {hbold('Informações')}\n"
        "⭐ /grad: Sobre o Serviço de Graduação.\n"
        "/biblio: Sobre a Biblioteca Achille Bassi.\n"
        "/museu: Sobre o Museu de Computação Odelar Leite Linhares.\n"
        "/coc: Composição das coordenações dos cursos.\n"
        "/depto: Composição dos departamentos.\n"
        "\n"
        f"📖 {hbold('Tutoriais')}\n"
        "⭐ /eduroam: Como configurar e utilizar a eduroam?\n"
        "/printer: Como imprimir na Pró-Aluno?\n"
        "/reservas: Como reservar salas no ICMC em nome de grupos de extensão?\n"
        "/vpn: Como configurar e utilizar a VPN-USP?\n"
        "/matriculas: Como funciona o sistema de matrículas de disciplinas?\n"
        "\n"
        f"🪢 {hbold('Miscelânea')}\n"
        "/hino: Hino do CAASO.\n"
    )

    REPO = (
        f"💛🤖 Repositório Github do {hbold('SACIMBot')}\n"
        "\n"
        f"Sinta-se livre para explorar o código e nos ajudar a construir o Bot!\n"
        "\n"
        f"{hbold("Repositório")}: {hlink("SACIM-ICMC/SACIMBot", RedesSACIM.REPO)}\n"
    )

    def VERSOES(versoes: list[Versao]) -> str:
        txt = f"💛🤖 Versões e Atualizações do {hbold('SACIMBot')}\n\n"
        for v in versoes:
            txt += f"📢 {hbold(f'Versão {v.versao} — {v.data}')}\n"

            if v.novidades:
                txt += f"{hbold('Novidades')}\n"
                for item in v.novidades:
                    txt += f"- {item}\n"
            if v.correcoes:
                txt += f"{hbold('Correções')}\n"
                for item in v.correcoes:
                    txt += f"- {item}\n"
            txt += "\n"
        return txt


class TxtArquivos(StrEnum):
    def CALENDARIO(ano: int) -> str:
        return f"📅 {hbold(f'Calendário Escolar {ano}')}"

    MATRICULAS = f"🛎️ {hbold('Informativo sobre Matrículas')}"
