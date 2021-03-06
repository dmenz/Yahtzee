import mysql.connector
import unittest
from os import path
from datetime import datetime
from entidades import *
from funcionalidades import *

def limpa_tabelas():
    tabelas = ['Tabela_Pontuacao', 'Tabela', 'Jogador', 'Partida']
    banco = banco_de_dados.abre_acesso()
    sqlDelete = "delete from "
    for tab in tabelas:
        banco['cursor'].execute(sqlDelete+tab)
    banco_de_dados.fecha_acesso(banco)

class Test(unittest.TestCase):


##########################
#      TESTES BANCO:      
#      Daniel Menezes 
#      19/05/2020
##########################
    def test_001_configura_banco_ok_condicao_retorno(self):
        print("Caso de Teste 001 - Configura banco ok condição de retorno")
        retorno = banco_de_dados.configura()
        self.assertEqual(retorno, 0)

    #Não é possível testar o erro de conexão em teste de caixa fechada

    def test_002_abre_acesso_ok_condicao_retorno(self):
        print("Caso de Teste 002 - Abre acesso tipos corretos.")
        retorno = banco_de_dados.abre_acesso()
        self.assertTrue( isinstance(retorno['conexao'],
                         mysql.connector.connection.MySQLConnection)
                     and
                         isinstance(retorno['cursor'],
                         mysql.connector.cursor.MySQLCursor))
        retorno['conexao'].close()
        retorno['cursor'].close()

    # Não há como testar o retorno 1 de abre_acesso em teste de caixa
    # fechada.

    def test_003_fecha_acesso_ok_condicao_retorno(self):
        print("Caso de Teste 003 - Fecha acesso Condição de retorno ok.")
        dic = banco_de_dados.abre_acesso()
        retorno = banco_de_dados.fecha_acesso(dic)
        self.assertEqual(retorno, 0)


    # Não há como testar o retorno 1 de fecha_acesso em teste de caixa
    # fechada.

    def test_004_fecha_acesso_nok_condicao_retorno_tipo_invalido(self):
        print("Caso de Teste 004 - Fecha acesso parâmetros inválidos.")
        retorno = banco_de_dados.fecha_acesso(
                    {'conexao':1, 'cursor':'daniel'}
                )
        self.assertEqual(retorno, 2)


##########################
#      TESTES DADO:      
#      Daniel Menezes 
#      24/04/2020
##########################

    def test_005_rola_ok_intervalo(self):
        print("Caso de Teste 005 - Valores dos dados dentro do intervalo.")
        correto = False
        for i in range(4):
            correto = dado.rola(6) in range(1,7)
            if not correto:
                break
        self.assertTrue(correto)
    
    def test_006_rola_ok_aleatorio(self):
        print("Caso de Teste 006 - Dados gerando valores diferentes.")
        primeiro_valor = dado.rola(6)
        for i in range(10):
            if primeiro_valor != dado.rola(6):
                diferente = True
        self.assertTrue(diferente)

    def test_007_rola_nok_faces_invalido(self):
        print("Caso de Teste 007 - Valor invalido de n_faces.")
        self.assertEqual(-1, dado.rola(-1))
        

##########################
#      TESTES CATEGORIA:      
#      Daniel Menezes 
#      24/04/2020
##########################


    def test_008_obtem_nomes_ok_retorna_lista(self):
        print("Caso de Teste 008 - Retorno de obtem nomes é uma lista.")
        self.assertTrue(type(categoria.obtem_nomes()) is list)

    def test_009_obtem_nomes_ok_lista_com_nomes(self):
        print("Caso de Teste 009 - Lista possui dicionario com nome.")
        categorias = categoria.obtem_nomes()
        self.assertTrue(all('nome' in categoria for categoria in categorias))
    
    def test_010_obtem_descricoes_ok_retorna_lista(self):
        print("Caso de Teste 010 - Retorno de obtem_descricoes é uma lista.")
        self.assertTrue(type(categoria.obtem_descricoes()) is list)

    def test_011_obtem_descricoes_ok_lista_com_descricao(self):
        print("Caso de Teste 011 - Lista possui dicionario com nome e descricao.")
        descricoes = categoria.obtem_descricoes()
        iterador = ('nome' and 'descricao' in categoria for categoria in descricoes)
        self.assertTrue(all(iterador))


