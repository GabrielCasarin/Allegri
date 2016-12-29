# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import os
import sys
import string
from comum.configuracoes import *

from comum.compilador import decompoe_texto_fonte, analisador_lexico
from comum.compilador import analisador_sintatico
from Barber_Lang.analise_semantica import gerar_codigo_assembly

import comum.automatos.loaders as loaders


# lê o texto-fonte
decompositor = decompoe_texto_fonte(log_decompoe_texto_fonte, log_imprimir_linhas, log_imprimir_caracteres)
decompositor.add_categoria('enter', ['\n'])
decompositor.add_categoria('espaco', ['\t', ' '])
decompositor.add_categoria('Letra', string.ascii_uppercase[6:] + string.ascii_lowercase[6:]) # Letras não HA
decompositor.add_categoria('HexAlg', string.ascii_uppercase[:6] + string.ascii_lowercase[:6]) # Hexadecimal Algarismo
decompositor.add_categoria('Zero', ['0'])
decompositor.add_categoria('DecAlg', string.digits[1:]) # Decimal Algarismo sem o zero

# cria o automato que reconhece os diversos tokens da linguagem
automato_tokenizador_de_barber = loaders.transdutor_finito(os.path.join(ROOT_DIR, BARBER_DIR, 'tokenizer_barber.af'))

# palavras reservadas
palavras_reservadas = tuple(open(os.path.join(BARBER_DIR, 'barber.tokens')).read().splitlines())

# analisador léxico
tokenizer = analisador_lexico(automato_tokenizador_de_barber, decompositor, None, log_analise_lexica, palavras_reservadas)
tokenizer.add_classificacao('q39', 'enter')
tokenizer.add_classificacao('q15', 'Identificador')
tokenizer.add_classificacao('q29', 'NumeroDecimal')
tokenizer.add_classificacao('q30', 'NumeroDecimal')
tokenizer.add_classificacao('q4', 'Comparacao')  # ==
tokenizer.add_classificacao('q7', 'Comparacao')  # >=
tokenizer.add_classificacao('q20', 'Comparacao') # <=
tokenizer.add_classificacao('q27', 'Comparacao') # !=
tokenizer.add_classificacao('q36', 'Comparacao') # >
tokenizer.add_classificacao('q22', 'Comparacao') # <

# instancia o gerador de código MVN
gc = gerar_codigo_assembly(True)

# instancia um analisador sintático
automato_sintatico = loaders.automato_pilha_estruturado(os.path.join(BARBER_DIR, 'barber.ap'))
analisador_sintatico = analisador_sintatico(automato_sintatico, tokenizer, gc, log=log_analise_sintatica)

arquivo_saida = 'aout'
if len(sys.argv) == 2:
    arquivo_fonte = sys.argv[1] + '.barber'
    arquivo_saida = sys.argv[1] + '.asm'

# Executa a compilação a partir DAQUI
analisador_sintatico(arquivo_fonte)

# salva
with open(arquivo_saida, 'w') as aout:
    for line in gc.preambulo:
        aout.write(line + '\n')
    aout.write('; declaracao de CONSTANTES\n')
    for line in gc.constantes:
        aout.write(line + '\n')
    aout.write('; declaracao de FUNCOES\n')
    for line in gc.codigo:
        aout.write(line + '\n')
    aout.write('# FIM\n')
