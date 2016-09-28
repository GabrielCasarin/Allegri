# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import os
import math
import string
from comum import Simulador
from configuracoes import ROOT_DIR


class decompoe_texto_fonte(Simulador):
    def __init__(self, log_decompoe_texto_fonte=False,
                 log_imprimir_linhas=False, log_imprimir_caracteres=False,
                 imprimir_listagem=False):
        super(decompoe_texto_fonte, self).__init__()
        self.log_decompoe_texto_fonte = log_decompoe_texto_fonte
        self.log_imprimir_linhas = log_imprimir_linhas
        self.log_imprimir_caracteres = log_imprimir_caracteres
        self.imprimir_listagem = imprimir_listagem
        self.categorias = {}

    def trata_evento(self, evento):
        if evento == '<LeituraLinha>':
            self.LeituraLinha()
        elif evento == '<FimArquivo>':
            self.FimArquivo()
        elif evento == '<ChegadaCaractere>':
            self.ChegadaCaractere()

    def LeituraLinha(self):
        linha = self.arquivo_fonte.readline()
        if linha != '':
            self.linhas_indexadas.append((self.cont_linhas, linha))
            if self.log_imprimir_linhas:
                print("<LeituraLinha>      {0[0]} {0[1]}".format(self.linhas_indexadas[-1]), end='')
            self.cont_linhas += 1
            # add eventos
            self.cursor = 0
            for char in linha:
                self.add_evento('<ChegadaCaractere>')
            self.add_evento('<LeituraLinha>')
        else:
            self.add_evento('<FimArquivo>')

    def FimArquivo(self):
        if self.log_imprimir_linhas:
            print("<FimArquivo>        chegou ao fim do arquivo fonte '{}'".format(self.arquivo_fonte.name))
        self.arquivo_fonte.close()

    def add_categoria(self, categoria, conjunto):
        if categoria not in self.categorias:
            self.categorias[categoria] = set()
        for el in conjunto:
            self.categorias[categoria].add(el)

    def ChegadaCaractere(self):
        num_linha, linha = self.linhas_indexadas[-1]
        char = linha[self.cursor]
        for categoria, conjunto in self.categorias.items():
            if char in conjunto:
                classificacao = categoria
        self.caracteres_classificados.append((char, classificacao))
        if self.log_imprimir_caracteres:
            print("<ChegadaCaractere>    {0[0]} (ascii HEX {1:X}) {0[1]}".format(self.caracteres_classificados[-1], ord(self.caracteres_classificados[-1][0])))
        self.cursor += 1

    def __call__(self, nome_arquivo_fonte):
        if self.log_decompoe_texto_fonte:
            print('entrei na sub-rotina de extração de texto fonte...')

        try:
            self.arquivo_fonte = open(nome_arquivo_fonte)
            self.cont_linhas = 0
            self.linhas_indexadas = []
            self.caracteres_classificados = []

            self.add_evento('<LeituraLinha>')
            self.run()

        except Exception as e:
            raise e

        if self.log_decompoe_texto_fonte:
            print('saí da sub-rotina de extração de texto fonte.')

        if self.imprimir_listagem:
            LOG_DIR = os.path.join(ROOT_DIR, 'log')
            with open(os.path.join(LOG_DIR, 'linhas_indexadas.txt'), 'w') as arq_out:
                for el in self.linhas_indexadas:
                    arq_out.write("{0[0]:{1}} {0[1]}".format(el, num_linhas))
            with open(os.path.join(LOG_DIR, 'caracteres_classificados.txt'), 'w') as arq_out:
                for el in self.caracteres_classificados:
                    arq_out.write("{0[0]} {0[1]}\n".format(el))


class classificador_lexico(Simulador):
    def __init__(self, automato, decompositor, log=False):
        super(classificador_lexico, self).__init__()
        self.__automato = automato
        self.__decompositor = decompositor
        self.__log = log
        self.__classificacoes = {}

    def __call__(self, arquivo_fonte):
        self.__decompositor(arquivo_fonte)
        self.add_evento(('<PartidaInicial>', ))
        self.run()

    def add_classificacao(self, estado_final, classificacao):
        self.__classificacoes[estado_final] = classificacao

    def categorizar(self):
        # por default, o tipo do token é igual a ele mesmo
        token_tipo = self.token_atual
        for estado_final, classificacao in self.__classificacoes.items():
            # até que se prove o contrário
            if self.__automato._estadoAtual == estado_final:
                token_tipo = classificacao
        self.tokens.append((self.token_atual, token_tipo))


    def trata_evento(self, evento):
        if evento[0] == '<PartidaInicial>':
            self.PartidaInicial()
        elif evento[0] == '<ReiniciarAutomato>':
            self.ReiniciarAutomato()
        elif evento[0] == '<ChegadaSimbolo>':
            self.ChegadaSimbolo(evento[1])
        elif evento[0] == '<CursorParaDireita>':
            self.CursorParaDireita()
        elif evento[0] == '<ExecutarTransducao>':
            self.ExecutarTransducao(evento[1])

    def PartidaInicial(self):
        # poe o automato no estado inicial
        self.__automato.inicializar()
        # põe os dados na "fita"
        self.__caracteres = iter(self.__decompositor.caracteres_classificados)
        self.token_atual = ''
        self.token_tipo = None
        self.token_valor = 0 # Para numerais
        self.tokens = []
        self.add_evento(('<CursorParaDireita>', ))
        if self.__log:
            print('<PartidaInicial>\n')

    def ReiniciarAutomato(self):
        if self.__automato._estadoAtual.isFinal():
            self.categorizar()
        # Põe o autômato no estado inicial
        self.__automato.inicializar()
        if self.__log:
            print('<ReiniciarAutomato>')
            print('token reconhecido: {}, categoria {}'.format(self.tokens[-1][0], self.tokens[-1][1]))
            print()
        self.token_atual = ''

    def CursorParaDireita(self):
        try:
            c = next(self.__caracteres)
            self.add_evento(('<ChegadaSimbolo>', c))
            if self.__log:
                print('<CursorParaDireita>')
                print('chegou caractere', c)
                print()
        except Exception as e:
            print(e)

    def ChegadaSimbolo(self, c):
        try:
            self.__automato.atualizar_simbolo(c[1])
            transitou = self.__automato.fazer_transicao()
        except Exception as e:
            print(e)
            transitou = False

        if transitou:
            self.token_atual += c[0]
            if self.__automato.saida_gerada is not None:
                self.add_evento(('<ExecutarTransducao>', c))
            self.add_evento(('<CursorParaDireita>', ))
        else:
            self.add_evento(('<ReiniciarAutomato>', ))
            self.add_evento(('<ChegadaSimbolo>', c))

        if self.__log:
            print('<ChegadaSimbolo>')
            print('estado atual: {t[0]}\nsimbolo atual: {t[1]}'.format(t=self.__automato.mConfiguracao()))
            print('saida gerada =', self.__automato.saida_gerada)
            print()

    def ExecutarTransducao(self, c):
        rotina = self.__automato.saida_gerada
        if rotina == 'aspas':
            self.aspas()
        elif rotina == 'limpa':
            self.limpa()

        if self.__log:
            print('<ExecutarTransducao>')
            print('rotina executada:', rotina)
            print()

    def aspas(self):
        self.token_atual += '"'

    def limpa(self):
        self.token_atual = self.token_atual[:-1]
