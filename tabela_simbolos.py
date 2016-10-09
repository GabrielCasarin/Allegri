# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


class Simbolo:
	def __init__(self, nome, tipo):
		super(Simbolo, self).__init__()
		self.nome = nome
		self.tipo = tipo
		self.posicao = None
		self.referenciado = False
		self.utilizado = False

# class IntSimbolo:
# 	tamanho = 1
# 	tipo = "INT"
# 	def __init__(self):
# 		super(Simbolo, self).__init__()

# 		self.valor

class TabelaSimbolos:

	class Escopo:
		def __init__(self, pai):
			super(TabelaSimbolos.Escopo, self).__init__()
			self.pai = pai
			self.simbolos = []

	def __init__(self):
			super(TabelaSimbolos, self).__init__()
			self.escopo_global= TabelaSimbolos.Escopo(pai=None)
			self.escopo_atual = self.escopo_global

	def novo_escopo(self):
		escopo = TabelaSimbolos.Escopo(pai=self.escopo_atual)
		self.escopo_atual = escopo

	def remover_escopo(self):
		if self.escopo_atual.pai is not None:
		    self.escopo_atual = self.escopo_atual.pai

	def inserir_simbolo(self, simbolo):
		self.escopo_atual.simbolos.append(simbolo)

	def procurar(self, simbolo):
		p = self.escopo_atual
		while p is not None:
			for s in range(len(p.simbolos)):
				if p.simbolos[s].nome == simbolo:
					return p, s
			p = p.pai
		return None, None