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
        elif evento == '<ChegadaSimbolo>':
            self.ChegadaSimbolo()

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
                self.add_evento('<ChegadaSimbolo>')
            self.add_evento('<LeituraLinha>')
        else:
            self.add_evento('<FimArquivo>')

    def FimArquivo(self):
        if self.log_imprimir_linhas:
            print("<FimArquivo>        chegou ao fim do arquivo fonte '{}'".format(self.arquivo_fonte.name))
        self.arquivo_fonte.close()
        #  num_linhas = math.ceil(math.log10(len(self.linhas_indexadas)))

    def ChegadaSimbolo(self):
        num_linha, linha = self.linhas_indexadas[-1]
        char = linha[self.cursor]
        if char != '\n':
            if char in string.digits:
                classificacao = 'digito'
            elif char in string.ascii_letters:
                classificacao = 'letra'
            elif char in string.punctuation:
                classificacao = 'pontuacao'
            elif char in ' \t':
                classificacao = 'espaco'
            self.caracteres_classificados.append((char, classificacao))
            if self.log_imprimir_caracteres:
                print("<ChegadaSimbolo>    {0[0]} (ascii HEX {1:X}) {0[1]}".format(self.caracteres_classificados[-1], ord(self.caracteres_classificados[-1][0])))
        self.cursor += 1

    def __call__(self, nome_arquivo_fonte):
        if self.log_decompoe_texto_fonte:
            print('entrei na sub-rotina de extração de texto fonte...')

        try:
            self.cont_linhas = 1
            self.linhas_indexadas = []
            self.caracteres_classificados = []
            self.arquivo_fonte = open(nome_arquivo_fonte)
            self.add_evento('<LeituraLinha>')
            self.run()

        except Exception as e:
            print(e)

        if self.log_decompoe_texto_fonte:
            print('sai na sub-rotina de extração de texto fonte.')

        if self.imprimir_listagem:
            LOG_DIR = os.path.join(ROOT_DIR, 'log')
            with open(os.path.join(LOG_DIR, 'linhas_indexadas.txt'), 'w') as arq_out:
                for el in self.linhas_indexadas:
                    arq_out.write("{0[0]:{1}} {0[1]}".format(el, num_linhas))
            with open(os.path.join(LOG_DIR, 'caracteres_classificados.txt'), 'w') as arq_out:
                for el in self.caracteres_classificados:
                    arq_out.write("{0[0]} {0[1]}\n".format(el))


class analise_lexica(Simulador):
    def __init__(self, automato, log_analise_lexica=False):
        super(analise_lexica, self).__init__()
        self.automato = automato
        self.automato.inicializar()
        self.log_analise_lexica = log_analise_lexica

    def trata_evento(self, evento):
        if evento == '<ChegadaSimbolo>':
            self.ChegadaSimbolo()

    def ChegadaSimbolo(self):
        self.automato.atualizarSimbolo()
        if self.automato.fazerTransicao():
            pass

    def __call__(self):
        if self.log_analise_lexica:
            print('entrei na sub-rotina de análise léxica...')

        if self.log_analise_lexica:
            print('sai na sub-rotina de análise léxica.')


class analise_sintatica(Simulador):
    def __init__(self, log_analise_sintatica=False):
        super(analise_sintatica, self).__init__()

    def __call__(self):
        if self.log_analise_sintatica:
            print('entrei na sub-rotina de análise sintática...')

        if self.log_analise_sintatica:
            print('sai na sub-rotina de análise sintática.')
