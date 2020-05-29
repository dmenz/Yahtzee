#######################################################################
# MODULO PARTIDA
#
#  Centraliza as ações relacionadas ao andamento de uma partida fazendo
#  a comunicação entre os diversos módulos envolvidos. Cada partida 
#  possui um atributo identificador “data_horario”, trata-se do tipo 
#  datetime do python, indicando a data e horário em que foi criada. 
#   Uma partida pode ter status “andamento”, “pausada” ou “encerrada”.
#  Somente uma partida poderá estar em andamento ao mesmo tempo. As 
#  partidas são armazenadas no banco de dados apenas para registrar um
#  histórico. Portanto, não é possível recuperar uma partida pausada 
#  pelo banco de dados, para isso, é necessário salvar o estado da 
#  partida em um arquivo XML.
#
#---------------------------v0.1.0: 25/05/2020-------------------------
#  Por: Daniel Menezes
#  Criado mocking para tabela.cria_tabela
#  Implementada inicia_partida passando nos testes
#
#---------------------------v0.2.0: 27/05/2020-------------------------
#  Por: Daniel Menezes
#  Modificada inicia_partida. Agora se recusa a iniciar uma partida
#  caso já haja uma partida em andamento. Passando nos novos testes.
#
#---------------------------v0.3.0: 27/05/2020-------------------------
#  Por: Daniel Menezes
#  Implementada faz_lancamento. Passando nos testes.
#
#---------------------------v0.4.0: 28/05/2020-------------------------
#  Por: Daniel Menezes
#  Implementada marca_pontuacao usando mock. Passando nos testes.
#  Mocks criados: 
#    -tabela.insere_pontuacao 
#    -tabela.obtem_tabelas
#---------------------------v0.4.1: 28/05/2020------------------------
#  Por: Daniel Menezes
#  Removido import indevido de jogador.
#
#---------------------------v0.4.2: 28/05/2020------------------------
#  Por: Daniel Menezes
#  Adicionado marca_pontuacao em __all__.
#
#---------------------------v0.5.0: 28/05/2020------------------------
#  Por: Daniel Menezes
#  Criado mock de tabela.registra_desistencia
#  Implementada desiste. Passando nos testes.
#  
#######################################################################

from datetime import datetime
from random import shuffle
from os.path import isdir
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom

from entidades import tabela
from funcionalidades import banco_de_dados
from funcionalidades import combinacao

from unittest import mock

__all__ = ['inicia_partida', 'faz_lancamento', 'marca_pontuacao', 'desiste',
        'obtem_partidas']


partida_atual = {}

#MOCKS:
tabela = mock.Mock()
tabela.cria_tabela.side_effect = [1, 0, 0, 0]
tabela.insere_pontuacao.side_effect = [0,4]
tabela.obtem_tabelas.side_effect = [
       [{'nome_jogador':'flavio', 
         'data_horario_partida':None, 
         'pontos_por_categoria': [ 
                {'nome':'chance', 'pontuacao':14},
                {'nome':'yahtzee', 'pontuacao':None}
             ],
         'pontuacao_total':14, 
         'colocacao':1,
         'desistencia':False
       }]
    ]
tabela.registra_desistencia.return_value = 0

def _proximo_jogador():
    index = partida_atual['jogadores'].index(partida_atual['jogador_da_vez'])
    index = (index + 1) % len(partida_atual['jogadores'])
    return partida_atual['jogadores'][index]

def _partida_deve_acabar():
    tabelas = tabela.obtem_tabelas([],[partida_atual['data_horario']])

    todos_desistiram = False
    if all(tabela_jogador['desistencia'] for tabela_jogador in tabelas):
        todos_desistiram = True
    else:
        todas_as_tabelas_preenchidas = False
        jogadores_nao_desistentes = [tabela_jogador for tabela_jogador \
                in tabelas if not tabela_jogador['desistencia']]
        pontuacoes = []
        for tabela_jogador in jogadores_nao_desistentes:
            for pontos_por_cat in tabela_jogador['pontos_por_categoria']:
                pontuacoes.append(pontos_por_cat)
        if all(pts['pontuacao'] != None for pts in pontuacoes ):
            todas_as_tabelas_preenchidas = True

    return todos_desistiram or todas_as_tabelas_preenchidas

def _altera_status_bd(status):
    sql = """UPDATE Partida
             SET status = %s
             WHERE data_horario = %s"""
    banco = banco_de_dados.abre_acesso()
    banco['cursor'].execute(sql, (status, partida_atual['data_horario']))
    banco_de_dados.fecha_acesso(banco)
    return

def _ha_partida_em_andamento():
    return (partida_atual and partida_atual['status'] == 'andamento')

def _passa_turno():
    partida_atual['jogador_da_vez'] = _proximo_jogador()
    partida_atual['turno'] += 1
    partida_atual['tentativas'] = 3
    return

