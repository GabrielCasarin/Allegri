# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import SimuladorAutomatoPilhaEstruturado


class analise_sintatica(SimuladorAutomatoPilhaEstruturado):
    def __init__(self, automato, analisador_lexico, gerador_codigo, log=False):
        super(analise_sintatica, self).__init__(automato, log)
        self.__analisador_lexico = analisador_lexico
        self.__gerador_codigo = gerador_codigo

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
            if self._log:
                print("Terminaram-se os tokens")

    def ExecutarTransducao(self, token):
        rotina = self.ap.saida_gerada
        self.__gerador_codigo(rotina, token)

        if self._log:
            print('<ExecutarTransducao>')
            print('rotina executada:', rotina)
            print()

    def __call__(self, arquivo_fonte):
        if self._log:
            print('entrei na sub-rotina de análise sintática...')

        self.__analisador_lexico(arquivo_fonte)
        self.add_evento(('<PartidaInicial>', ))
        self.run()

        if self._log:
            print('saí da sub-rotina de análise sintática.')
