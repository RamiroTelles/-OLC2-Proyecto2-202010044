

class Simbolos(): #VALOR - NODO
    
    def __init__(self, id, tipo_simbolo,tipo, valor,ambito, instrucciones = [], parametros = [],RA=0,linea=0,columna=0):
        self.id = id
        self.tipo = tipo
        self.tipo_simbolo =tipo_simbolo
        self.valor = valor
        self.ambito = ambito
        self.RA=RA
        self.instrucciones = instrucciones
        self.parametros = parametros
        
        self.linea = linea
        self.columna = columna


class TablaSimbolos():

    def __init__(self, simbolos = {},ambito='global'):
        self.simbolos = simbolos
        
        self.listaErrores =[]
        self.ambito= ambito
        self.temp=-1
        self.label=-1
        self.msg=-1
        self.inst=""
        self.Datos =""

    def agregar(self, simbolo):
        self.simbolos[simbolo.id] = simbolo

    def obtener(self, id):
        if not id in self.simbolos:
            return None
        else:
            return self.simbolos[id]
    
    def actualizar(self, id, valor):
        if not id in self.simbolos:
            return None
        else:
            self.simbolos[id].valor = valor

    def getNextMsg(self):
        self.msg+=1
        return self.msg
    
    def getLastMsg(self):
        return self.msg
    
    def getNextLabel(self):
        self.label+=1
        return self.label

    def getLastLabel(self):
        return self.label
    
    def getNextTemp(self,offset):
        self.temp+=1
        self.temp-=offset
        if self.temp==17:
            self.temp=0

        if self.temp>6:
            return f's{self.temp-6}'
        else:
            return f't{self.temp}'
    
    
    
    def getLastTemp(self):
        return self.temp
    
    def restoreTemp(self,num):
        self.temp -=num

    def restartTemp(self):
        self.temp=-1


        

    def limpiar(self):
        #self.salida=""
        self.listaErrores.clear()
        self.simbolos.clear()
        self.ambito='global'
        self.inst=""
        self.Datos=""

    def getSalida(self):
        return f'''
    .data
          
    {self.Datos}

    
    msgSalto: .byte 10 
    BufferChar: .byte 0
	msgErrorDivisionlen: .word 21
	msgErrorDivision: .asciz "Error, division por 0"
    msgErrorIndexOutofBoundslen: .word 41
	msgErrorIndexOutofBounds: .asciz "Error, Acceso a array fuera de los limites"
    msgTruelen: .word 4
    msgTrue: .asciz "True"
    msgFalselen: .word 5
    msgFalse: .asciz "False"

    msgCorcheteAbre: .byte 91
    msgCorcheteCierra: .byte 93
    msgComa: .byte 44

    .text
    .globl main
    main:

    {self.inst}

    final:
	li a7, 10    
	ecall

	
	err_divisionZero:
	
	la a0, msgErrorDivisionlen
	la a1, msgErrorDivision
	lw a2, 0(a0)
	li a0,1
	li a7,64
	ecall
	j final

    err_IndexOutofBOunds:
	
	la a0, msgErrorIndexOutofBoundslen
	la a1, msgErrorIndexOutofBounds
	lw a2, 0(a0)
	li a0,1
	li a7,64
	ecall
	j final

    _print_true:

    la a0, msgTruelen
	la a1, msgTrue
	lw a2, 0(a0)
	li a0,1
	li a7,64
	ecall
    ret

    _print_false:

    la a0, msgFalselen
	la a1, msgFalse
	lw a2, 0(a0)
	li a0,1
	li a7,64
	ecall
    ret

_print_Array_Int: #Argunmentos: t0=ptr Array, #Hacer push t0,t1,t2,t3 
	la a0, msgCorcheteAbre
	lb a0, 0(a0)
	li a7,11
	ecall

	lw t1,0(t0) #Tamano array
	
	addi t2,x0,1 #iterador

_print_Array_Int_Ciclo:
	
	blt t1,t2, _print_Array_Int_Final
	
	addi a0,x0,4
	
	mul a0,a0,t2
	
	
	
	add a0,a0,t0
	
	lw a0,0(a0)
	
	li a7,1
	ecall
	
	
	addi t2,t2,1
	
	la a0, msgComa
	lb a0, 0(a0)
	li a7,11
	ecall
	
	j _print_Array_Int_Ciclo
	
_print_Array_Int_Final:

	la a0, msgCorcheteCierra
	lb a0, 0(a0)
	li a7,11
	ecall
	ret 

_print_Array_Char: #Argunmentos: t0=ptr Array, #Hacer push t0,t1,t2,t3 
	la a0, msgCorcheteAbre
	lb a0, 0(a0)
	li a7,11
	ecall

	lw t1,0(t0) #Tamano array
	
	addi t2,x0,1 #iterador

_print_Array_Char_Ciclo:
	
	blt t1,t2, _print_Array_Char_Final
	
	addi a0,x0,1
	
	mul a0,a0,t2
	
	
	
	add a0,a0,t0
	
	lb a0,0(a0)
	
	li a7,11
	ecall
	
	
	addi t2,t2,1
	
	la a0, msgComa
	lb a0, 0(a0)
	li a7,11
	ecall
	
	j _print_Array_Char_Ciclo
	
_print_Array_Char_Final:

	la a0, msgCorcheteCierra
	lb a0, 0(a0)
	li a7,11
	ecall
	ret 
	
_print_Array_Bool: #Argunmentos: t0=ptr Array, #Hacer push t0,t1,t2,t3 
	la a0, msgCorcheteAbre
	lb a0, 0(a0)
	li a7,11
	ecall

	lw t1,0(t0) #Tamano array
	
	addi t2,x0,1 #iterador

_print_Array_Bool_Ciclo:
	
	blt t1,t2, _print_Array_Bool_Final
	
	addi a0,x0,1
	
	mul a0,a0,t2
	
	
	
	add a0,a0,t0
	
	lb a0,0(a0)
	
	bnez a0, _print_Array_Bool_true
	
	addi sp,sp,-4
	sw ra,0(sp)
	call _print_false
	lw ra,0(sp)
	addi sp,sp,4
	j _print_Array_Bool_continue
	
	
_print_Array_Bool_true:
	
	addi sp,sp,-4
	sw ra,0(sp)
	call _print_true
	lw ra,0(sp)
	addi sp,sp,4
	
	#li a7,1
	#ecall
	
_print_Array_Bool_continue:

	addi t2,t2,1
	
	la a0, msgComa
	lb a0, 0(a0)
	li a7,11
	ecall
	
	j _print_Array_Bool_Ciclo
	
_print_Array_Bool_Final:

	la a0, msgCorcheteCierra
	lb a0, 0(a0)
	li a7,11
	ecall
	ret
    '''
