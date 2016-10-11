# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import AbstractSimulador


class SimuladorAutomatoPilhaEstruturado(AbstractSimulador):
    """docstring for SimuladorAutomatoPilhaEstruturado"""
    def __init__(self, automato, log=False):
        super(SimuladorAutomatoPilhaEstruturado, self).__init__()
        self.ap = automato
        self.__log = log


    # ROTINAS DE EXECUÇÃO DO AUTÔMATO DE PILHA
    def trata_evento(self, evento):
        if evento[0] == '<PartidaInicial>':
            self.PartidaInicial()
        elif evento[0] == '<CursorParaDireita>':
            self.CursorParaDireita()
        elif evento[0] == '<ChegadaSimbolo>':
            self.ChegadaSimbolo(evento[1])
        elif evento[0] == '<ChamadaSubmaquina>':
            self.ChamadaSubmaquina()
        elif evento[0] == '<RetornoSubmaquina>':
            self.RetornoSubmaquina()
        elif evento[0] == '<ExecutarTransducao>':
            self.ExecutarTransducao(evento[1])


    def PartidaInicial(self):
        self.ap.inicializar()
        if self.__log:
            print('<PartidaInicial>')
            print('Sub-maquina atual:', self.ap.mConfiguracao()[0].nome)
            print()

    def CursorParaDireita(self):
        pass

    def ChamadaSubmaquina(self):
        self.ap.chama()
        if self.__log:
            print('<ChamadaSubmaquina>')
            print('Sub-maquina atual:', self.ap.mConfiguracao()[0].nome)
            print()

    def RetornoSubmaquina(self):
        self.ap.retorna()
        if self.__log:
            print('<RetornoSubmaquina>')
            print('Sub-maquina atual:', self.ap.mConfiguracao()[0].nome)
            print()

    def ChegadaSimbolo(self, simbolo):
        try:
            self.ap.atualizar_simbolo(simbolo[1])
            transitou = self.ap.fazer_transicao()
        except Exception as e:
            transitou = False

        if not transitou:
            maquina_atual, estado_atual, _ = self.ap.mConfiguracao()
            if maquina_atual.tem_transicao_para_submaquina():
                self.add_evento(('<ChegadaSimbolo>', simbolo), True)
                self.add_evento(('<ChamadaSubmaquina>', ), True)
            elif estado_atual.final:
                self.add_evento(('<ChegadaSimbolo>', simbolo), True)
                self.add_evento(('<RetornoSubmaquina>', ), True)
        else:
            self.add_evento(('<ExecutarTransducao>', simbolo[0]), True)

        if self.__log:
            print('<ChegadaSimbolo>')
            print('simbolo chegado:', simbolo[0])
            print('estado atual: {t[0]}\nsimbolo atual: {t[1]}'.format(t=self.ap.mConfiguracao()))
            print()



    def ExecutarTransducao(self, token):
        rotina = self.ap.saida_gerada

        if self.__log:
            print('<ExecutarTransducao>')
            print('rotina executada:', rotina)
            print()