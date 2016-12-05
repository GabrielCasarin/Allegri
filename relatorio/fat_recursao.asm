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
K_FFFC	K /FFFC
K_FFFA	K /FFFA
K_0004	K /0004
K_0006	K /0006
; declaracao de FUNCOES
fat	$ =1
LD    K_FFFC
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0000
SC    PUSH
SC IGUAL
fat_IF_1 SC POP
JZ fat_END_IF_1
LD    K_0001
SC    PUSH
LD    K_FFFA
SC    PUSH
SC    SET_TO_FRAME
JP    RET_fat
JP fat_END_IF_1
fat_END_IF_1 + K_0000 ; pseudo NOP
LD    K_FFFC
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
; espaco para valor de retorno
LD K_0000
SC PUSH
LD    K_FFFC
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
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
LD    K_FFFA
SC    PUSH
SC    SET_TO_FRAME
JP    RET_fat
RET_fat	LD  FP
-   WORD_TAM
MM  SP
RS	fat
main	$ =1
LD K_0000
SC PUSH  ; var a
LD K_0000
SC PUSH  ; var b
LD    FP
SC    PUSH
LD    K_0004
*     K_FFFF
SC    PUSH
LD    K_0006
SC    PUSH
SC    SET_TO_VECT
LD    FP
SC    PUSH
LD    K_0002
*     K_FFFF
SC    PUSH
; espaco para valor de retorno
LD K_0000
SC PUSH
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
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
SC    SET_TO_VECT
RET_main	LD  FP
-   WORD_TAM
MM  SP
RS	main
# FIM
