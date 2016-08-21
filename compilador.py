# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from analisador_lexico import decompoe_texto_fonte, analise_lexica, analise_sintatica
from analisador_semantico import gerar_codigo_intermediario, otimizador, gerar_codigo_objeto


class gerar_codigo_executavel:
    def __init__(self):
        super(gerar_codigo_executavel, self).__init__()

    def __call__(self):
        print('entrei na sub-rotina de geração de código executável...')

        print('saí da sub-rotina de geração de código executável...')


with open('conf.txt') as arq_conf:
    log_decompoe_texto_fonte = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_imprimir_linhas = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_imprimir_caracteres = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_analise_lexica = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_analise_sintatica = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False

# front end
decompoe_texto_fonte(log_decompoe_texto_fonte, log_imprimir_linhas, log_imprimir_caracteres)('prog.txt')
analise_lexica(log_analise_lexica)
analise_sintatica(log_analise_sintatica)

# código intermediário
gerar_codigo_intermediario()()
otimizador()()
gerar_codigo_objeto()()

# back end
gerar_codigo_executavel()()
