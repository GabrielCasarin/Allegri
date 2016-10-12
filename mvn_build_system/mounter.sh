#!/bin/bash

set -e # Isso serve pra ele não continuar executando se encontrar algum erro.
for ARG in "$@"
do
    java -cp MLR.jar montador.MvnAsm $ARG.asm
done

args_linker=("$@")
args_linker=("${args_linker[@]/%/.mvn}")

java -cp MLR.jar linker.MvnLinker "${args_linker[@]}" ./biblioteca/const.mvn ./biblioteca/push_pop.mvn ./biblioteca/boolean_op.mvn -s ./bin/linkado.mvn

java -cp MLR.jar relocator.MvnRelocator ./bin/linkado.mvn ./bin/saida.mvn 0000 000

java -jar mvn.jar
