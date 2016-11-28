%.asm:
	python compilador.py $* $*

%: %.asm
	if [ -e mvn_build_system/src/$< ] ;\
		then cd mvn_build_system; make $*; make run ;\
	fi ;

salva_no_rela:
	cp src/$(prog).barber relatorio/
	cp mvn_build_system/src/$(prog).asm relatorio/
