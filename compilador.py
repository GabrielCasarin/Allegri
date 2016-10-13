# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import os
import string
from configuracoes import *

from analisador_lexico import decompoe_texto_fonte, analisador_lexico
from analisador_sintatico import analise_sintatica

from util.automatos_loaders import transdutor_finito, automato_pilha_estruturado


decompositor = decompoe_texto_fonte(log_decompoe_texto_fonte, log_imprimir_linhas, log_imprimir_caracteres)
decompositor.add_categoria('enter', ['\n'])
decompositor.add_categoria('espaco', ['\t', ' '])
decompositor.add_categoria('Letra', string.ascii_uppercase[6:] + string.ascii_lowercase[6:]) # Letras não HA
decompositor.add_categoria('HexAlg', string.ascii_uppercase[:6] + string.ascii_lowercase[:6]) # Hexadecimal Algarismo
decompositor.add_categoria('Zero', ['0'])
decompositor.add_categoria('DecAlg', string.digits[1:]) # Decimal Algarismo sem o zero

# cria o automato que reconhece os diversos tokens da linguagem
automato_transdutor_tokenizador_de_barber = transdutor_finito(os.path.join(ROOT_DIR, 'Barber', 'tokenizer_barber.maquina'))

# palavras reservadas
palavras_reservadas = tuple(open(os.path.join('Barber', 'barber.tokens')).read().splitlines())

# analisador léxico
tokenizer = analisador_lexico(automato_transdutor_tokenizador_de_barber, decompositor, None, log_analise_lexica, palavras_reservadas)
tokenizer.add_classificacao('q39', 'enter')
tokenizer.add_classificacao('q15', 'Identificador')
tokenizer.add_classificacao('q29', 'NumeroDecimal')
tokenizer.add_classificacao('q30', 'NumeroDecimal')

# instancia um analisador sintático
automato_sintatico = automato_pilha_estruturado(os.path.join(ROOT_DIR, 'dev', 'simples_funcao.maquina'))
analisador_sintatico = analise_sintatica(automato_sintatico, tokenizer, log=log_analise_sintatica)

# Executa a Transdução a partir DAQUI
analisador_sintatico(os.path.join('src', 'main.barber'))

# print(tokenizer.tokens)
