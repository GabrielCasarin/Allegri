
$(fonte): Gerador_Codigo_Executavel/src/$(fonte).asm
	if [ -e $< ] ;\
		then cd Gerador_Codigo_Executavel;\
		make $(fonte);\
		make run ;\
	fi ;

Gerador_Codigo_Executavel/src/$(fonte).asm: src/$(fonte).barber
	python compilador.py $(fonte)

gerar_reconhecedor_sintatico:
	python converte_wirth_em_ape.py $(fonte) $(fonte)

salva_no_rela:
	cp src/$(fonte).barber relatorio/
	cp Gerador_Codigo_Executavel/src/$(fonte).asm relatorio/

rm:
	rm Gerador_Codigo_Executavel/src/$(fonte).asm
