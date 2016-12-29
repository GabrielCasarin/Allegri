JAVA=/usr/bin/java

# Diretórios
BINDIR=Gerador_Codigo_Executavel/assembler
LIBDIR=Gerador_Codigo_Executavel/biblioteca
BIB_ARQS = boolean const environment comparacao push_pop heap

# montador MVN
MONTADOR=montador.MvnAsm
LINKADOR=linker.MvnLinker
RELOCADOR=relocator.MvnRelocator

.PRECIOUS: %.mvn

$(fonte): $(fonte).mvn $(addprefix $(LIBDIR)/, $(addsuffix .mvn, $(BIB_ARQS)))
	$(JAVA) -cp $(BINDIR)/MLR.jar $(LINKADOR) $^ -s linkado.mvn
	$(JAVA) -cp $(BINDIR)/MLR.jar $(RELOCADOR) linkado.mvn $(fonte).mvn 0000 0000
	rm linkado.mvn
	rm $(fonte).run


$(fonte).mvn: $(fonte).asm
	$(JAVA) -cp $(BINDIR)/MLR.jar $(MONTADOR) $^
	rm $(fonte).lst


$(LIBDIR)/%.mvn: $(LIBDIR)/%.asm
	$(JAVA) -cp $(BINDIR)/MLR.jar $(MONTADOR) $^
	rm $(LIBDIR)/$*.lst


$(fonte).asm: $(fonte).barber
	python compilador.py $(fonte)


gerar_reconhecedor_sintatico:
	python converte_wirth_em_ape.py $(fonte) $(fonte)


run:
	@$(JAVA) -jar $(BINDIR)/mvn.jar


rm:
	rm $(fonte).asm
