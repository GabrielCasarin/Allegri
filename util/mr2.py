import itertools
from comum import Simulador, AutomatoPilhaEstruturado
from comum.automatos import AbstractAutomato

def gera_nome(nb_estado):
    return 'q' + str(nb_estado)

class MetaReconhecedor(Simulador):
    def __init__(self):
        super(MetaReconhecedor, self).__init__()

        # conjunto de submáquinas geradas pelo meta-reconhecedor
        self.submaquinas = {}
        self.submaquina_atual = None

        # Automato de Pilha que direciona o meta-reconhecimento
        self.ap = AutomatoPilhaEstruturado(nome='wirth', sub_maquinas=['grammar', 'exp'])
        self.ap['grammar'].add_transicao('q0', 'NT', 'q2')
        self.ap['grammar'].add_transicao('q2', '=',  'q3')
        self.ap['grammar'].add_transicao('q4', '.',  'q5')
        self.ap['grammar'].add_transicao('q5', 'NT', 'q2')
        self.ap['grammar'].add_chamada_para_submaquina(de='q3', para=self.ap['exp'], retorno='q4')
        self.ap['grammar'].set_inicial('q0')
        self.ap['grammar']['q5'].setFinal()

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

        self.ap['exp'].add_chamada_para_submaquina(de='q5', para=self.ap['exp'], retorno='q6')
        self.ap['exp'].add_chamada_para_submaquina(de='q8', para=self.ap['exp'], retorno='q9')
        self.ap['exp'].add_chamada_para_submaquina(de='q11', para=self.ap['exp'], retorno='q12')
        self.ap['exp'].set_inicial('q0')
        self.ap['exp']['q1'].setFinal()

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

    # ROTINAS DE EXECUÇÃO DO AUTÔMATO DE PILHA
    def trata_evento(self, evento):
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
            transitou = self.ap.fazer_transicao()
        except Exception as e:
            print(e)
            transitou = False

        if not transitou:
            maquina_atual, estado_atual, _ = self.ap.mConfiguracao()
            if maquina_atual.tem_transicao_para_submaquina():
                self.add_evento(('<ChegadaSimbolo>', simbolo), True)
                self.add_evento(('<ChamadaSubmaquina>', ), True)
            elif estado_atual.isFinal():
                self.add_evento(('<ChegadaSimbolo>', simbolo), True)
                self.add_evento(('<RetornoSubmaquina>', ), True)
        else:
            self.add_evento(('<ExecutarTransducao>', simbolo[0]), True)

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

    def ExecutarTransducao(self, token):
        rotina = self.ap.mConfiguracao()[0].saida_gerada

        if rotina == 'criar_submaquina':
            self.criar_submaquina(token)
        # elif rotina == 'sinal':
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
        if nome_da_submaq not in self.submaquinas:
            self.submaquinas[nome_da_submaq] = AbstractAutomato(deterministico=False)

        estado_anterior = self.estado
        self.estado = self.valor_atual
        self.valor_atual = next(self.contador)
        self.transicoes.append((estado_anterior, nome_da_submaq, self.estado))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(estado_anterior), com=nome_da_submaq, para=gera_nome(self.estado))

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
        self.transicoes.append((estadoAtual, '', proxEstado))

        self.submaquinas[self.submaquina_atual].add_transicao(de=gera_nome(estadoAtual), com='', para=gera_nome(proxEstado))

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