#################################################################
# Cria uma nova partida e associa tabelas para os seus jogadores.
# nomes: lista de nomes dos jogadores participantes.
#
# retorna data_horario da partida criada em caso de sucesso
# ou retorna 1 caso um dos jogadores passados não exista.
# ou retorna 2 caso já haja uma partida em andamento.
#################################################################
def inicia_partida(nomes):
    if _ha_partida_em_andamento():
        return 2
    data_horario = datetime.now()
    for jogador in nomes:
        cod_retorno = tabela.cria_tabela(jogador, data_horario) 
        if cod_retorno == 1:
            #jogador nao existe
            for jogador_a_remover in nomes:
                if jogador == jogador_a_remover:
                    break
                tabela.remove(jogador, data_horario)
            return 1

    banco = banco_de_dados.abre_acesso()
    sql_partida = """INSERT Partida VALUES (%s, %s)"""
    banco['cursor'].execute(sql_partida, (data_horario, 'andamento'))
    banco_de_dados.fecha_acesso(banco)

    shuffle(nomes)
    partida_atual['data_horario'] = data_horario
    partida_atual['combinacao'] = None
    partida_atual['pts_combinacao'] = None
    partida_atual['turno'] = 1
    partida_atual['tentativas'] = 3
    partida_atual['jogadores'] = nomes
    partida_atual['jogador_da_vez'] = nomes[0]
    partida_atual['status'] = 'andamento'
    partida_atual['salva'] = False

    return data_horario 

############################################################################
#  Gera um novo lançamento para o jogador do turno na partida em andamento.
#  
#  dados_escolhidos: lista com os índices (inteiros no intervalo [0,4])
#   dos dados a terem seus valores mantidos
#   ou lista vazia para rolar todos os dados
#
#  Retorna 0 em caso de sucesso
#   ou retorna 1 caso não haja partida em andamento
#   ou retorna 2 caso um dos índices em dados_escolhidos não seja válido
#   ou retorna 3 caso dados_escolhidos não seja uma lista vazia no primeiro
#    lançamento do turno atual.
#   ou retorna 4 caso o jogador do turno atual já tenha esgotado o número 
#    de tentativas.
#
############################################################################
def faz_lancamento(dados_escolhidos):
    if not _ha_partida_em_andamento():
        return 1
    if any(d not in range(1,7) for d in dados_escolhidos):
        return 2
    if partida_atual['tentativas'] == 3 and dados_escolhidos:
        return 3
    if partida_atual['tentativas'] == 0:
        return 4

    comb = combinacao.gera_combinacao(dados_escolhidos)
    partida_atual['combinacao'] = comb['combinacao'] 
    partida_atual['pts_combinacao'] = comb['pontos']
    partida_atual['tentativas'] -= 1

    partida_atual['salva'] = False
    return 0

########################################################################
#
#  Atribui ao jogador do turno da partida atual os pontos do seu último
#   lançamento (do mesmo turno) na categoria escolhida e passa para o
#   próximo turno.
#
#  categoria: nome da categoria escolhida
#
#  Retorna 0 em caso de sucesso
#   ou retorna 1 caso não haja partida em andamento
#   ou retorna 2 caso a categoria seja inválida
#   ou retorna 3 caso o jogador do turno ainda não tenha realizado
#     um lançamento no turno atual.
#   ou retorna 4 caso o jogador já tenha marcado pontos
#     na categoria escolhida nessa partida
#
########################################################################
def marca_pontuacao(categoria):
    if not _ha_partida_em_andamento():
        return 1
    if partida_atual['tentativas'] == 3:
        return 3

    for categ in partida_atual['pts_combinacao']:
        if categ['nome'] == categoria:
            pontos = categ['pontuacao']
            break
    else:
        return 2

    args = [partida_atual['jogador_da_vez'],
            partida_atual['data_horario'],
            categoria,
            pontos]
    ret_insere = tabela.insere_pontuacao(*args)

    if ret_insere == 4:
        return 4

    partida_atual['salva'] = False
    if _partida_deve_acabar():
        partida_atual['status'] = 'encerrada'  
        _altera_status_bd('encerrada') 
    else:
        _passa_turno()

    return 0

##############################################################################
# Retira um jogador da partida.
# Retorna 0 em caso de sucesso.
#  ou retorna 1 caso não haja partida em andamento
#  ou retorna 2 caso nome_jogador não seja o nome de nenhum jogador da partida
##############################################################################
def desiste(nome_jogador):
    if not _ha_partida_em_andamento():
        return 1
    if nome_jogador not in partida_atual['jogadores']:
        return 2
    
    partida_atual['jogadores'].remove(nome_jogador)
    tabela.registra_desistencia(nome_jogador, partida_atual['data_horario'])
    if partida_atual['jogador_da_vez'] == nome_jogador:
        _passa_turno()
    partida_atual['salva'] = False
    return 0