##########################
#      TESTES AVALIA:      
#      Daniel Menezes 
#      25/04/2020
##########################

    def test_012_avalia_combinacao_ok_1(self):
        print("Caso de Teste 012 - Combinacao avaliada corretamente na categoria '1'")
        retorno = avalia.avalia_combinacao([1,2,1,5,1])
        self.assertIn( {'nome':'1', 'pontuacao':3}, retorno )
    
    def test_013_avalia_combinacao_ok_2(self):
        print("Caso de Teste 013 - Combinacao avaliada corretamente na categoria '2'")
        retorno = avalia.avalia_combinacao([1,2,1,2,2])
        self.assertIn( {'nome':'2', 'pontuacao':6}, retorno )
        
    def test_014_avalia_combinacao_ok_3(self):
        print("Caso de Teste 014 - Combinacao avaliada corretamente na categoria '3'")
        retorno = avalia.avalia_combinacao([1,3,1,3,3])
        self.assertIn( {'nome':'3', 'pontuacao':9}, retorno )
        
    def test_015_avalia_combinacao_ok_4(self):
        print("Caso de Teste 015 - Combinacao avaliada corretamente na categoria '4'")
        retorno = avalia.avalia_combinacao([6,4,1,3,2])
        self.assertIn( {'nome':'4', 'pontuacao':4}, retorno )

    def test_016_avalia_combinacao_ok_5(self):
        print("Caso de Teste 016 - Combinacao avaliada corretamente na categoria '5'")
        retorno = avalia.avalia_combinacao([5,4,5,3,2])
        self.assertIn( {'nome':'5', 'pontuacao':10}, retorno )

    def test_017_avalia_combinacao_ok_6(self):
        print("Caso de Teste 017 - Combinacao avaliada corretamente na categoria '6'")
        retorno = avalia.avalia_combinacao([6,4,6,6,2])
        self.assertIn( {'nome':'6', 'pontuacao':18}, retorno )
        
    def test_018_avalia_combinacao_ok_tripla(self):
        print("Caso de Teste 018 - Combinacao avaliada corretamente na categoria 'tripla'")
        retorno = avalia.avalia_combinacao([3,4,3,3,2])
        self.assertIn( {'nome':'tripla', 'pontuacao':15}, retorno )

    def test_019_avalia_combinacao_ok_quadra(self):
        print("Caso de Teste 019 - Combinacao avaliada corretamente na categoria 'quadra'")
        retorno = avalia.avalia_combinacao([6,4,6,6,6])
        self.assertIn( {'nome':'quadra', 'pontuacao':28}, retorno )

    def test_020_avalia_combinacao_ok_fullhouse(self):
        print("Caso de Teste 020 - Combinacao avaliada corretamente na categoria 'fullhouse'")
        retorno = avalia.avalia_combinacao([6,4,4,6,6])
        self.assertIn( {'nome':'fullhouse', 'pontuacao':25}, retorno )

    def test_021_avalia_combinacao_ok_sequencia4(self):
        print("Caso de Teste 021 - Combinacao avaliada corretamente na categoria 'sequencia4'")
        retorno = avalia.avalia_combinacao([3,2,4,2,5])
        self.assertIn( {'nome':'sequencia4', 'pontuacao':30}, retorno )

    def test_022_avalia_combinacao_ok_sequencia5(self):
        print("Caso de Teste 022 - Combinacao avaliada corretamente na categoria 'sequencia5'")
        retorno = avalia.avalia_combinacao([3,2,4,6,5])
        self.assertIn( {'nome':'sequencia5', 'pontuacao':40}, retorno )

    def test_023_avalia_combinacao_ok_yahtzee(self):
        print("Caso de Teste 023 - Combinacao avaliada corretamente na categoria 'yahtzee'")
        retorno = avalia.avalia_combinacao([3,3,3,3,3])
        self.assertIn( {'nome':'yahtzee', 'pontuacao':50}, retorno )
        
    def test_024_avalia_combinacao_ok_chance(self):
        print("Caso de Teste 024 - Combinacao avaliada corretamente na categoria 'chance'")
        retorno = avalia.avalia_combinacao([3,2,4,6,5])
        self.assertIn( {'nome':'chance', 'pontuacao':20}, retorno )



    
