# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import itertools
from comum.simulador import SimuladorAutomatoPilhaEstruturado
from comum.automatos import AutomatoAbstrato, AutomatoPilhaEstruturado


def gera_nome(nb_estado):
    return 'q' + str(nb_estado)


class MetaReconhecedor(SimuladorAutomatoPilhaEstruturado):
    def __init__(self, automato, classificador_lexico, log=True):
        super(MetaReconhecedor, self).__init__(automato, log)
        self.__classificador_lexico = classificador_lexico

    def __call__(self, arquivo_fonte):
        # conjunto de submáquinas geradas pelo meta-reconhecedor
        self.submaquinas = {}
        self.submaquina_atual = None

        # chama o analisador léxico
        self.__classificador_lexico(arquivo_fonte)
        self.add_evento(('<PartidaInicial>', ))
        self.run()

    def PartidaInicial(self):
        self._tokens = iter(self.__classificador_lexico.tokens)
        self.eh_ape = False
        super(MetaReconhecedor, self).PartidaInicial()


    def ExecutarTransducao(self, token):
        rotina = self.ap.saida_gerada

        if rotina == 'criar_submaquina':
            self.criar_submaquina(token)
        elif rotina == 'inicio_regra':
            self.igual()
        elif rotina == 'fim_regra':
            self.ponto_final()
        elif rotina == '(':
            self.lparen()
        elif rotina == ')':
            self.rparen()
        elif rotina == '[':
            self.lcolchete()
        elif rotina == ']':
            self.rcolchete()
        elif rotina == '{':
            self.lchave()
        elif rotina == '}':
            self.rchave()
        elif rotina == '|':
            self.barra_vertical()

        elif rotina == 'terminal':
            self.terminal(token)

        elif rotina == 'chamada':
            self.chamada(token)

        if self._log:
            print('<ExecutarTransducao>')
            print('rotina executada:', rotina)
            print()

    # ROTINAS SEMÂNTICAS
    def criar_submaquina(self, nome):
        self.submaquina_atual = nome
        # por que criar uma máquina nova, pressupondo que ela já possa existir?
        # simples: ela pode existir apenas por causa de uma referência anterior feita por outra
        if self.submaquina_atual not in self.submaquinas:
            self.submaquinas[self.submaquina_atual] = AutomatoAbstrato(deterministico=False)
        # pilha que determina o escopo em que está o pé da análise
        self.pilha = []
        # conjunto de transições obtido pela análise do conjunto de regras da gramática
        self.transicoes = []
        self.contador = itertools.count()
        # estado inicial é o 0
        self.estado = next(self.contador)
        # insere o estado final 1
        self.valor_atual = next(self.contador)
        self.transicoes.append((self.valor_atual, '', 'pop()'))

        self.submaquinas[self.submaquina_atual].add_estado(gera_nome(self.estado))
        self.submaquinas[self.submaquina_atual].add_estado(gera_nome(self.valor_atual), True)

    def igual(self):
        # Apenas atualiza o escopo
        self.pilha.append((self.estado, self.valor_atual))
        self.valor_atual = next(self.contador)

    def terminal(self, valor_do_terminal):
        estado_anterior = self.estado
        self.estado = self.valor_atual
        self.valor_atual = next(self.contador)
        self.transicoes.append((estado_anterior, valor_do_terminal, self.estado))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(estado_anterior), com=valor_do_terminal, para=gera_nome(self.estado))

    def chamada(self, nome_da_submaq):
        # if nome_da_submaq not in self.submaquinas:
        #     self.submaquinas[nome_da_submaq] = AutomatoAbstrato(deterministico=False)

        estado_anterior = self.estado
        self.estado = self.valor_atual
        self.valor_atual = next(self.contador)
        self.transicoes.append((estado_anterior, nome_da_submaq, self.estado))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(estado_anterior), com=nome_da_submaq, para=gera_nome(self.estado))
        self.submaquinas[self.submaquina_atual][gera_nome(estado_anterior)].submaquinas_chamadas.add(nome_da_submaq)
        self.eh_ape = True

    def lparen(self):
        self.pilha.append((self.estado, self.valor_atual))
        self.valor_atual = next(self.contador)

    def rparen(self):
        estadoAtual, proxEstado = self.pilha.pop()
        self.transicoes.append((self.estado, '', proxEstado))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(self.estado), com='', para=gera_nome(proxEstado))

        self.estado = proxEstado

    def lcolchete(self):
        self.pilha.append((self.estado, self.valor_atual))
        self.transicoes.append((self.estado, '', self.valor_atual))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(self.estado), com='', para=gera_nome(self.valor_atual))

        self.valor_atual = next(self.contador)

    def rcolchete(self):
        estadoAtual, proxEstado = self.pilha.pop()
        self.transicoes.append((self.estado, '', proxEstado))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(self.estado), com='', para=gera_nome(proxEstado))

        self.estado = proxEstado

    def lchave(self):
        self.transicoes.append((self.estado, '', self.valor_atual))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(self.estado), com='', para=gera_nome(self.valor_atual))

        self.estado = self.valor_atual
        self.pilha.append((self.estado, self.estado))
        self.valor_atual = next(self.contador)

    def rchave(self):
        estadoAtual, proxEstado = self.pilha.pop()
        self.transicoes.append((self.estado, '', estadoAtual))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(self.estado), com='', para=gera_nome(estadoAtual))

        self.estado = estadoAtual

    def barra_vertical(self):
        estadoAtual, proxEstado = self.pilha[-1]
        self.transicoes.append((self.estado, '', proxEstado))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(self.estado), com='', para=gera_nome(proxEstado))

        self.estado = estadoAtual

    def ponto_final(self):
        estadoAtual, proxEstado = self.pilha[-1]
        self.transicoes.append((self.estado, '', proxEstado))

        self.submaquinas[self.submaquina_atual].add_transicao(de='q'+str(self.estado), com='', para='q'+str(proxEstado))
