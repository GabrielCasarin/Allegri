import string
from util.mr2 import MetaReconhecedor
from util.minimizador import *

mr2 = MetaReconhecedor(log=False)
mr2.add_evento(('<PartidaInicial>',))
mr2.add_evento(('<ChegadaSimbolo>', ('S', 'NT')))
mr2.add_evento(('<ChegadaSimbolo>', ('=', '=')))


mr2.add_evento(('<ChegadaSimbolo>', ('(', '(')))
mr2.add_evento(('<ChegadaSimbolo>', ('"', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('{', '{')))
mr2.add_evento(('<ChegadaSimbolo>', ('Letra', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('Algarismo', 'TERM')))
for c in string.punctuation:
    if c != '"':
        mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
        mr2.add_evento(('<ChegadaSimbolo>', (c, 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('}', '}')))
mr2.add_evento(('<ChegadaSimbolo>', ('"', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', (')', ')')))

mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))

mr2.add_evento(('<ChegadaSimbolo>', ('(', '(')))
mr2.add_evento(('<ChegadaSimbolo>', ('Letra', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('{', '{')))
mr2.add_evento(('<ChegadaSimbolo>', ('Letra', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('Algarismo', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('}', '}')))
mr2.add_evento(('<ChegadaSimbolo>', (')', ')')))

mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))

mr2.add_evento(('<ChegadaSimbolo>', ('(', '(')))
mr2.add_evento(('<ChegadaSimbolo>', (';', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('{', '{')))
mr2.add_evento(('<ChegadaSimbolo>', ('Letra', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('Algarismo', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('espaco', 'TERM')))
for c in string.punctuation:
    mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
    mr2.add_evento(('<ChegadaSimbolo>', (c, 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('}', '}')))
mr2.add_evento(('<ChegadaSimbolo>', ('enter', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', (')', ')')))

mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))

mr2.add_evento(('<ChegadaSimbolo>', ('(', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', (')', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('{', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('}', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('[', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', (']', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('.', 'TERM')))
mr2.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr2.add_evento(('<ChegadaSimbolo>', ('=', 'TERM')))

mr2.add_evento(('<ChegadaSimbolo>', ('.', '.')))

mr2.run()

S = mr2.submaquinas['S']
eliminar_transicoes_em_vazio(S)
eliminar_indeterminismos(S)
eliminar_estados_inacessiveis(S, 'q0')
particao = minimizador_de_Hopcroft(S)
print(particao)
particao_para_automato_finito(particao)
