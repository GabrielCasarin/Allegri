PUSH    <
POP     <
SP      <
TRUE    <
FALSE   <
AND     <
OR      <
NOT     <
GET_VECT    <
SET_VECT    <
GET_OFFSET  <
SET_OFFSET  <
PUSHDOWN_SUM    <
PUSHDOWN_DIF    <
PUSHDOWN_MUL    <
PUSHDOWN_DIV    <
GET_LENGTH      <
IGUAL           <
DIFERENTE       <
MAIOR           <
MAIOR_OU_IGUAL  <
MENOR           <
MENOR_OU_IGUAL  <
BASE      <
K_0000    <
K_0001    <
K_FFFF    <
WORD_TAM  <
DIM_1     <
DIM_2     <
INIT_HEAP      <
NEW_ARRAY      <
NEW_MATRIX     <
&     /0000
SC    INIT_HEAP
LD    SP
+     WORD_TAM
MM    FP
SC    main
FIM   HM FIM
FP    $ =1
; declaracao de CONSTANTES
K_FFFC	K /FFFC
K_FFFA	K /FFFA
K_0006	K /0006
K_0004	K /0004
K_0002	K /0002
; declaracao de FUNCOES
fat	$ =1
LD FP
MM BASE
LD K_FFFC
SC PUSH
SC GET_VECT
SC PUSH
LD K_0000
SC PUSH
SC IGUAL
fat_IF_1 SC POP
JZ fat_END_IF_1
LD K_0001
SC PUSH
LD FP
MM BASE
LD K_FFFA
SC PUSH
SC SET_VECT
JP RET_fat
JP fat_END_IF_1
fat_END_IF_1 + K_0000 ; pseudo NOP
LD FP
MM BASE
LD K_FFFC
SC PUSH
SC GET_VECT
SC PUSH
; espaco para valor de retorno
LD K_0000
SC PUSH
LD FP
MM BASE
LD K_FFFC
SC PUSH
SC GET_VECT
SC PUSH
LD K_0001
SC PUSH
SC PUSHDOWN_DIF
; par n
LD fat
SC PUSH
LD FP
SC PUSH
; troca o contexto
LD SP
+ WORD_TAM
MM FP
SC fat
; volta ao contexto anterior
SC POP ; restaura FP
MM FP
SC POP ; restaura end. de retorno
MM fat
SC POP
; termina de desempilhar os parametros passados aa funcao
; resta o valor de retorno no topo da pilha
SC PUSHDOWN_MUL
LD FP
MM BASE
LD K_FFFA
SC PUSH
SC SET_VECT
JP RET_fat
LD FP
-  WORD_TAM
MM SP
RET_fat	RS	fat
main	$ =1
LD K_0000
SC PUSH  ; var a
LD K_0000
SC PUSH  ; var b
LD K_0006
SC PUSH
LD FP
MM BASE
LD K_0004
SC PUSH
SC SET_VECT
; espaco para valor de retorno
LD K_0000
SC PUSH
LD FP
MM BASE
LD K_0004
SC PUSH
SC GET_VECT
SC PUSH
; par n
LD main
SC PUSH
LD FP
SC PUSH
; troca o contexto
LD SP
+ WORD_TAM
MM FP
SC fat
; volta ao contexto anterior
SC POP ; restaura FP
MM FP
SC POP ; restaura end. de retorno
MM main
SC POP
; termina de desempilhar os parametros passados aa funcao
; resta o valor de retorno no topo da pilha
LD FP
MM BASE
LD K_0002
SC PUSH
SC SET_VECT
LD FP
-  WORD_TAM
MM SP
RET_main	RS	main
# FIM