############################################################################
# Gera uma lista de dicionários com as partidas registradas no histórico.
# 
# data_horario: data_horario da partida a buscar ou uma lista
#   com os data_horario das partidas a buscar. Se for uma lista vazia ou None,
#   busca partidas com qualquer data_horario.
# 
# status: status da partida a buscar ou uma lista com os status das partidas
#   a buscar. Se for uma lista vazia ou None, busca partidas com qualquer
#   status.
#
# Retorna uma lista de dicionários do tipo { ‘data_horario’, ‘status’ }.
#  ou retorna uma lista vazia caso não haja partida com os parâmetros passados.
#  ou retorna 1 caso um dos parâmetros seja inválido
############################################################################
def obtem_partidas(data_horario = [], status = []):
    if isinstance(data_horario, datetime):
        data_horario = [data_horario]
    if isinstance(status, str):
        status = [status]
    if not isinstance(data_horario, list) or not isinstance(status, list):
        return 1

    sqlBusca = """ SELECT * FROM Partida"""
    
    banco = banco_de_dados.abre_acesso()
    if data_horario:
        sqlBusca += ' WHERE data_horario in (%s'+\
                    ((len(data_horario)-1)*',%s') + ')'
        if status:
            sqlBusca += ' AND status in (%s' +\
                        ((len(status)-1)*',%s') + ')'
        banco['cursor'].execute(sqlBusca, tuple(data_horario+status))
    elif status:
        sqlBusca += ' WHERE status in (%s'+\
                    ((len(status)-1)*',%s') + ')'
        banco['cursor'].execute(sqlBusca, status)
    else:
        banco['cursor'].execute(sqlBusca)
    resultado = [dictPartida for dictPartida in banco['cursor']]
    banco_de_dados.fecha_acesso(banco)
    return resultado

#############################################################
# Salva a partida em andamento em um arquivo XML.
#
#  path: caminho para a pasta onde o arquivo será criado. 
#
#  retorna 0 em caso de sucesso
#   ou retorna 1 caso não haja partida em andamento
#   ou retorna 2 caso o caminho não seja econtrado
#   ou retorna 3 caso haja erro de escrita.
#
#############################################################
def salva_partida(path):
    if not _ha_partida_em_andamento():
        return 1
    if not isdir(path):
        return 2
    
    elem_partida = Element('partida')
    for key, value in partida_atual:
        if key == 'jogadores':
            elem_jogadores = SubElement(elem_partida, 'jogadores')
            for nome_jogador in value:
                elem_nome = SubElement(elem_jogadores)
                elem_nome.text = nome_jogador
        elif key == 'salva':
            pass
        else:
            elem_atributo = SubElement(elem_partida, key)
            elem_atributo.text = str(value)

    arquivo_nome = partida_atual['data_horario'].strftime('%Y%m%d%H%M%S%f')
    with open(os.path.join(path,arquivo_nome)) as xml_file:
        rough_string = ElementTree.tostring(elem_partida, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        final_string = reparsed.toprettyxml(indent="  ")
        xml_file.write(final_string)

    partida_atual['salva'] = True
    return 0

## Carrega uma partida que foi pausada anteriormente.
## data_horario: identificador da partida.
## retorna 0 em caso de sucesso
## ou retorna 1 caso a partida informada não exista
## ou retorna 3 caso a partida esteja encerrada
#def continua_partida(data_horario):
#    return
#


#Encerra a partida em andamento. O status da partida será alterado para
# 'encerrada' caso esteja salva ou 'pausada' caso não esteja salva.
#
#def encerra_partida():
#   return



##############################################################################
#
# Gera informações gerais sobre a partida atual.
# São por essas informações que a interface de usuário deve se guiar
# sobre as mudanças que ocorrem na partida.
#
# Retorna um dicionário do tipo:
#   {
#   “data_horario”,         #identificador
#   status”,               #status da partida
#   “combinacao_atual”,     #lista com os valores dos 5 dados
#   “pts_combinacoes”,      #lista com dicionários com as pontuações possíveis
#                           # (ver abaixo)
#
#   “turno_atual” ,         #número do turno atual
#   “jogador_da_vez” ,      #nome do jogador da vez
#   “tentativas” ,          #número de tentativas restantes para lançamento
#   “jogadores” ,           #lista com os nomes dos jogadores participantes
#                               (jogadores desistentes não inclusos)
#   "salva"                 #diz se a partida foi salva desde a última ação
#                               (True/False)
# }
#
# “pts_combinacoes”:
# [ { “nome”: <nome_da_categoria1>, “pontuacao”: <pontuacao_na_categoria_1> },
#   { “nome”: <nome_da_categoria2>, “pontuacao”: <pontuacao_na_categoria_2> },
#   { “nome”: <nome_da_categoria3>, “pontuacao”: <pontuacao_na_categoria_3> }
#  ... ]
#
#  Retorna 1 caso não haja uma partida em andamento.
#
##############################################################################
def obtem_info_partida():
    return partida_atual