##########################
#      TESTES COMBINACAO:      
#      Bruno Coutinho 
#      24/04/2020
##########################

    def test_025_gera_combinacao_ok_mantem_dados_escolhidos(self):
        print("Caso de Teste 025 - Combinacao gerada manteve dados escolhidos")
        primeira_combinacao = combinacao.gera_combinacao([])
        primeira_combinacao = primeira_combinacao['combinacao']
        primeira_indice2 = primeira_combinacao[2]
        primeira_indice3 = primeira_combinacao[3]
        nova_combinacao = combinacao.gera_combinacao([2,3])
        nova_combinacao = nova_combinacao['combinacao']
        nova_indice2 = nova_combinacao[2]
        nova_indice3 = nova_combinacao[3]
        self.assertEqual((primeira_indice2,primeira_indice3),
                         (nova_indice2, nova_indice3))

    def test_026_gera_combinacao_ok_altera_dados_descartados(self):
        print("Caso de Teste 026 - Combinacao gerada alterou dados descartados")
        primeira_combinacao = combinacao.gera_combinacao([])
        primeira_combinacao = primeira_combinacao['combinacao']
        primeira_indice0 = primeira_combinacao[0]
        primeira_indice1 = primeira_combinacao[1]
        primeira_indice4 = primeira_combinacao[4]
        descartados_alterados = False
        for i in range(10):
            nova_combinacao = combinacao.gera_combinacao([2,3])
            nova_combinacao = nova_combinacao['combinacao']
            if nova_combinacao[0] != primeira_indice0 or\
               nova_combinacao[1] != primeira_indice1 or\
               nova_combinacao[4] != primeira_indice4:
                descartados_alterados = True
        self.assertTrue(descartados_alterados)

    def test_027_gera_combinacao_nok_indice_invalido(self):
        print("Caso de Teste 027 - Nao gera combinacao caso indice invalido")
        retorno_esperado = combinacao.gera_combinacao([2,7,-1])
        self.assertEqual(retorno_esperado, 1)

    def test_028_inicializa_combinacao_ok_condicao_retorno(self):
        print("Caso de Teste 028 - Inicializa combinacao com sucesso")
        retorno_esperado = combinacao.inicializa_combinacao([2,3,2,5,5])
        self.assertEqual(retorno_esperado, 0)

    def test_029_inicializa_combinacao_nok_tamanho_invalido(self):
        print("Caso de Teste 029 - Nao inicializa combinacao caso tamanho" +
              " da lista seja invalido")
        retorno_esperado = combinacao.inicializa_combinacao([2,3,2,5,5,7])
        self.assertEqual(retorno_esperado, 1)

    def test_030_inicializa_combinacao_ok_condicao_retorno(self):
        print("Caso de Teste 030 - Nao inicializa combinacao caso algum dado" +
              " tenha valor invalido")
        retorno_esperado = combinacao.inicializa_combinacao([8,3,2,-1,5])
        self.assertEqual(retorno_esperado, 2)


