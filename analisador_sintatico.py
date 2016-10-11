# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import SimuladorAutomatoPilhaEstruturado
from tabela_simbolos import TabelaSimbolos


class analise_sintatica(SimuladorAutomatoPilhaEstruturado):
    def __init__(self, automato, analisador_lexico, log=False):
        super(analise_sintatica, self).__init__(automato, log)
        self.__analisador_lexico = analisador_lexico
        # self.__tabela_simbolos = TabelaSimbolos()

    def __call__(self):
        if self.__log:
            print('entrei na sub-rotina de análise sintática...')

        if self.__log:
            print('saí da sub-rotina de análise sintática.')
