# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import AbstractSimulador


class SimuladorAutomatoPilhaEstruturado(AbstractSimulador):
    def __init__(self, automato, log=False):
        super(SimuladorAutomatoPilhaEstruturado, self).__init__()
        self.ap = automato
        self._log = log

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
        elif evento[0] == '<FimEntrada>':
            self.FimEntrada()
        elif evento[0] == '<Erro>':
            self.Erro()

    def PartidaInicial(self):
        self.ap.inicializar()
        self.add_evento(('<CursorParaDireita>', ))
        if self._log:
            print('<PartidaInicial>')
            print('Sub-maquina atual:', self.ap.sub_maquina_atual.nome)
            print()

    def CursorParaDireita(self):
        try:
            tok = next(self._tokens)
            self.add_evento(('<ChegadaSimbolo>', tok))
            if self._log:
                print('<CursorParaDireita>: lido o token', tok)
                print()
        except Exception as e:
            self.add_evento(('<FimEntrada>',))
            if self._log:
                print("<CursorParaDireita>: terminaram-se os tokens")
                print()
            if self.ap.tem_retorno_a_realizar():
                self.add_evento(('<CursorParaDireita>', ), no_fim=True)
                self.add_evento(('<RetornoSubmaquina>', ), no_fim=True)

    def ChamadaSubmaquina(self):
        self.ap.chama()
        if self.ap.saida_gerada is not None:
            self.add_evento(('<ExecutarTransducao>', None), no_fim=True)
        if self._log:
            print('<ChamadaSubmaquina>')
            print('Sub-maquina atual:', self.ap.sub_maquina_atual.nome)
            print()

    def RetornoSubmaquina(self):
        self.ap.retorna()
        if self.ap.saida_gerada is not None:
            self.add_evento(('<ExecutarTransducao>', None), no_fim=True)
        if self._log:
            print('<RetornoSubmaquina>')
            print('Sub-maquina atual:', self.ap.sub_maquina_atual.nome)
            print('Estado atual:', self.ap.sub_maquina_atual.mConfiguracao()[0])
            print()

    def ChegadaSimbolo(self, simbolo):
        try:
            self.ap.atualizar_simbolo(simbolo[1])
            transitou = self.ap.fazer_transicao()
        except Exception as e:
            transitou = False

        if not transitou:
            estado_atual, _ = self.ap.mConfiguracao()
            # tentar fazer chamda de sub-maquina
            if self.ap.sub_maquina_atual.tem_transicao_para_submaquina():
                self.add_evento(('<ChegadaSimbolo>', simbolo), no_fim=True)
                self.add_evento(('<ChamadaSubmaquina>', ), no_fim=True)
            # senao, tenta voltar a uma suposta maquina anterior
            elif estado_atual.final and self.ap.tem_retorno_a_realizar():
                self.add_evento(('<ChegadaSimbolo>', simbolo), no_fim=True)
                self.add_evento(('<RetornoSubmaquina>', ), no_fim=True)
            # se nenhuma das duas opcoes deu ceerto, entao emite um sinal de erro
            else:
                self.add_evento(('<Erro>', ), no_fim=True)
        else:
            self.add_evento(('<CursorParaDireita>', ), no_fim=True)
            if self.ap.saida_gerada is not None:
                self.add_evento(('<ExecutarTransducao>', simbolo[0]), no_fim=True)

        if self._log:
            print('<ChegadaSimbolo>')
            print('simbolo chegado:', simbolo[0])
            print('estado atual: {t[0]}\nsimbolo atual: {t[1]}'.format(t=self.ap.mConfiguracao()))
            print()

    def ExecutarTransducao(self, token):
        r = self.ap.saida_gerada

        if self._log:
            print('<ExecutarTransducao>')
            print('saida gerada:', r)
            print()

    def FimEntrada(self):
        estado_atual, _ = self.ap.mConfiguracao()
        if self._log:
            print('<FimEntrada>')
            if not self.ap.tem_retorno_a_realizar() and estado_atual.final:
                print('resultado: CADEIA ACEITA')
            else:
                print('resultado: CADEIA REJEITADA')
            print()

    def Erro(self):
        if self._log:
            print('<Erro>')
            print('Sub-máquina atual:', self.ap.sub_maquina_atual.nome)
            print('Estado: {0[0]}\nSimbolo: {0[1]}'.format(self.ap.mConfiguracao()))
            print('resultado: CADEIA REJEITADA')
            print()
