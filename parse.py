import re
from comum import TransdutorFinito

with open('gramatica_lexica_wirth.maquina') as arq:
    match_automato = re.compile(r'<(?P<nome>\w+)>(.*)</(?P=nome)>', re.DOTALL | re.MULTILINE)
    match_transicoes = re.compile(r"\(([a-zA-Z]\w*)\s*,\s*'(.+)'\s*\)\s*->\s*([a-zA-Z]\w*)(?:\\(\w+))?")
    texto = arq.read()
    mo1 = match_automato.search(texto)
    nome_automato = mo1.group(1)
    linhas = mo1.group(2).split('\n')

    linha_atual = 0

    while linhas[linha_atual] == '':
        linha_atual += 1
    estados = linhas[linha_atual].split()
    linha_atual += 1

    while linhas[linha_atual] == '':
        linha_atual += 1
    inicial = linhas[linha_atual]
    linha_atual += 1

    while linhas[linha_atual] == '':
        linha_atual += 1
    finais = linhas[linha_atual].split()
    linha_atual += 1

    while linhas[linha_atual] == '':
        linha_atual += 1
    alfabeto = linhas[linha_atual].split()

    tf = TransdutorFinito(nome=nome_automato, estados=estados, estadoInicial=inicial, estadosFinais=finais, alfabeto=alfabeto)

    for mo2 in match_transicoes.finditer(mo1.group(2)):
        qi, s, qj, saida = mo2.groups()
        tf.add_transicao(de=qi, com=s, para=qj)
        if saida is not None:
            tf.add_saida(de=qi, com=s, saida=saida)

    print(nome_automato)
    print(estados)
    print(inicial)
    print(finais)
    print(set(alfabeto))
