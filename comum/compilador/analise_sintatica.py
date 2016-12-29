# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum.simulador import SimuladorAutomatoPilhaEstruturado


class analisador_sintatico(SimuladorAutomatoPilhaEstruturado):
    def __init__(self, automato, analisador_lexico, gerador_codigo, log=False):
        super(analisador_sintatico, self).__init__(automato, log)
        self.__analisador_lexico = analisador_lexico
        self.__gerador_codigo = gerador_codigo

    def PartidaInicial(self):
        self._tokens = iter(self.__analisador_lexico.tokens)
        super(analisador_sintatico, self).PartidaInicial()

    def ExecutarTransducao(self, token):
        rotina = self.ap.saida_gerada
        self.__gerador_codigo(rotina, token)

        if self._log:
            print('<ExecutarTransducao>: executada rotina', rotina)
            print()

    def __call__(self, arquivo_fonte):
        if self._log:
            print('entrei na sub-rotina de análise sintática...')

        self.__analisador_lexico(arquivo_fonte)
        self.add_evento(('<PartidaInicial>', ))
        self.run()

        if self._log:
            print('saí da sub-rotina de análise sintática.')
