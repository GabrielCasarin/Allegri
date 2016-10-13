# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import AbstractSimulador
import tabela_simbolos as ST


class gerar_codigo_assembly(AbstractSimulador):
    def __init__(self, log=False):
        super(gerar_codigo_assembly, self).__init__()
        self.__tabela_simbolos = ST.TabelaSimbolos()
        self.tipos = {
                "int": ST.TipoBasico("int", 2),
                "char": ST.TipoBasico("char", 1),
                "bool": ST.TipoBasico("bool", 2),
                "void": ST.TipoBasico("void", 0),
        }
        self.pilha_operandos = []
        self.pilha_operadores = []
        self.__log = log

    def __call__(self, rotina, token=None):
        if self.__log:
            print('entrei na sub-rotina de geração de código objeto...')

        if rotina == 'iniciar_expressao_mat':
            self.iniciar_expressao_mat()
        elif rotina == 'recebe_operador_normal':
            self.recebe_operador_normal(token)
        elif rotina == 'mais_ou_menos':
            self.mais_ou_menos(token)
        elif rotina == 'vezes_ou_dividir':
            self.vezes_ou_dividir(token)
        # elif rotina == 'vezes_ou_dividir2':
        #     self.vezes_ou_dividir2(token)
        elif rotina == 'recebe_operando_var':
            self.recebe_operando_var(token)
        elif rotina == 'finalizar_expressao':
            self.finalizar_expressao()
        elif rotina == 'abre_parenteses':
            self.abre_parenteses()
        elif rotina == 'fecha_parenteses':
            self.fecha_parenteses()
        # elif rotina == 'fecha_parenteses2':
        #     self.fecha_parenteses2()

        if self.__log:
            print('saí da sub-rotina de geração de código objeto...')

    def declaracao_funcao(self, nome_func, tipo_return):
        _, simb = self.__tabela_simbolos.procurar(nome_func)
        if simb is None:
            func_simb = ST.Simbolo(nome_func, "func", self.tipos[tipo_return])
            self.__tabela_simbolos.inserir_simbolo(func_simb)
            print("{}\t$ /0001".format(nome_func.upper()))
            self.__tabela_simbolos.novo_escopo()

    def encerra_funcao(self, nome_func):
        self.__tabela_simbolos.remover_escopo()
        escopo, simb = self.__tabela_simbolos.procurar(nome_func)
        if simb is not None:
            print("RET_{0}\tRS\t{0}".format(escopo[simb].nome.upper()))

    def inicia_declaracao_variavel(self):
        self.__lista_variaveis_a_declarar = []

    def nova_var(self, nome_var):
        self.__lista_variaveis_a_declarar.append(nome_var)

    def fecha_declaracao_variavel(self, tipo_var):
        for nome_var in self.__lista_variaveis_a_declarar:
            _, simb = self.__tabela_simbolos.procurar(nome_var)
            if simb is None:
                var_simb = ST.Simbolo(nome_var, "var", self.tipos[tipo_var])

    # EXPRESSÕES MATEMÁTICAS
    def iniciar_expressao_mat(self):
        self.pilha_operadores.append('LD')

    def recebe_operador_normal(self, operador):
        print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
        self.pilha_operadores.append(operador)

    def mais_ou_menos(self, operador):
        # termina a operacap de * ou /
        print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
        if self.pilha_operadores:
            # guarda em X
            print('MM X')
            print('SC POP')
            # entrega tudo bonitinho no acc
            print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
        self.pilha_operadores.append(operador)

    def vezes_ou_dividir(self, operador):
        self.pilha_operadores.append(operador)
        print('SC PUSH')
        self.pilha_operadores.append('LD')
        print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
        self.pilha_operandos.append('X')

    def recebe_operando_var(self, operando):
        self.pilha_operandos.append(operando)

    def finalizar_expressao(self):
        while len(self.pilha_operandos) > 1:
            # termina a operacap de * ou /
            print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
            # guarda em X
            print('MM X')
            print('SC POP')
            # entrega tudo bonitinho no acc
        print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))

    def abre_parenteses(self):
        self.pilha_operandos.append('X')
        self.pilha_operadores.append('(')
        print('SC PUSH')
        self.pilha_operadores.append('LD')

    def fecha_parenteses(self):
        # finaliza a expressão interna
        while self.pilha_operadores[-1] != '(':
            print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
            # restaura o estado anterior
            print('MM X')
            print('SC POP')
        self.pilha_operadores.pop() # retira o '('

    # def declaracao_parametro(self, nome_par, tipo_par):
    #     _, simb = self.__tabela_simbolos.procurar(nome_par)
    #     if simb is None:
    #         var_simb = ST.Simbolo(nome_par, "par", self.tipos[tipo_par])
