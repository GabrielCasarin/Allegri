# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import re
from comum import AutomatoPilhaEstruturado
from comum.carregar_automato_finito import parse_tf


def automato_pilha_estruturado(nome_arquivo):
	with open(nome_arquivo) as f:
		texto = f.read()
		texto = re.sub(r'\n+', '\n', texto)