##########################
#      TESTES JOGADOR:      
#      Bruno Coutinho 
#      25/04/2020
##########################

    def test_031_insere_jogador_ok_condicao_retorno(self):
        print("Caso de Teste 031 - Insere jogador com sucesso")
        retorno_esperado = jogador.insere('maria')
        self.assertEqual(retorno_esperado, 0)

    def test_032_insere_jogador_ok_inserido_com_sucesso(self):
        print("Caso de Teste 032 - Verifica insercao")
        self.assertTrue(jogador.valida_jogador('maria'))

    def test_033_insere_jogador_nok_nome_nulo(self):
        print("Caso de Teste 033 - Impede insercao caso nome seja nulo")
        retorno_esperado = jogador.insere('')
        self.assertEqual(retorno_esperado, 1)

    def test_034_insere_jogador_nok_nome_existente(self):
        print("Caso de Teste 034 - Impede insercao caso nome ja exista")
        retorno_esperado = jogador.insere('maria')
        self.assertEqual(retorno_esperado, 2)

    def test_035_remove_jogador_ok_condicao_retorno(self):
        print("Caso de Teste 035 - Remove jogador com sucesso")
        retorno_esperado = jogador.remove('maria')
        self.assertEqual(retorno_esperado, 0)

    def test_036_remove_jogador_ok_removido_com_sucesso(self):
        print("Caso de Teste 036 - Verifica remocao")
        self.assertFalse(jogador.valida_jogador('maria'))

    def test_037_remove_jogador_nok_nome_invalido(self):
        print("Caso de Teste 037 - Impede remocao caso nome invalido")
        retorno_esperado = jogador.remove('carlos')
        self.assertEqual(retorno_esperado, 1)

    def test_038_obtem_info_ok(self):
        print("Caso de Teste 038 - Obter info de jogadores")
        jogador.insere('joao')
        info_joao = jogador.obtem_info(['joao'])[0]
        self.assertEqual((info_joao['nome'],
                          info_joao['pontuacao_total'],
                          info_joao['recorde']),
                         ('joao',0,0))

    def test_039_obtem_info_nok_jogador_nao_encontrado(self):
        print("Caso de Teste 039 - obtem_info retorna lista"
              + " vazia se nomes nao encontrados")
        retorno_esperado = jogador.obtem_info(['julia'])
        self.assertEqual(retorno_esperado, [])

    def test_040_obtem_info_ok_todos_os_jogadores(self):
        print("Caso de Teste 040 - obtem_info mostra todos os jogadores "+
                "com lista vazia no input.")
        retorno_esperado = jogador.obtem_info([])[0]
        self.assertEqual((retorno_esperado['nome'],
                          retorno_esperado['pontuacao_total'],
                          retorno_esperado['recorde']),
                         ('joao',0,0))

    def test_041_obtem_info_nok_input_invalido(self):
        print("Caso de Teste 041 - obtem_info erro com input inválido")
        retorno_esperado = jogador.obtem_info([1,2,3])
        self.assertEqual( retorno_esperado, 1 )


    def test_042_atualiza_info_ok_condicao_retorno(self):
        print("Caso de Teste 042 - Atualiza pontuacao total,"+
              " ranking e recorde de jogador com sucesso")
        retorno_esperado = jogador.atualiza_info('joao', 100)
        self.assertEqual(retorno_esperado, 0)

    def test_043_atualiza_info_ok_atualiza_com_sucesso(self):
        print("Caso de Teste 043 - Verifica atualizacao")
        info_joao = jogador.obtem_info(['joao'])[0]
        self.assertEqual((info_joao['pontuacao_total'],
                          info_joao['recorde']),(100,100))

    def test_044_atualiza_info_nok_nome_invalido(self):
        print("Caso de Teste 044 - Impede atualizacao caso nome invalido")
        retorno_esperado = jogador.atualiza_info('carlos', 80)
        self.assertEqual(retorno_esperado, 1)

    def test_045_atualiza_info_pontos_negativos(self):
        print("Caso de Teste 045 - Impede atualizacao caso pontuacao negativa")
        retorno_esperado = jogador.atualiza_info('joao', -80)
        self.assertEqual(retorno_esperado, 2)

    def test_046_valida_jogador_nome_registrado(self):
        print("Caso de Teste 046 - valida jogador existente")
        retorno_esperado = jogador.valida_jogador('joao')
        self.assertTrue(retorno_esperado)

    def test_047_valida_jogador_nome_nao_registrado(self):
        print("Caso de Teste 047 - nao valida jogador nao registrado")
        retorno_esperado = jogador.valida_jogador('paula')
        self.assertFalse(retorno_esperado)



