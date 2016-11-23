# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import itertools
from comum import SimuladorAutomatoPilhaEstruturado
from comum.automatos import AbstractAutomato, AutomatoPilhaEstruturado
__all__ = ['MetaReconhecedor']


def gera_nome(nb_estado):
    return 'q' + str(nb_estado)

class MetaReconhecedor(SimuladorAutomatoPilhaEstruturado):
    def __init__(self, classificador_lexico, log=True):
        super(MetaReconhecedor, self).__init__(automato=None, log=log)
        self.__classificador_lexico = classificador_lexico

        # Automato de Pilha que direciona o meta-reconhecimento
        self.ap = AutomatoPilhaEstruturado(nome='wirth', sub_maquinas=['grammar', 'exp'])
        self.ap['grammar'].add_transicao('q0', 'NT', 'q2')
        self.ap['grammar'].add_transicao('q2', '=',  'q3')
        self.ap['grammar'].add_transicao('q4', '.',  'q5')
        self.ap['grammar'].add_transicao('q5', 'NT', 'q2')
        self.ap['grammar'].add_chamada_para_submaquina(de='q3', para=self.ap['exp'].nome, retorno='q4')
        self.ap['grammar'].set_inicial('q0')
        self.ap['grammar']['q5'].final = True

        self.ap['exp'].add_transicao('q0', '(', 'q5')
        self.ap['exp'].add_transicao('q0', '[', 'q8')
        self.ap['exp'].add_transicao('q0', '{', 'q11')
        self.ap['exp'].add_transicao('q1', '(', 'q5')
        self.ap['exp'].add_transicao('q1', '[', 'q8')
        self.ap['exp'].add_transicao('q1', '{', 'q11')
        self.ap['exp'].add_transicao('q6', ')', 'q1')
        self.ap['exp'].add_transicao('q9', ']', 'q1')
        self.ap['exp'].add_transicao('q12', '}', 'q1')
        self.ap['exp'].add_transicao('q0', 'NT', 'q1')
        self.ap['exp'].add_transicao('q0', 'TERM', 'q1')
        self.ap['exp'].add_transicao('q1', 'NT', 'q1')
        self.ap['exp'].add_transicao('q1', 'TERM', 'q1')
        self.ap['exp'].add_transicao('q1', '|', 'q0')

        self.ap['exp'].add_chamada_para_submaquina(de='q5', para=self.ap['exp'].nome, retorno='q6')
        self.ap['exp'].add_chamada_para_submaquina(de='q8', para=self.ap['exp'].nome, retorno='q9')
        self.ap['exp'].add_chamada_para_submaquina(de='q11', para=self.ap['exp'].nome, retorno='q12')
        self.ap['exp'].set_inicial('q0')
        self.ap['exp']['q1'].final = True

        self.ap.set_submaquina_inicial('grammar')
        self.ap.inicializar()

        self.ap['grammar'].add_saida(de='q0', com='NT', saida='criar_submaquina')
        self.ap['grammar'].add_saida(de='q5', com='NT', saida='criar_submaquina')
        self.ap['grammar'].add_saida(de='q2', com='=',  saida='=')
        self.ap['grammar'].add_saida(de='q4', com='.',  saida='.')

        self.ap['exp'].add_saida(de='q0', com='(', saida='(')
        self.ap['exp'].add_saida(de='q0', com='[', saida='[')
        self.ap['exp'].add_saida(de='q0', com='{', saida='{')
        self.ap['exp'].add_saida(de='q1', com='(', saida='(')
        self.ap['exp'].add_saida(de='q1', com='[', saida='[')
        self.ap['exp'].add_saida(de='q1', com='{', saida='{')
        self.ap['exp'].add_saida(de='q6', com=')', saida=')')
        self.ap['exp'].add_saida(de='q9', com=']', saida=']')
        self.ap['exp'].add_saida(de='q12', com='}', saida='}')
        self.ap['exp'].add_saida(de='q0', com='TERM', saida='terminal')
        self.ap['exp'].add_saida(de='q1', com='TERM', saida='terminal')
        self.ap['exp'].add_saida(de='q0', com='NT', saida='chamada')
        self.ap['exp'].add_saida(de='q1', com='NT', saida='chamada')
        self.ap['exp'].add_saida(de='q1', com='|', saida='|')

        self.ap.gerar_alfabeto()

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
        elif rotina == '.':
            self.ponto_final()
        elif rotina == '=':
            self.igual()
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
            self.submaquinas[self.submaquina_atual] = AbstractAutomato(deterministico=False)
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
        #     self.submaquinas[nome_da_submaq] = AbstractAutomato(deterministico=False)

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
