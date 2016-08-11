# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from analisador_lexico import extrai_texto_fonte, analise_lexica, analise_sintatica


with open('conf.txt') as arq_conf:
    log_extrai_texto_fonte = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_analise_lexica = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_analise_sintatica = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False

extrai_texto_fonte()('cool.so', log_extrai_texto_fonte)
analise_lexica(log_analise_lexica)
analise_sintatica(log_analise_sintatica)