##########################
#      TESTES TABELA:      
#      Bruno Coutinho 
#      25/04/2020
##########################

    def test_048_cria_tabela_ok_condicao_retorno(self):
        print("Caso de Teste 048 - Cria tabela com sucesso")
        jogador.insere('eduardo')

        #adiciona partida ao bd para ser usada para testes. Adicionamos
        #direto ao bd para saber o data_horaio identificador, que é
        #gerado automaticamente pelo módulo partida e fica encapsulado nele
        
        banco = banco_de_dados.abre_acesso()
        data_horario = datetime(2020,2,2,10)
        sql_teste = """INSERT INTO Partida VALUES (%s, %s)"""
        banco['cursor'].execute(sql_teste, (data_horario, 'encerrada'))
        banco_de_dados.fecha_acesso(banco)

        retorno_esperado = tabela.cria_tabela('eduardo', data_horario) 
        self.assertEqual(retorno_esperado, 0)

    def test_049_cria_tabela_ok_criada_com_sucesso(self):
        print("Caso de Teste 049 - Verifica criacao de tabela")
        temp = tabela.obtem_tabelas(['eduardo'], [datetime(2020,2,2,10)])
        self.assertEqual((temp[0]['nome_jogador'],
                          temp[0]['data_horario'],
                          temp[0]['pontuacao_total'],
                          temp[0]['colocacao'],
                          temp[0]['desistencia']),
                         ('eduardo',datetime(2020,2,2,10),0, None, False))

    def test_050_cria_tabela_nok_nome_inexistente(self):
        print("Caso de Teste 050 - Impede criacao de tabela caso" +
              " nao exista jogador com nome fornecido")
        retorno_esperado = tabela.cria_tabela('norma', datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 1)

    def test_051_cria_tabela_nok_tabela_ja_existente(self):
        print("Caso de Teste 051 - Impede criacao de tabela caso" + 
              " jogador já possua tabela na partida")
        retorno_esperado = tabela.cria_tabela('eduardo',datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 2)

    def test_052_insere_pontuacao_ok_condicao_retorno(self):
        print("Caso de Teste 052 - Insere pontuacao com sucesso")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo',datetime(2020,2,2,10),
                                                   categ,30)
        self.assertEqual(retorno_esperado, 0)

    def test_053_insere_pontuacao_ok_insere_com_sucesso(self):
        print("Caso de Teste 053 - Verifica insercao")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        temp = tabela.obtem_tabelas(['eduardo'], [datetime(2020,2,2,10)])
        temp = temp[0]['pontos_por_categoria'] #pontos por categoria do eduardo
        pontos_categ = next(pontos for pontos in temp if pontos['nome']==categ)
        self.assertEqual(pontos_categ['pontuacao'], 30)

    def test_054_insere_pontuacao_nok_tabela_nao_existe(self):
        print("Caso de Teste 054 - Nao insere se a tabela informada nao existir")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('karla',datetime(2020,2,2,10),
                                                   categ, 30)
        self.assertEqual(retorno_esperado, 1)

    def test_055_insere_pontuacao_nok_categoria_nao_existe(self):
        print("Caso de Teste 055 - Nao insere se a" +
              " categoria informada nao existir")
        retorno_esperado = tabela.insere_pontuacao('eduardo',
                                                   datetime(2020,2,2,10),
                                                   'categ_falsa', 30)
        self.assertEqual(retorno_esperado, 2)

    def test_056_insere_pontuacao_nok_pontos_negativos(self):
        print("Caso de Teste 056 - Nao insere se a quantidade de"+
              " pontos for negativa")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo',datetime(2020,2,2,10),
                                                   categ, -30)
        self.assertEqual(retorno_esperado, 3)

    def test_057_insere_pontuacao_nok_categoria_ja_pontuada(self):
        print("Caso de Teste 057 - Nao insere se" +
              " o jogador ja marcou pontos na categoria informada")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo',datetime(2020,2,2,10),
                                                   categ, 30)
        self.assertEqual(retorno_esperado, 4)

    def test_058_registra_desistencia_ok_condicao_retorno(self):
        print("Caso de Teste 058 - registra desistencia com sucesso")
        jogador.insere('jorge')
        tabela.cria_tabela('jorge',datetime(2020,2,2,10))
        retorno_esperado = tabela.registra_desistencia('jorge',
                                                       datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 0)

    def test_059_registra_desistencia_ok_zera_nao_pontuadas(self):
        print("Caso de Teste 059 - Verifica se categorias nao pontuadas" +
              " foram zeradas ao desistir")
        zeradas = True
        temp = tabela.obtem_tabelas(['jorge'],[datetime(2020,2,2,10)])
        pontos_categ = temp[0]['pontos_por_categoria']
        for categ in pontos_categ:
            if categ['pontuacao']!=0:
                zeradas = False
        self.assertTrue(zeradas)

    def test_060_registra_desistencia_ok_desiste_com_sucesso(self):
        print("Caso de Teste 060 - Verifica desistencia")
        temp = tabela.obtem_tabelas(['jorge'], [datetime(2020,2,2,10)])
        confere_desistiu = temp[0]['desistencia']
        self.assertTrue(confere_desistiu)

    def test_061_registra_desistencia_nok_tabela_nao_existe(self):
        print("Caso de Teste 061 - impede desistencia caso tabela" +
              " do jogador na partida nao exista")
        retorno_esperado = tabela.registra_desistencia('karla',
                                                       datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 1)

    def test_062_registra_desistencia_nok_todas_categorias_pontuadas(self):
        print("Caso de Teste 062 - impede desistencia caso jogador" +
              " ja tenha pontuado em todas as categorias")
        categorias = categoria.obtem_nomes()
        for categ in categorias[1:]:  
            nome_cat = categ['nome']
            tabela.insere_pontuacao('eduardo',datetime(2020,2,2,10),
                                                   nome_cat,30)
        retorno_esperado = tabela.registra_desistencia('eduardo',
                                                       datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 2)

    def test_063_obtem_tabelas_ok(self):
        print("Caso de Teste 063 - Obter tabelas de jogadores nas partidas")
        temp = tabela.obtem_tabelas(['eduardo'],[datetime(2020,2,2,10)])
        n_categorias = len(categoria.obtem_nomes())
        self.assertEqual((temp[0]['nome_jogador'],
                          temp[0]['data_horario'],
                          temp[0]['pontuacao_total'],
                          temp[0]['desistencia']),
                         ('eduardo',datetime(2020,2,2,10),
                          30 * n_categorias,False))

    def test_064_obtem_tabelas_ok_colocacoes_corretas(self):
        print("Caso de Teste 064 - Tabelas calculam colocacoes corretamente")
        tab_ed = tabela.obtem_tabelas(['eduardo'],[datetime(2020,2,2,10)])
        tab_jorge = tabela.obtem_tabelas(['jorge'],[datetime(2020,2,2,10)])
        self.assertEqual((tab_ed[0]['colocacao'], tab_jorge[0]['colocacao']),
                         (1,2))

    def test_065_obtem_tabelas_ok_colocacoes_corretas(self):
        print("Caso de Teste 065 - Pontos por categoria corretos")
        tab_edu = tabela.obtem_tabelas(['eduardo'],[datetime(2020,2,2,10)])
        n_categorias = len(categoria.obtem_nomes())
        todos_pontos_iguais_a_30 = True
        for i in range(n_categorias):
            if tab_edu[0]['pontos_por_categoria'][i]['pontuacao'] !=30:
                todos_pontos_iguais_a_30 = False
        self.assertTrue(todos_pontos_iguais_a_30)
        
    def test_066_obtem_tabelas_nok_parametros_invalidos(self):
        print("Caso de Teste 066 - obtem_info retorna 1 se as listas não"
              + " possuirem nenhuma combinacao(nome,data_horario) valida")
        retorno_esperado = tabela.obtem_tabelas(['pedro'],[datetime(2020,2,2,10)])
        self.assertEqual(retorno_esperado, 1)
        
    def test_067_remove_ok_condicao_retorno(self):
        print("Caso de Teste 067 - remove tabela de um jogador" +
              " em uma partida com sucesso")
        retorno_esperado = tabela.remove('eduardo',datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 0)

    def test_068_remove_ok_retira_com_sucesso(self):
        print("Caso de Teste 068 - Verifica remocao")
        retorno_esperado = tabela.obtem_tabelas(['eduardo'],
                                                [datetime(2020,2,2,10)])
        self.assertEqual(retorno_esperado, 1)#pois obtem retorna 1 se n acha tabela

    def test_069_remove_nok_tabela_nao_existe(self):
        print("Caso de Teste 069 - impede remocao caso tabela" +
              "do jogador na partida nao exista")
        retorno_esperado = tabela.remove('eduardo',datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 1)



