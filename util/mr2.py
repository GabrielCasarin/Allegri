import itertools
from comum import Simulador, Estado, AutomatoFinito

class MetaReconhecedor(Simulador):
    def __init__(self):
        super(MetaReconhecedor, self).__init__()

        ## pilha que determina o escopo em que está o pé da análise
        self.pilha = []

        ## conjunto de transições obtidas pela análise do conjunto de regras da gramática
        self.transicoes = []

        self.contador = itertools.count()
        self.valor_atual = next(self.contador)
        self.estado = self.valor_atual

    def trata_evento(self, evento):
        if evento[0] == 'regra':
            self.regra()

        elif evento[0] == 'sinal':
            if evento[1] == '.':
                self.ponto_final()
            elif evento[1] == '=':
                self.igual()
            elif evento[1] == '(':
                self.lparen()
            elif evento[1] == ')':
                self.rparen()
            elif evento[1] == '[':
                self.lcolchete()
            elif evento[1] == ']':
                self.rcolchete()
            elif evento[1] == '{':
                self.lchave()
            elif evento[1] == '}':
                self.rchave()
            elif evento[1] == '|':
                self.barra_vertical()

        elif evento[0] == 'terminal':
            self.terminal(evento[1])

    def regra(self):
        self.valor_atual = next(self.contador)
        self.transicoes.append((self.valor_atual, '', 'pop()'))

    def igual(self):
        self.pilha.append((self.estado, self.valor_atual))
        self.valor_atual = next(self.contador)

    def terminal(self, token_value):
        estado_anterior = self.estado
        self.estado = self.valor_atual
        self.valor_atual = next(self.contador)
        self.transicoes.append((estado_anterior, token_value, self.estado))

    def lparen(self):
        self.pilha.append((self.estado, self.valor_atual))
        self.valor_atual = next(self.contador)

    def rparen(self):
        estadoAtual, proxEstado = self.pilha.pop()
        self.transicoes.append((self.estado, '', proxEstado))
        self.estado = proxEstado

    def lcolchete(self):
        self.pilha.append((self.estado, self.valor_atual))
        self.transicoes.append((self.estado, '', self.valor_atual))
        self.valor_atual = next(self.contador)

    def rcolchete(self):
        estadoAtual, proxEstado = self.pilha.pop()
        self.transicoes.append((estado, '', proxEstado))
        self.estado = proxEstado

    def lchave(self):
        self.transicoes.append((self.estado, '', self.valor_atual))
        self.estado = self.valor_atual
        self.pilha.append((self.estado, self.estado))
        self.valor_atual = next(self.contador)

    def rchave(self):
        estadoAtual, proxEstado = self.pilha.pop()
        self.transicoes.append((self.estado, '', estadoAtual))
        self.estado = estadoAtual

    def barra_vertical(self):
        estadoAtual, proxEstado = self.pilha[-1]
        self.transicoes.append((self.estado, '', proxEstado))
        self.estado = estadoAtual

    def ponto_final(self):
        estadoAtual, proxEstado = self.pilha[-1]
        self.transicoes.append((self.estado, '', proxEstado))
