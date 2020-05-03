#####################################################################
# MODULO COMBINACAO
#
#  Responsável por gerar combinações de 5 dados e a sua avaliação
#  em pontos em cada categoria.
#
#--------------v0.1.0: 03/05/2020--------------------
#  Por: Daniel Menezes
#  -usando mocking do modulo avalia
#  -gera_combinacao implementada e passando nos testes
#
#  A fazer:
#   - remover mocking quando avalia for implementada
#####################################################################

from . import dado

#from .avalia import avalia_combinacao as avalia

# MODULO AVALIA AINDA NAO IMPLEMENTADO
# DESCOMENTAR O IMPORT ACIMA QUANDO FOR IMPLEMENTADA
# E APAGAR O MOCKING ABAIXO: 
from unittest import mock
avalia = mock.Mock()
avalia.return_value = [
        {'nome': '1', 'pontuacao':10},
        {'nome': '2', 'pontuacao':10},
        {'nome': '3', 'pontuacao':10},
        {'nome': '4', 'pontuacao':10},
        {'nome': '5', 'pontuacao':10},
        {'nome': '6', 'pontuacao':10},
        {'nome': 'tripla', 'pontuacao':10},
        {'nome': 'quadra', 'pontuacao':10},
        {'nome': 'fullhouse', 'pontuacao':10},
        {'nome': 'sequencia4', 'pontuacao':10},
        {'nome': 'sequencia5', 'pontuacao':10},
        {'nome': 'yahtzee', 'pontuacao':10},
        {'nome': 'chance', 'pontuacao':10}
    ]
# FIM DO MOCKING

        

__all__ = ["gera_combinacao"]

combinacao = [None, None, None, None, None]
#futuramente poderá ser inicitalizada com valores salvos ao continuar uma
#partida pausada

###############################################################################
#
#  sorteia uma nova combinação mantendo os valores dos dados escolhidos
#  dados_escolhidos: índices (inteiros no intervalo [0,4]) dos dados a terem
#  seus valores mantidos ou
#  lista vazia para modificar todos os dados
#  retorna um dicionário do tipo:
#  {“pontos”, “combinacao”}
#  “pontos” : dicionário com a pontuação da combinação em cada categoria
#  na forma
#  [ { “nome”: <nome_da_categoria1>, “pontuacao”: <pontuacao_na_categoria_1> },
#    { “nome”: <nome_da_categoria2>, “pontuacao”: <pontuacao_na_categoria_2> },
#    { “nome”: <nome_da_categoria3>, “pontuacao”: <pontuacao_na_categoria_3> }
#   ... ]
#  combinacao: lista com 5 valores de dados (inteiros no intervalo [1,6])
#  retorna 1 caso um dos índices em dados_escolhidos não seja válido
#
###############################################################################
def gera_combinacao(dados_escolhidos = []):
    if any([i not in range(5) for i in dados_escolhidos]):
        #um dos índices em dados_escolhidos não é válido
        return 1
    for i in range(5):
        if i not in dados_escolhidos:
            combinacao[i] = dado.rola(6)
    pontos = avalia(combinacao)
    return {'pontos':pontos, 'combinacao':combinacao}