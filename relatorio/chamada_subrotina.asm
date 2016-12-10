PUSH    <
POP     <
SP      <
FP      <
TRUE    <
FALSE   <
AND     <
OR      <
NOT     <
GET_FROM_FRAME  <
SET_TO_FRAME    <
GET_FROM_VECT   <
SET_TO_VECT     <
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
K_0000    <
K_0001    <
K_0002    <
K_FFFF    <
WORD_TAM  <
DIM_1     <
DIM_2     <
INIT_HEAP      <
NEW_ARRAY      <
NEW_MATRIX     <

; inicio do codigo
&     /0000
SC    INIT_HEAP
LD    SP
+     WORD_TAM
MM    FP
SC    main
FIM   HM FIM
; declaracao de CONSTANTES
K_0004	K /0004
K_0007	K /0007
K_FFFA	K /FFFA
K_FFFC	K /FFFC
K_FFF8	K /FFF8
K_000A	K /000A
K_0014	K /0014
; declaracao de FUNCOES
f	$ =1
LD K_0000
SC PUSH  ; var v3
LD K_0000
SC PUSH  ; var v4
LD    FP
SC    PUSH
LD    K_0004
*     K_FFFF
SC    PUSH
LD    K_0002
SC    PUSH
SC    SET_TO_VECT
LD    FP
SC    PUSH
LD    K_0002
*     K_FFFF
SC    PUSH
LD    K_0007
SC    PUSH
SC    SET_TO_VECT
LD    K_FFFA
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
SC PUSHDOWN_SUM
LD    K_FFFC
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
SC PUSHDOWN_SUM
SC PUSHDOWN_MUL
LD    K_FFF8
SC    PUSH
SC    SET_TO_FRAME
JP    RET_f
RET_f	LD  FP
-   WORD_TAM
MM  SP
RS	f
main	$ =1
; espaco para valor de retorno
LD K_0000
SC PUSH
LD    K_000A
SC    PUSH
; par p1
LD    K_0014
SC    PUSH
; par p2
LD main
SC PUSH
LD FP
SC PUSH
; troca o contexto
LD SP
+ WORD_TAM
MM FP
SC f
; volta ao contexto anterior
SC POP ; restaura FP
MM FP
SC POP ; restaura end. de retorno
MM main
SC POP
SC POP
; termina de desempilhar os parametros passados aa funcao
; resta o valor de retorno no topo da pilha
RET_main	LD  FP
-   WORD_TAM
MM  SP
RS	main
# FIM
