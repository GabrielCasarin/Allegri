
$(fonte): mvn_build_system/src/$(fonte).asm
	if [ -e $< ] ;\
		then cd mvn_build_system; make $(fonte); make run ;\
	fi ;

mvn_build_system/src/$(fonte).asm: src/$(fonte).barber
	python compilador.py $(fonte)

salva_no_rela:
	cp src/$(fonte).barber relatorio/
	cp mvn_build_system/src/$(fonte).asm relatorio/
