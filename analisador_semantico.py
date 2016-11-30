# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.

import itertools
import string
from comum import AbstractSimulador
import tabela_simbolos as ST


class gerar_codigo_assembly(AbstractSimulador):
    def __init__(self, log=False):
        super(gerar_codigo_assembly, self).__init__()
        self.tabela_simbolos = ST.TabelaSimbolos()
        self.tipos = {
                "int": ST.TipoBasico("int", 2),
                "char": ST.TipoBasico("char", 2),
                "bool": ST.TipoBasico("bool", 2),
                "int pointer": ST.TipoBasico("int pointer", 2),
                "bool pointer": ST.TipoBasico("bool pointer", 2),
                "void": ST.TipoBasico("void", 0),
        }
        self.pilha_operandos = []
        self.pilha_operadores = []
        self.__func_atual = None


        # código necessário a todos os programas compilados
        self.preambulo = [
            "PUSH    <",
            "POP     <",
            "SP      <",
            "TRUE    <",
            "FALSE   <",
            "AND     <",
            "OR      <",
            "NOT     <",
            "GET_FROM_FRAME  <",
            "SET_TO_FRAME    <",
            "GET_FROM_VECT   <",
            "SET_TO_VECT     <",
            "PUSHDOWN_SUM    <",
            "PUSHDOWN_DIF    <",
            "PUSHDOWN_MUL    <",
            "PUSHDOWN_DIV    <",
            "GET_LENGTH      <",
            "IGUAL           <",
            "DIFERENTE       <",
            "MAIOR           <",
            "MAIOR_OU_IGUAL  <",
            "MENOR           <",
            "MENOR_OU_IGUAL  <",
            "BASE      <",
            "K_0000    <",
            "K_0001    <",
            "K_0002    <",
            "K_FFFF    <",
            "WORD_TAM  <",
            "DIM_1     <",
            "DIM_2     <",
            "INIT_HEAP      <",
            "NEW_ARRAY      <",
            "NEW_MATRIX     <",
            "&     /0000",
            "SC    INIT_HEAP",
            "LD    SP",
            "+     WORD_TAM",
            "MM    FP",
            "SC    main",
            "FIM   HM FIM",
        ]

        # insere na tabela de símbolos todos os imports
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("PUSH", "func", self.tipos["void"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("POP", "func", self.tipos["int"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("TRUE", "const", self.tipos["bool"], 1)
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("FALSE", "const", self.tipos["bool"], 0)
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("AND", "func", self.tipos["bool"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("NOT", "func", self.tipos["bool"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("OR", "func", self.tipos["bool"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("K_0000", "const", self.tipos["int"], 0)
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("K_0001", "const", self.tipos["int"], 1)
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("K_0002", "const", self.tipos["int"], 2)
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("K_FFFF", "const", self.tipos["int"], -1)
        )

        # armazena o código referente a declarações de constantes 
        self.constantes = []
        # armazena todo o código gerado
        self.codigo = []

        self.__identificador_atual = []
        self.__contador_parametros_atribuidos = []
        self.inverte = []
        self.pilha_tipos_resultados_parciais = []
        self.pilha_operadores_booleanos = []
        self.__dummy_labels_generator = itertools.cycle(string.ascii_uppercase)
        self.labels_a_resolver = []
        self.tem_simbolos_a_resolver = []
        self.__identificadores_do_len = []
        
        self.__log = log

    def __call__(self, rotina, token=None):
        if self.__log:
            print('entrei na sub-rotina de geração de código objeto...')

        # EXPRESSÕES MATEMÁTICAS
        if   rotina == 'iniciar_expressao_mat': self.iniciar_expressao_mat()
        elif rotina == 'mais_ou_menos': self.mais_ou_menos(token)
        elif rotina == 'vezes_ou_dividir': self.vezes_ou_dividir(token)
        elif rotina == 'recebe_operando_id': self.recebe_operando_id(token)
        elif rotina == 'recebe_operando_num': self.recebe_operando_num(token)
        elif rotina == 'finalizar_expressao_mat': self.finalizar_expressao_mat()
        elif rotina == 'abre_parenteses': self.abre_parenteses()
        elif rotina == 'fecha_parenteses': self.fecha_parenteses()
        elif rotina == 'sai_termo': self.sai_termo()
        elif rotina == 'inverte_termo': self.inverte_termo()
        # FIM EXPRESSÕES MATEMÁTICAS

        # EXPRESSÕES BOOLEANAS
        elif rotina == 'recebe_comparador': self.recebe_comparador(token)
        elif rotina == 'and_op': self.and_op()
        elif rotina == 'or_op': self.or_op()
        # FIM DE EXPRESSÕES BOOLEANAS

        # DECLARAÇÃO DE FUNÇÕES
        elif rotina == 'declaracao_funcao': self.declaracao_funcao(token)
        elif rotina == 'definir_tipo_funcao': self.definir_tipo_funcao(token)
        elif rotina == 'inicia_declaracao_parametros': self.inicia_declaracao_parametros()
        elif rotina == 'novo_par': self.novo_par(token)
        elif rotina == 'parametro_eh_ponteiro': self.parametro_eh_ponteiro()
        elif rotina == 'fecha_declaracao_parametro': self.fecha_declaracao_parametro(token)        
        elif rotina == 'encerra_funcao': self.encerra_funcao()
        elif rotina == 'calcular_end_parametros': self.calcular_end_parametros()
        # FIM DECLARAÇÃO DE FUNÇÕES

        # DECLARAÇÃO DE VARIÁVEIS
        elif rotina == 'inicia_declaracao_variavel': self.inicia_declaracao_variavel()
        elif rotina == 'add_tipo': self.add_tipo(token)
        elif rotina == 'add_dim': self.add_dim(token)
        elif rotina == 'nova_var': self.nova_var(token)
        elif rotina == 'fecha_declaracao_variavel': self.fecha_declaracao_variavel(token)
        # FIM DECLARAÇÃO DE VARIÁVEIS

        # CHAMADA DE FUNÇÃO
        elif rotina == 'iniciar_frame': self.iniciar_frame()
        elif rotina == 'chamar_funcao': self.chamar_funcao()
        elif rotina == 'guarda_parametro_e_chamar_funcao': self.guarda_parametro_e_chamar_funcao()
        elif rotina == 'guarda_parametro': self.guarda_parametro()
        elif rotina == 'separa_argumentos': self.separa_argumentos()
        # FIM CHAMADA DE FUNÇÃO

        # COMANDO SIMPLES
        elif rotina == 'inicia_comando_simples': self.inicia_comando_simples(token)
        elif rotina == 'comando_atribuicao': self.comando_atribuicao()
        elif rotina == 'comando_retorno': self.comando_retorno()
        # FIM COMANDO SIMPLES

        # COMANDO IF
        elif rotina == 'constroi_if': self.constroi_if()
        elif rotina == 'constroi_elif': self.constroi_elif()
        elif rotina == 'constroi_else': self.constroi_else()
        elif rotina == 'fecha_if': self.fecha_if()
        elif rotina == 'fecha_else': self.fecha_else()
        # FIM COMANDO IF

        # COMANDO WHILE
        elif rotina == 'constroi_while': self.constroi_while()
        elif rotina == 'constroi_while2': self.constroi_while2()
        elif rotina == 'fecha_while': self.fecha_while()
        # FIM COMANDO WHILE

        elif rotina == 'get_len_v': self.get_len_v()
        elif rotina == 'get_len': self.get_len()

        if self.__log:
            print('saí da sub-rotina de geração de código objeto...')

    # FUNÇÕES AUXILIARES
    def hex_repr(num):
        if num < 0:
            return hex(((abs(num) ^ 0xffff) + 1) & 0xffff)[-4:]
        else:
            return "{:0>4X}".format(num)

    def get_const_num_repr(self, num):
        label = "K_" + gerar_codigo_assembly.hex_repr(int(num)).upper()
        const_existe = self.tabela_simbolos.existe(label)
        if not const_existe:
            nova_const = ST.SimboloConst(label, "const", self.tipos["int"], num)
            nova_const.referenciado = True
            nova_const.utilizado = True
            self.tabela_simbolos.inserir_const(nova_const)
            self.constantes.append("{nome}\tK /{val}".format(nome=nova_const.nome, val=nova_const.nome[2:]))
        return label

    def log_tabela(self):
        escopo = self.tabela_simbolos.escopo_atual
        while escopo is not None:
            print()
            for s in escopo.simbolos:
                print("{0.nome}    {0.tipo.s}    {0.especie}    {0.posicao}".format(s))
            print()
            escopo = escopo.pai
    
    def load_val(self, operando):
        if (operando.especie == "var"
            or operando.especie == "par"):
                self.codigo.append('LD {}'.format(self.get_const_num_repr(operando.posicao)))
                self.codigo.append('SC PUSH')
                self.codigo.append('SC GET_FROM_FRAME')
        elif operando.especie == "const":
            self.codigo.append('LD {}'.format(operando.nome))
        self.codigo.append('SC PUSH')
        self.pilha_tipos_resultados_parciais.append(operando.tipo.s)
        print(self.pilha_tipos_resultados_parciais)
    # FIM FUNÇÕES AUXILIARES

    # DECLARAÇÃO DE FUNÇÕES
    def declaracao_funcao(self, nome_func):
        func_existe = self.tabela_simbolos.existe(nome_func)
        if not func_existe:
            self.__func_atual = ST.SimboloFunc(nome_func, self.tipos["void"]) # toda função é procedimento até que se prove o contrário
            self.tabela_simbolos.inserir_simbolo(self.__func_atual)
            self.tabela_simbolos.novo_escopo()
            self.codigo.append("{}\t$ =1".format(self.__func_atual.nome))
        self.__contador_ifs = 0
        self.__pilha_ids_if = []
        self.__pilha_ids_elif = []
        self.__contador_whiles = 0
        self.__pilha_ids_while = []

    def definir_tipo_funcao(self, tipo_retorno):
        if tipo_retorno in self.tipos:
            self.__func_atual.tipo = self.tipos[tipo_retorno]

    def inicia_declaracao_parametros(self):
        self.__lista_parametros = []

    def novo_par(self, nome_par):
        self.__lista_parametros.append(nome_par)

    def parametro_eh_ponteiro(self):
        if self.__tipo_atual.s == 'int':
            self.__tipo_atual = self.tipos['int pointer']
        elif self.__tipo_atual.s == 'bool':
            self.__tipo_atual = self.tipos['bool pointer']

    def fecha_declaracao_parametro(self, tipo_par):
        for nome_par in self.__lista_parametros:
            parametro_existe = self.tabela_simbolos.existe(nome_par)
            if not parametro_existe:
                par_simb = ST.Simbolo(nome_par, "par", self.__tipo_atual)
                self.tabela_simbolos.inserir_simbolo(par_simb)
                self.__func_atual.add_parametro(par_simb)

    def encerra_funcao(self):
        escopo = self.tabela_simbolos.escopo_atual
        print()
        for s in escopo.simbolos:
            print("{0.nome}    {0.tipo.s}    {0.especie}    {0.posicao}".format(s))
        print('return:', self.__func_atual.offset_valor_retorno)
        self.tabela_simbolos.remover_escopo()
        self.codigo.append("LD FP")
        self.codigo.append("-  WORD_TAM")
        self.codigo.append("MM SP")
        self.codigo.append("RET_{0}\tRS\t{0}".format(self.__func_atual.nome))
        self.__func_atual = None

    def inicia_declaracao_variavel(self):
        self.__lista_variaveis_a_declarar = []
        self.__tipo_atual = None
        self.__dims = []

    def add_tipo(self, tipo):
        self.__tipo_atual = self.tipos[tipo]

    def add_dim(self, dim):
        self.__dims.append(dim)
        if self.__tipo_atual.s == 'int':
            self.__tipo_atual = self.tipos['int pointer']
        elif self.__tipo_atual.s == 'bool':
            self.__tipo_atual = self.tipos['bool pointer']

    def nova_var(self, nome_var):
        self.__lista_variaveis_a_declarar.append(nome_var)

    def fecha_declaracao_variavel(self, tipo_var):
        for nome_var in self.__lista_variaveis_a_declarar:
            variavel_existe = self.tabela_simbolos.existe(nome_var)
            if not variavel_existe:
                if self.__dims:
                    var_simb = ST.SimboloArray(nome_var, "var", self.__tipo_atual, self.__dims)
                else:
                    var_simb = ST.Simbolo(nome_var, "var", self.__tipo_atual)
                self.__func_atual.pilha_variaveis_offset += var_simb.tipo.tamanho
                var_simb.posicao = self.__func_atual.pilha_variaveis_offset
                self.tabela_simbolos.inserir_simbolo(var_simb)
                self.__func_atual.add_variavel(var_simb)
                if (var_simb.tipo.s == 'int pointer'
                    or var_simb.tipo.s == 'bool pointer'):
                        if len(var_simb.dimensoes) == 1:
                            self.codigo.append('LD {}'.format(self.get_const_num_repr(var_simb.dimensoes[0])))
                            self.codigo.append('MM DIM_1')
                            self.codigo.append('SC NEW_ARRAY')
                        elif len(var_simb.dimensoes) == 2:
                            self.codigo.append('LD {}'.format(self.get_const_num_repr(var_simb.dimensoes[0])))
                            self.codigo.append('MM DIM_1')
                            self.codigo.append('LD {}'.format(self.get_const_num_repr(var_simb.dimensoes[1])))
                            self.codigo.append('MM DIM_2')
                            self.codigo.append('SC NEW_MATRIX')
                        self.codigo.append('SC PUSH  ; var %s'%var_simb.nome)

                else:
                    for b in range(0, var_simb.tipo.tamanho, 2):
                        self.codigo.append('LD K_0000')
                        self.codigo.append('SC PUSH  ; var %s'%var_simb.nome)
                    

    def calcular_end_parametros(self):
        for i in range(len(self.__func_atual.parametros)-1, -1, -1):
            par_simb = self.__func_atual.parametros[i]
            par_simb.posicao = self.__func_atual.pilha_parametros_offset
            self.__func_atual.pilha_parametros_offset -= par_simb.tipo.tamanho
        self.__func_atual.offset_valor_retorno = self.__func_atual.pilha_parametros_offset
    # FIM DECLARAÇÃO DE FUNÇÕES

    # EXPRESSÕES MATEMÁTICAS
    def iniciar_expressao_mat(self):
        # self.pilha_operadores.append('LD')
        # if not self.__fp_em_base:
        #     self.codigo.append("LD FP")
        #     self.codigo.append("MM BASE")
            # self.__fp_em_base = False
        self.inverte.append(False)

    def mais_ou_menos(self, operador):
        print(self.pilha_operadores)
        if self.inverte[-1]:
            self.codigo.append('LD K_FFFF')
            self.codigo.append('SC PUSH')
            self.codigo.append('SC PUSHDOWN_MUL')
            self.inverte[-1] = False
        if self.pilha_operadores:
            if (self.pilha_operadores[-1] == '*'
                or self.pilha_operadores[-1] =='/'):
                    self.sai_termo()
            if self.pilha_operadores and self.pilha_operadores[-1] != '(':
                operador_old = self.pilha_operadores.pop()
                if (self.pilha_tipos_resultados_parciais[-1]
                    == self.pilha_tipos_resultados_parciais[-2]):
                        if operador_old == '+':
                            self.codigo.append('SC PUSHDOWN_SUM')
                        elif operador_old == '-':
                            self.codigo.append('SC PUSHDOWN_DIF')
                        self.pilha_tipos_resultados_parciais.pop()
                        print(self.pilha_tipos_resultados_parciais)
        self.pilha_operadores.append(operador)
        print(self.pilha_operadores)

    def vezes_ou_dividir(self, operador):
        if self.inverte[-1]:
            self.codigo.append('LD K_FFFF')
            self.codigo.append('SC PUSH')
            self.codigo.append('SC PUSHDOWN_MUL')
            self.inverte[-1] = False
        if self.pilha_operadores:
            operador_old = self.pilha_operadores[-1]
            if (self.pilha_tipos_resultados_parciais[-1]
                == self.pilha_tipos_resultados_parciais[-2]):
                    if operador_old == '*':
                        self.codigo.append('SC PUSHDOWN_MUL')
                        self.pilha_operadores.pop()
                        self.pilha_tipos_resultados_parciais.pop()
                    elif operador_old == '/':
                        self.codigo.append('SC PUSHDOWN_DIV')
                        self.pilha_operadores.pop()
                        self.pilha_tipos_resultados_parciais.pop()
                    print(self.pilha_tipos_resultados_parciais)
        self.pilha_operadores.append(operador)
        print(self.pilha_operadores)

    def recebe_operando_id(self, operando):
        s = self.tabela_simbolos.procurar(operando)
        if s is not None:
            if s.especie == "func":
                self.__identificador_atual.append(s)
                self.pilha_operadores.append('(')
            else:
                if s.tipo.s == 'int pointer' or s.tipo.s == 'bool pointer': # q p... de sintaxe :-(
                    self.__identificadores_do_len.append(s)
                    self.pilha_operadores.append('(')
                self.load_val(s)

    def recebe_operando_num(self, num):
        label = self.get_const_num_repr(num)
        self.load_val(self.tabela_simbolos.procurar(label))

    def finalizar_expressao_mat(self):
        if self.inverte[-1]:
            self.codigo.append('LD K_FFFF')
            self.codigo.append('SC PUSH')
            self.codigo.append('SC PUSHDOWN_MUL')
        self.inverte.pop()
        if self.pilha_operadores:
            if (self.pilha_operadores[-1] == '*'
                or self.pilha_operadores[-1] =='/'):
                    self.sai_termo()
            if self.pilha_operadores and self.pilha_operadores[-1] != '(':
                operador_old = self.pilha_operadores.pop()
                if (self.pilha_tipos_resultados_parciais[-1]
                    == self.pilha_tipos_resultados_parciais[-2]):
                        if operador_old == '+':
                            self.codigo.append('SC PUSHDOWN_SUM')
                        elif operador_old == '-':
                            self.codigo.append('SC PUSHDOWN_DIF')
                        self.pilha_tipos_resultados_parciais.pop()
                        print(self.pilha_tipos_resultados_parciais)
        # cuida das comparacoes (eu acho)
        if self.pilha_operadores_booleanos:
            comp = self.pilha_operadores_booleanos.pop()
            if (self.pilha_tipos_resultados_parciais[-1] == 'int'
                and self.pilha_tipos_resultados_parciais[-2] == 'int'):
                    if comp == '==':
                        self.codigo.append('SC IGUAL')
                    elif comp == '>=':
                        self.codigo.append('SC MAIOR_OU_IGUAL')
                    elif comp == '<=':
                        self.codigo.append('SC MENOR_OU_IGUAL')
                    elif comp == '!=':
                        self.codigo.append('SC DIFERENTE')
                    elif comp == '>':
                        self.codigo.append('SC MAIOR')
                    elif comp == '<':
                        self.codigo.append('SC MENOR')
                    self.pilha_tipos_resultados_parciais.pop()
                    self.pilha_tipos_resultados_parciais.pop()
                    self.pilha_tipos_resultados_parciais.append('bool')

    def abre_parenteses(self):
        self.pilha_operadores.append('(')
        self.inverte.append(False)

    def fecha_parenteses(self):
        # finaliza a expressão interna
        while self.pilha_operadores[-1] != '(':
            self.finalizar_expressao_mat()
        self.pilha_operadores.pop() # retira o '('

    def sai_termo(self):
        # termina a operacap de * ou /
        operador = self.pilha_operadores.pop()
        if (self.pilha_tipos_resultados_parciais[-1]
            == self.pilha_tipos_resultados_parciais[-2]):
                if operador == '*':
                    self.codigo.append('SC PUSHDOWN_MUL')
                elif operador == '/':
                    self.codigo.append('SC PUSHDOWN_DIV')
                self.pilha_tipos_resultados_parciais.pop()
                print(self.pilha_tipos_resultados_parciais)

    def separa_argumentos(self):
        if self.pilha_operadores:
            # print(self.pilha_operadores[-1])
            while self.pilha_operadores[-1] != '(':
                self.finalizar_expressao_mat()
        self.guarda_parametro()

    def inverte_termo(self):
        self.inverte[-1] = True

    def guarda_parametro_e_chamar_funcao(self):
        self.separa_argumentos()
        if self.pilha_operadores:
            self.pilha_operadores.pop()
        self.chamar_funcao()
        if self.inverte[-1]:
            self.codigo.append('LD K_FFFF')
            self.codigo.append('SC PUSH')
            self.codigo.append('SC PUSHDOWN_MUL')
            self.inverte[-1] = False
    # FIM EXPRESSÕES MATEMÁTICAS

    # EXPRESSÕES BOOLEANAS
    def and_op(self):
        pass

    def or_op(self):
        pass

    def recebe_comparador(self, comparador):
        self.finalizar_expressao_mat()
        if self.pilha_tipos_resultados_parciais[-1] == "int":
            self.iniciar_expressao_mat()
            self.pilha_operadores_booleanos.append(comparador)

    # FIM EXPRESSÕES BOOLEANAS

    # CHAMADA DE PROCEDIMENTOS
    def iniciar_frame(self):
        self.codigo.append('; espaco para valor de retorno')
        for b in range(0, self.__identificador_atual[-1].tipo.tamanho, 2):
            self.codigo.append('LD K_0000')
            self.codigo.append('SC PUSH')
        # reserva espaço para os parâmetros
        self.__contador_parametros_atribuidos.append(0)

    def chamar_funcao(self):
        # empilha o endereço de retorno
        self.codigo.append("LD {}".format(self.__func_atual.nome))
        self.codigo.append("SC PUSH")
        # empilha o FP
        self.codigo.append("LD FP")
        self.codigo.append("SC PUSH")
        # atualiza FP com seu novo valor
        self.codigo.append("; troca o contexto")
        self.codigo.append("LD SP")
        self.codigo.append("+ WORD_TAM")
        self.codigo.append("MM FP")
        self.codigo.append("SC {}".format(self.__identificador_atual[-1].nome))
        self.codigo.append("; volta ao contexto anterior")
        self.codigo.append("SC POP ; restaura FP")
        self.codigo.append("MM FP")
        self.codigo.append("SC POP ; restaura end. de retorno")
        self.codigo.append("MM {}".format(self.__func_atual.nome))
        for i in range(self.__contador_parametros_atribuidos[-1]):
            self.codigo.append("SC POP")
        self.codigo.append("; termina de desempilhar os parametros passados aa funcao")
        self.codigo.append("; resta o valor de retorno no topo da pilha")
        self.__identificador_atual.pop()
        self.__contador_parametros_atribuidos.pop()

    def guarda_parametro(self):
        par = self.__identificador_atual[-1].parametros[self.__contador_parametros_atribuidos[-1]]
        self.codigo.append("; par %s"%par.nome)
        self.__contador_parametros_atribuidos[-1] += 1
    # FIM CHAMADA DE PROCEDIMENTOS

    # COMANDO SIMPLES
    def inicia_comando_simples(self, identificador):
        # procura o identificador na tabela
        s = self.tabela_simbolos.procurar(identificador)
        # se encontrou em algum escopo
        if s is not None:
            self.__identificador_atual.append(s)
            self.__identificador_atual[-1].utilizado = True

    def comando_atribuicao(self):
        simb = self.__identificador_atual.pop()
        if simb.tipo.s != 'int pointer' and simb.tipo.s != 'bool pointer':
            if (self.pilha_tipos_resultados_parciais[-1]
                == simb.tipo.s):
                    self.codigo.append("LD {}".format(self.get_const_num_repr(simb.posicao)))
                    self.codigo.append("SC PUSH")
                    self.codigo.append("SC SET_TO_FRAME")
        else:
                    self.load_val(simb)
                    self.codigo.append('LD WORD_TAM')
                    self.codigo.append('SC PUSH')
                    self.codigo.append('SC PUSHDOWN_SUM')
                    self.codigo.append('SC SET_TO_VECT')

        self.pilha_tipos_resultados_parciais.pop()
        print(self.pilha_tipos_resultados_parciais)

    def comando_retorno(self):
        self.codigo.append("LD {}".format(self.get_const_num_repr(self.__func_atual.offset_valor_retorno)))
        self.codigo.append("SC PUSH")
        self.codigo.append("SC SET_TO_FRAME")
        self.codigo.append("JP RET_{}".format(self.__func_atual.nome))
    # FIM COMANDO SIMPLES

    # COMANDO IF
    def constroi_if(self):
        self.__contador_ifs += 1
        self.__pilha_ids_if.append(self.__contador_ifs)
        self.__contador_elifs = 0
        self.__pilha_ids_elif.append([self.__contador_elifs])
        self.codigo.append('{}_IF_{} SC POP'.format(self.__func_atual.nome, self.__pilha_ids_if[-1]))
        self.pilha_tipos_resultados_parciais.pop()
        dummy_label = next(self.__dummy_labels_generator)
        self.labels_a_resolver.append((dummy_label, len(self.codigo)))
        self.codigo.append('JZ {}'.format(dummy_label))

    def constroi_elif(self):
        self.__contador_elifs += 1
        self.__pilha_ids_elif[-1].append([self.__contador_elifs])
        dummy_label, indice = self.labels_a_resolver.pop()
        label_elif = '{}_ELIF_{}_{}'.format(self.__func_atual.nome, self.__pilha_ids_if[-1], self.__contador_elifs)
        self.codigo.append(label_elif + ' SC POP')
        label_real = self.codigo[indice]
        label_real = label_real.replace(' {}'.format(dummy_label), ' ' + label_elif)
        self.codigo[indice] = label_real
        self.labels_a_resolver.append((dummy_label, len(self.codigo)))
        self.codigo.append('JZ {}'.format(dummy_label))

    def constroi_else(self):
        self.codigo.append('JP {}_END_IF_{}'.format(self.__func_atual.nome, self.__pilha_ids_if[-1]))
        dummy_label, indice = self.labels_a_resolver.pop()
        label_else = '{}_ELSE_{}'.format(self.__func_atual.nome, self.__pilha_ids_if[-1])
        self.codigo.append(label_else + ' + K_0000 ; pseudo NOP')
        label_real = self.codigo[indice]
        label_real = label_real.replace(' {}'.format(dummy_label), ' ' + label_else)
        self.codigo[indice] = label_real

    def fecha_if(self):
        self.codigo.append('JP {}_END_IF_{}'.format(self.__func_atual.nome, self.__pilha_ids_if[-1]))
        dummy_label, indice = self.labels_a_resolver.pop()
        label_real = self.codigo[indice]
        label_real = label_real.replace(' {}'.format(dummy_label), ' {}_END_IF_{}'.format(self.__func_atual.nome, self.__pilha_ids_if[-1]))
        self.codigo[indice] = label_real
        self.codigo.append('{}_END_IF_{} + K_0000 ; pseudo NOP'.format(self.__func_atual.nome, self.__pilha_ids_if[-1]))
        self.__pilha_ids_if.pop()

    def fecha_else(self):
        self.codigo.append('{}_END_IF_{} + K_0000 ; pseudo NOP'.format(self.__func_atual.nome, self.__pilha_ids_if[-1]))
        self.__pilha_ids_if.pop()
    # FIM COMANDO IF

    # COMANDO WHILE
    def constroi_while(self):
        self.__contador_whiles += 1
        self.__pilha_ids_while.append(self.__contador_whiles)
        self.codigo.append('{}_WHILE_{} + K_0000'.format(self.__func_atual.nome, self.__pilha_ids_while[-1]))
    def constroi_while2(self):
        self.codigo.append('SC POP')
        self.pilha_tipos_resultados_parciais.pop()
        self.codigo.append('JZ {}_END_WHILE_{}'.format(self.__func_atual.nome, self.__pilha_ids_while[-1]))
    def fecha_while(self):
        self.codigo.append('JP {}_WHILE_{}'.format(self.__func_atual.nome, self.__pilha_ids_while[-1]))
        self.codigo.append('{}_END_WHILE_{} + K_0000'.format(self.__func_atual.nome, self.__pilha_ids_while[-1]))
        self.__pilha_ids_while.pop()
    # FIM COMANDO WHILE

    def get_len_v(self):
        v = self.__identificadores_do_len.pop()
        if v.tipo.s == 'int pointer' or v.tipo.s == 'bool pointer':
            self.codigo.append('LD K_0000')
            self.codigo.append('SC PUSH')
            self.codigo.append('SC GET_LENGTH')
            self.pilha_tipos_resultados_parciais.pop()
            self.pilha_tipos_resultados_parciais.append('int')
            self.pilha_operadores.pop()

    def get_len(self):
        v = self.__identificadores_do_len.pop()
        if v.tipo.s == 'int pointer' or v.tipo.s == 'bool pointer':
            self.codigo.append('SC GET_LENGTH')
            self.pilha_tipos_resultados_parciais.pop()
            self.pilha_tipos_resultados_parciais.pop()
            self.pilha_tipos_resultados_parciais.append('int')
            print(self.pilha_tipos_resultados_parciais)
            self.pilha_operadores.pop()
