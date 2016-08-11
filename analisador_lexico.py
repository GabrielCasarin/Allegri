# Copyright (c) 2016 Gabriel Casarin da Silva All Rights Reserved.


from comum import Simulador
import math


class extrai_texto_fonte(Simulador):

    def trata_evento(self, evento):
        if evento == '<LeituraLinha>':
            self.LeituraLinha()
        if evento == '<FimArquivo>':
            self.FimArquivo()

    def LeituraLinha(self):
        linha = self.arquivo_fonte.readline()
        if linha != '':
            self.linhas_indexadas.append((self.cont_linhas, linha[:-1]))
            self.cont_linhas += 1
            self.add_evento('<LeituraLinha>')
        else:
            self.add_evento('<FimArquivo>')

    def FimArquivo(self):
        print('chegou ao fimo do arquivo fonte "%s"'%self.arquivo_fonte.name)
        self.arquivo_fonte.close()
        num_linhas = math.ceil(math.log10(len(self.linhas_indexadas)))
        with open('linhas_indexadas.txt', 'w') as arq_out:
            for el in self.linhas_indexadas:
                arq_out.write("{0[0]:{1}} {0[1]}\n".format(el, num_linhas))

    def __call__(self, nome_arquivo_fonte, log_extrai_texto_fonte=False):
        if log_extrai_texto_fonte:
            print('entrei na sub-rotina de extração de texto fonte...')

        try:
            self.cont_linhas = 1
            self.linhas_indexadas = []
            self.arquivo_fonte = open(nome_arquivo_fonte)
            self.add_evento('<LeituraLinha>')
            self.run()

        except Exception as e:
            print(e)


        if log_extrai_texto_fonte:
            print('sai na sub-rotina de extração de texto fonte.')

def analise_lexica(log_analise_lexica=False):
    if log_analise_lexica:
        print('entrei na sub-rotina de análise léxica...')



    if log_analise_lexica:
        print('sai na sub-rotina de análise léxica.')

def analise_sintatica(log_analise_sintatica=False):
    if log_analise_sintatica:
        print('entrei na sub-rotina de análise sintática...')



    if log_analise_sintatica:
        print('sai na sub-rotina de análise sintática.')
