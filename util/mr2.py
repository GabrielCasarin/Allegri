import itertools
from comum import Simulador, AutomatoPilhaEstruturado


class MetaReconhecedor(Simulador):
    def __init__(self):
        super(MetaReconhecedor, self).__init__()

        # pilha que determina o escopo em que está o pé da análise
        self.pilha = []

        # conjunto de transições obtidas pela análise do conjunto de regras da gramática
        self.transicoes = []

        self.contador = itertools.count()
        self.valor_atual = next(self.contador)
        self.estado = self.valor_atual

        # Automato de Pilha que direciona o meta-reconhecimento
        self.ap = AutomatoPilhaEstruturado(nome='wirth', sub_maquinas=['grammar', 'exp'])
        self.ap['grammar'].add_transicao('q0', 'NT', 'q2')
        self.ap['grammar'].add_transicao('q2', '=',  'q3')
        self.ap['grammar'].add_transicao('q4', '.',  'q5')
        self.ap['grammar'].add_transicao('q5', 'NT', 'q2')
        self.ap['grammar']['q3'][''] = (self.ap['exp'], self.ap['grammar']['q4'])
        self.ap['grammar'].set_inicial('q0')
        self.ap['grammar']['q5'].setFinal()

        self.ap['exp'].add_transicao('q0', '(', 'q5')
        self.ap['exp'].add_transicao('q0', '[', 'q8')
        self.ap['exp'].add_transicao('q0', '{', 'q11')
        self.ap['exp'].add_transicao('q1', '(', 'q5')
        self.ap['exp'].add_transicao('q1', '[', 'q8')
        self.ap['exp'].add_transicao('q1', '{', 'q11')
        self.ap['exp'].add_transicao('q6', ')', 'q1')
        self.ap['exp'].add_transicao('q6', ']', 'q1')
        self.ap['exp'].add_transicao('q6', '}', 'q1')
        self.ap['exp'].add_transicao('q0', 'NT', 'q1')
        self.ap['exp'].add_transicao('q0', 'TERM', 'q1')
        self.ap['exp'].add_transicao('q1', 'NT', 'q1')
        self.ap['exp'].add_transicao('q1', 'TERM', 'q1')
        self.ap['exp'].add_transicao('q1', '|', 'q0')

        self.ap['exp']['q5'][''] = (self.ap['exp'], self.ap['exp']['q6'])
        self.ap['exp']['q8'][''] = (self.ap['exp'], self.ap['exp']['q9'])
        self.ap['exp']['q11'][''] = (self.ap['exp'], self.ap['exp']['q12'])
        self.ap['exp'].set_inicial('q0')
        self.ap['exp']['q1'].setFinal()

        self.ap.set_submaquina_inicial('grammar')
        self.ap.inicializar()

        self.ap['grammar'].add_saida(de='q0', com='NT', saida='regra')
        self.ap['grammar'].add_saida(de='q5', com='NT', saida='regra')
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
        self.ap['exp'].add_saida(de='q1', com='|', saida='|')

        self.ap.gerar_alfabeto()

    def trata_evento(self, evento):
        # noAtual = self._listaEventos.raiz
        # while noAtual is not None:
        #     print(noAtual.conteudo, ' ', end='')
        #     noAtual = noAtual.proximo

        if evento[0] == '<PartidaInicial>':
            self.PartidaInicial()
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
        print('<PartidaInicial>')
        print('Sub-maquina atual:', self.ap.mConfiguracao()[0].nome)
        print()

    def ChegadaSimbolo(self, simbolo):
        try:
            self.ap.atualizar_simbolo(simbolo[1])
            saida = self.ap.mConfiguracao()[0].traduzir()
            transitou = self.ap.fazer_transicao()
        except Exception as e:
            print(e)
            transitou = False

        if not transitou:
            _, estado_atual, _ = self.ap.mConfiguracao()
            try:
                if estado_atual[''] is not None:
                    print('estado_atual[\'\'] =', estado_atual[''])
                    self.add_evento(('<ChegadaSimbolo>', simbolo), True)
                    self.add_evento(('<ChamadaSubmaquina>', ), True)
            except Exception as e:
                if estado_atual.isFinal():
                    self.add_evento(('<ChegadaSimbolo>', simbolo), True)
                    self.add_evento(('<RetornoSubmaquina>', ), True)
        else:
            if saida == 'regra':
                self.regra()
            elif saida == '.':
                self.ponto_final()
            elif saida == '=':
                self.igual()
            elif saida == '(':
                self.lparen()
            elif saida == ')':
                self.rparen()
            elif saida == '[':
                self.lcolchete()
            elif saida == ']':
                self.rcolchete()
            elif saida == '{':
                self.lchave()
            elif saida == '}':
                self.rchave()
            elif saida == '|':
                self.barra_vertical()
            elif saida == 'terminal':
                self.terminal(simbolo[0])
        print('<ChegadaSimbolo>')
        print('estado atual: {t[1]}\nsimbolo atual: {t[2]}'.format(t=self.ap.mConfiguracao()))
        print()

    def ChamadaSubmaquina(self):
        self.ap.chama()
        print('<ChamadaSubmaquina>')
        print('Sub-maquina atual:', self.ap.mConfiguracao()[0].nome)
        print()

    def RetornoSubmaquina(self):
        self.ap.retorna()
        print('<RetornoSubmaquina>')
        print('Sub-maquina atual:', self.ap.mConfiguracao()[0].nome)
        print()

    def ExecutarTransducao(self, rotina):
        pass

        # if evento[0] == 'regra':
        #     self.regra()

        # elif evento[0] == 'sinal':
        #     if evento[1] == '.':
        #         self.ponto_final()
        #     elif evento[1] == '=':
        #         self.igual()
        #     elif evento[1] == '(':
        #         self.lparen()
        #     elif evento[1] == ')':
        #         self.rparen()
        #     elif evento[1] == '[':
        #         self.lcolchete()
        #     elif evento[1] == ']':
        #         self.rcolchete()
        #     elif evento[1] == '{':
        #         self.lchave()
        #     elif evento[1] == '}':
        #         self.rchave()
        #     elif evento[1] == '|':
        #         self.barra_vertical()

        # elif evento[0] == 'terminal':
        #     self.terminal(evento[1])

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
        self.transicoes.append((estadoAtual, '', proxEstado))
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
