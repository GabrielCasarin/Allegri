# Copyright (c) 2016 Gabriel Casarin da Silva All Rights Reserved.


import os
import math
import string
from comum import Simulador
from definicoes import ROOT_DIR


class decompoe_texto_fonte(Simulador):
    def __init__(self, log_decompoe_texto_fonte=False,
                 log_imprimir_linhas=False, log_imprimir_caracteres=False,
                 imprimir_listagem=False):
        super(decompoe_texto_fonte, self).__init__()
        self.log_decompoe_texto_fonte = log_decompoe_texto_fonte
        self.log_imprimir_linhas = log_imprimir_linhas
        self.log_imprimir_caracteres = log_imprimir_caracteres
        self.imprimir_listagem = imprimir_listagem

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
        # self.caracteres_classificados.append(-1)

    def ChegadaCaractere(self):
        num_linha, linha = self.linhas_indexadas[-1]
        char = linha[self.cursor]
        if char == '\n':
            classificacao = 'enter'
        elif char in string.digits:
            classificacao = 'Algarismo'
        elif char in string.ascii_letters:
            classificacao = 'Letra'
        elif char in string.punctuation:
            classificacao = char
        elif char in ' \t':
            classificacao = 'espaco'
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


class analisador_lexico(Simulador):
    def __init__(self, automato, decompositor, log_analise_lexica=False):
        super(analisador_lexico, self).__init__()
        self.__automato = automato
        self.__decompositor = decompositor
        self.__log = log_analise_lexica

    def trata_evento(self, evento):
        # no = self._listaEventos.raiz
        # while no is not None:
        #     print(no.conteudo, end=' | ')
        #     no = no.proximo
        # print()
        # print()
        #
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
        self.__decompositor('gram_ex.txt')
        self.__caracteres = iter(self.__decompositor.caracteres_classificados)
        self.token_atual = ''
        self.token_tipo = None
        self.tokens = []
        self.add_evento(('<CursorParaDireita>', ))
        if self.__log:
            print('<PartidaInicial>\n')

    def ReiniciarAutomato(self):
        if self.__automato._estadoAtual.isFinal():
            if self.__automato._estadoAtual == 'q2':
                self.token_tipo = self.token_atual
            elif self.__automato._estadoAtual == 'q6':
                self.token_atual = self.token_atual[1:-1]
                self.token_tipo = 'TERM'
            elif self.__automato._estadoAtual == 'q3':
                self.token_tipo = 'NT'
            self.tokens.append((self.token_atual, self.token_tipo))

        self.__automato.inicializar()

        if self.__log:
            print('<ReiniciarAutomato>')
            print('token reconhecido:', self.token_atual)
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
        if rotina == 'E0':
            self.E0()
        # elif rotina == 'constroi_TERM':
        #     self.constroi_TERM(c[0])
        # elif rotina == 'igual':
        #     self.igual(c[0])
        # elif rotina == 'lparen':
        #     self.lparen(c[0])
        # elif rotina == 'rparen':
        #     self.rparen(c[0])
        # elif rotina == 'lchave':
        #     self.lchave(c[0])
        # elif rotina == 'rchave':
        #     self.rchave(c[0])
        # elif rotina == 'lcolchete':
        #     self.lcolchete(c[0])
        # elif rotina == 'rcolchete':
        #     self.rcolchete(c[0])
        # elif rotina == 'ponto_final':
        #     self.ponto_final(c[0])

        if self.__log:
            print('<ExecutarTransducao>')
            print('rotina executada:', rotina)
            print()

    def E0(self):
        self.token_atual = self.token_atual[:-1]

    # def constroi_NT(self, c):
    #     if self.token_atual is None:
    #         self.token_atual = c
    #         self.token_tipo = 'NT'
    #     else:
    #         self.token_atual += c
    #
    # def constroi_TERM(self, c):
    #     if self.token_atual is None:
    #         self.token_atual = c
    #         self.token_tipo = 'TERM'
    #     else:
    #         self.token_atual += c
    #
    # def igual(self, c):
    #     self.token_atual = c
    #     self.token_tipo = 'igual'
    #
    # def pontuacao(self, c):
    #     self.token_atual = c
    #     self.token_tipo = c

    # def token(self):
    #     if self.__log:
    #         print('entrei na sub-rotina de análise léxica...')
    #
    #
    #
    #     if self.__log:
    #         print('saí da sub-rotina de análise léxica.')


class analise_sintatica(Simulador):
    def __init__(self, log_analise_sintatica=False):
        super(analise_sintatica, self).__init__()

    def __call__(self):
        if self.log_analise_sintatica:
            print('entrei na sub-rotina de análise sintática...')

        if self.log_analise_sintatica:
            print('saí da sub-rotina de análise sintática.')
