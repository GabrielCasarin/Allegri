# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import SimuladorAutomatoPilhaEstruturado
from tabela_simbolos import TabelaSimbolos


class analise_sintatica(SimuladorAutomatoPilhaEstruturado):
    def __init__(self, automato, analisador_lexico, log=False):
        super(analise_sintatica, self).__init__(automato, log)
        self.__analisador_lexico = analisador_lexico
        # self.__tabela_simbolos = TabelaSimbolos()

    def PartidaInicial(self):
        self.__tokens = iter(self.__analisador_lexico.tokens)
        super(analise_sintatica, self).PartidaInicial()
        self.add_evento(('<CursorParaDireita>', ))

    def CursorParaDireita(self):
        try:
            tok = next(self.__tokens)
            self.add_evento(('<ChegadaSimbolo>', tok))
            if self._log:
                print('<CursorParaDireita>')
                print('chegou token', tok)
                print()
        except Exception as e:
            print(e)

    def __call__(self, arquivo_fonte):
        if self._log:
            print('entrei na sub-rotina de análise sintática...')

        self.__analisador_lexico(arquivo_fonte)
        self.add_evento(('<PartidaInicial>', ))
        self.run()

        if self._log:
            print('saí da sub-rotina de análise sintática.')