##########################
#      TESTES PARTIDA:      
#      Daniel Menezes 
#      25/04/2020
##########################

    def test_070_inicia_partida_nok_jogador_nao_existente(self):
        print("Caso de Teste 070 - Inicia partida nao aceita jogador"+
            " inexistente.")
        retorno = partida.inicia_partida(["juan"])
        self.assertEqual( retorno , 1 )

    def test_071_obtem_info_artida_nok_sem_partida(self):
        print("Caso de Teste 071 - Erro em obtem info sem nenhuma"+
                " partida em andamento.")
        retorno = partida.obtem_info_partida()
        self.assertEqual(retorno, 1)

    def test_072_faz_lancamento_nok_partida_sem_partida(self):
        print("Caso de Teste 072 - Erro em fazer lancamento sem nenhuma"+
                " partida em andamento.")
        retorno = partida.faz_lancamento([1,2])
        self.assertEqual( retorno, 1 )
        
    def test_073_marca_pontuacao_nok_sem_partida(self):
        print("Caso de Teste 073 - Erro ao marcar pontuacao sem nenhuma"+
                " partida em andamento.")
        retorno = partida.marca_pontuacao('1')
        self.assertEqual( retorno, 1 )

    def test_074_para_partida_nok_sem_partida(self):
        print("Caso de Teste 074 - Erro ao encerrar partida sem nenhuma"+
                " partida em andamento.")
        retorno = partida.para_partida()
        self.assertEqual( retorno, 1 )

    def test_075_desiste_nok_sem_partida(self):
        print("Caso de Teste 075 - Erro desiste sem partida em andamento.")
        retorno = partida.desiste('flavio')
        self.assertEqual( retorno, 1 )

    def test_076_salva_partida_nok_sem_partida(self):
        print("Caso de Teste 076 - Erro salva_partida sem partida em"+
                " andamento.")
        dir_raiz = path.dirname(path.realpath(__file__))
        saves = path.join(dir_raiz, 'saves') 
        retorno = partida.salva_partida(saves)
        self.assertEqual(retorno, 1)

    def test_077_inicia_partida_ok_condicao_retorno(self):
        print("Caso de Teste 077 - Inicia partida com sucesso.")
        jogador.insere("flavio")
        jogador.insere("lucas")
        jogador.insere("julia")
        retorno = partida.inicia_partida(["flavio", "lucas", "julia"])
        self.assertIsInstance(retorno, datetime)
   
    def test_078_inicia_partida_ok_jogadores_corretos(self):
        print("Caso de Teste 078 - Obtem info com jogadores corretos.")
        jogadores = partida.obtem_info_partida()['jogadores']
        self.assertSetEqual(set(jogadores), set(['flavio', 'lucas', 'julia']))

    def test_079_inicia_partida_nok_partida_em_andamento(self):
        print("Caso de Teste 079 - Inicia partida recusa iniciar partida"+
                " com outra partida em andamento.")
        retorno = partida.inicia_partida(["lucas"])
        self.assertEqual( retorno , 2 )

    def test_080_faz_lancamento_nok_indice_invalido(self):
        print("Caso de Teste 080 - Erro em fazer lancamento com indices de "+
                "dados invalidos.")
        retorno = partida.faz_lancamento([-1,5])
        self.assertEqual(retorno, 2)

    def test_081_faz_lancamento_nok_indice_primeiro_lancamento_indice(self):
        print("Caso de Teste 081 - Erro em fazer primeiro lancamento do turno"+
                " com indices de dados escolhidos.")
        retorno = partida.faz_lancamento([1,3])
        self.assertEqual(retorno, 3)

    def test_082_marca_pontuacao_nok_jogador_do_turno_nao_lancou(self):
        print("Caso de Teste 082 - Erro ao marcar pontuacao sem lancar"+
                " dados no turno.")
        retorno = partida.marca_pontuacao('2')
        self.assertEqual( retorno, 3 )

    def test_083_faz_lancamento_ok(self):
        print("Caso de Teste 083 - Faz lancamento em partida com sucesso.")
        retorno = partida.faz_lancamento([])
        self.assertEqual(retorno, 0)

    def test_084_faz_lancamento_ok_reduziu_tentativas(self):
        print("Caso de Teste 084 - Faz lancamento reduz o numero de"+
                " tentativas.")
        info = partida.obtem_info_partida()
        self.assertEqual( info['tentativas'], 2 )

    def test_085_faz_lancamento_nok_tentativas_esgotadas(self):
        print("Caso de Teste 085 - Faz lancamento erro quando o jogador já"+
                " esgotou suas tentativas.")
        partida.faz_lancamento([])
        partida.faz_lancamento([])
        retorno = partida.faz_lancamento([])
        self.assertEqual(retorno, 4)

    def test_086_faz_lancamento_ok_combinacao_gerada_com_sucesso(self):
        print("Caso de Teste 086 - Faz lancamento combinação gerada.")
        info = partida.obtem_info_partida()
        combinacao = info['combinacao']
        dados = ([ dadoNum for dadoNum in combinacao if dadoNum in range(1,7)])
        #confere que tem 5 numeros [1,6] na lista retornada
        self.assertEqual( len(dados), 5 )  
       
    def test_087_marca_pontuacao_nok_categoria_invalida(self):
        print("Caso de Teste 087 - Erro ao marcar pontuacao invalida.")
        partida.faz_lancamento([])
        retorno = partida.marca_pontuacao('abacate')
        self.assertEqual( retorno, 2 )

    def test_088_marca_pontuacao_ok_sucesso(self):
        print("Caso de Teste 088 - Marca pontuacao em uma categoria com"+
                " sucesso.")
        retorno = partida.marca_pontuacao('chance')
        self.assertEqual( retorno, 0 )

    def test_089_marca_pontuacao_ok_passou_o_turno(self):
        print("Caso de Teste 089 - Marca pontuacao passou o turno.")
        turno = partida.obtem_info_partida()['turno']
        self.assertEqual( turno, 2 )

    def test_090_marca_pontuacao_ok_restaura_tentativa(self):
        print("Caso de Teste 090 - Marca pontuacao proximo jogador tem 3"+
                " tentativas.")
        info = partida.obtem_info_partida()['tentativas']
        self.assertEqual( info, 3 )

    def test_091_desiste_ok_condicao_retorno(self):
        print("Caso de Teste 091 - Desiste com sucesso.")
        retorno = partida.desiste('julia')
        self.assertEqual( retorno, 0 )

    def test_092_desiste_ok_retira_jogador(self):
        print("Caso de Teste 092 - Desiste retira jogador da partida.")
        jogadores = partida.obtem_info_partida()['jogadores']
        self.assertNotIn( 'julia', jogadores )

    def test_093_desiste_nok_nome_invalido(self):
        print("Caso de Teste 093 - Erro desiste jogador invalido.")
        retorno = partida.desiste('julia')
        self.assertEqual( retorno, 2 )

    def test_094_marca_pontuacao_nok_jogador_ja_marcou_na_categoria(self):
        print("Caso de Teste 094 - Erro ao marcar pontuacao ja marcada"+
                " pelo jogador.")
        partida.faz_lancamento([]) 
        partida.marca_pontuacao('chance')
        partida.faz_lancamento([]) 
        partida.marca_pontuacao('chance')
        partida.faz_lancamento([])
        retorno = partida.marca_pontuacao('chance')
        self.assertEqual( retorno, 4 )

    def test_095_salva_partida_ok_condicao_retorno(self):
        print("Caso de Teste 095 - Salva partida sucesso.")
        dir_raiz = path.dirname(path.realpath(__file__))
        arquivo = open(path.join(dir_raiz, 'saves','test_salva_partida_ok.xml'),"w")
        retorno = partida.salva_partida(arquivo)
        self.assertEqual(retorno, 0)

    def test_096_salva_partida_nok_path_invalido(self):
        print("Caso de Teste 096 - Erro salva_partida caminho não encontrado")
        dir_raiz = path.dirname(path.realpath(__file__))
        saves = path.join(dir_raiz, 'pasta_nao_existente') 
        retorno = partida.salva_partida(saves)
        self.assertEqual(retorno, 2)

    def test_097_para_partida_ok_condicao_retorno(self):
        print("Caso de Teste 097 - Encerra partida com sucesso.")
        retorno = partida.para_partida()
        self.assertEqual( retorno, 0 )

    def test_098_continua_partida_ok(self):
        print("Caso de Teste 098 - Continua partida com sucesso.")
        nome_arquivo = 'test_salva_partida_ok.xml'
        arq = path.join(path.realpath(path.dirname(__file__)),'saves',nome_arquivo)
        retorno = partida.continua_partida(arq)
        self.assertEqual( retorno, 0 )

    def test_099_continua_partida_nok_arquivo_inexistente(self):
        print("Caso de Teste 099 - Continua partida Erro ao não encontrar o arquivo")
        retorno = partida.continua_partida('arquivo_nao_existente') 
        self.assertEqual( retorno, 1 )

    def test_100_obtem_info_partida_ok_condicao_retorno(self):
        print("Caso de Teste 100 - obtem_info_partida condição de retorno ok.")
        retorno = partida.obtem_info_partida()
        self.assertEqual(set(retorno.keys()), {'data_horario',
                                        'status',
                                        'combinacao',
                                        'pts_combinacao',
                                        'turno',
                                        'jogador_da_vez',
                                        'tentativas',
                                        'jogadores',
                                        'salva'})

    def test_101_obtem_partidas_ok_condicao_retorno(self):
        print("Caso de Teste 101 - obtem_partidas condicao de retorno ok")
        retorno = partida.obtem_partidas(status = 'andamento')
        data_horario = partida.obtem_info_partida()['data_horario']
        self.assertIn({'data_horario':data_horario, 'status':'andamento'},
                      retorno)

    def test_102_obtem_partidas_ok_condicao_retorno2(self):
        print("Caso de Teste 102 - obtem_partidas condicao de retorno ok"+
                " partida nao encontrada.")
        retorno = partida.obtem_partidas(datetime(2019,1,1,2,1,3))
        self.assertEqual(retorno, [])

    def test_103_obtem_partidas_nok_parametro_invalido(self):
        print("Caso de Teste 103 - obtem_partidas erro com parametro invalido")
        retorno = partida.obtem_partidas('parametro_invalido', [1])
        self.assertEqual( retorno, 1 )


unittest.main(exit=False)
limpa_tabelas()