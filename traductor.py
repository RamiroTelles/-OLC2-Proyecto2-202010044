from expresiones import *
from instrucciones import *
from simbolos import *
from tipos import TIPOS_P,TIPOS_Simbolos
from errores import error
from display import display
import copy

listaErrores =[]
PilaDisplay =[]


TSReporte = TablaSimbolos()

def ejec_instrucciones(instrucciones,TS,save=True):
    
    for inst in instrucciones:
        if save:

            if isinstance(inst,Imprimir): ejec_Imprimir(inst,TS)
            elif isinstance(inst,DeclaracionExplicita): ejec_declaracion_explicita(inst,TS)
            elif isinstance(inst,DeclaracionImplicita): ejec_declaracion_implicita(inst,TS)
            elif isinstance(inst,Asignacion): ejec_Asignacion(inst,TS)
            elif isinstance(inst,AsignacionArray): ejec_AsignacionArray(inst,TS)
            #elif isinstance(inst,AsignacionMatriz): ejec_AsignacionMatriz(inst,TS)
            elif isinstance(inst,funcionPush): ejec_FuncionPush(inst,TS)
            elif isinstance(inst,controlFlujo): #ejec_controlFlujo(inst,TS)
                #tupla=ejec_controlFlujo(inst,TS)
                
                #if tupla!=None:
                    #return tupla
                    #pass
                ejec_controlFlujo(inst,TS)
            elif isinstance(inst,guardar_func): ejec_Guardar_Func(inst,TS)
                
        else:
            if isinstance(inst,guardar_func): ejec_Guardar_Func(inst,TS)
        #else: print('Error: instruccion no valida')
        

def ejec_Imprimir(inst,TS):
    
    
    for exp in inst.lista:

        #print('>> ', ejec_expresion(exp,TS))
        result,tipo = ejec_expresion(exp,TS)
        

        if isinstance(exp,ExpresionArray):

            if tipo ==TIPOS_P.ARRAY_INT:

                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Int
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
            elif tipo ==TIPOS_P.ARRAY_CHAR:

                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Char
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
                
            elif tipo ==TIPOS_P.ARRAY_BOOLEAN:

                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Bool
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
            #Print Array int
	
	# addi sp,sp,-4
	# sw ra,0(sp)
	# addi sp,sp,-16
	# sw t0, 0(sp)
	# sw t1,4(sp)
	# sw t2, 8(sp)
	# sw t3,12(sp)
	
	# la t0, Arr2
	# lw t0, Arr2
	
	# call _print_Array_Int
	# lw t0,0(sp)
	# lw t1,4(sp)
	# lw t2,8(sp)
	# lw t3,12(sp)
	# addi sp,sp,16
	# lw ra,0(sp)
	# addi sp,sp,4
	
        elif isinstance(exp, ExpresionDobleComilla) :
            TS.inst += f'''la a1, {result}
                            la a0, {result}len
                            lw a2, 0(a0)
                            li a0, 1 
                            li a7, 64 
                            ecall\n'''
        elif isinstance(exp,ExpresionComillaSimple):
            TS.inst += f''' la a0, BufferChar
                            sb {result}, 0(a0)
                            la a1, BufferChar
                            li a2, 1
                            li a0, 1 
                            li a7, 64 
                            ecall\n'''
        elif isinstance(exp,ExpresionAritmetica):
            TS.inst += f''' add a0, {result},x0
                            li a7, 1 
                            ecall\n'''
        elif isinstance(exp,ExpresionRelacional):
            label1 = TS.getNextLabel()
            label2= TS.getNextLabel()
            TS.inst += f''' beqz {result},L{label1}
                            addi sp,sp,-4
	                        sw ra, 0(sp)
                            jal _print_true
                            lw ra,0(sp)
	                        addi sp,sp,4
                            j L{label2}
                        L{label1}:
                            addi sp,sp,-4
	                        sw ra, 0(sp)
                            jal _print_false
                            lw ra,0(sp)
	                        addi sp,sp,4
                        L{label2}:\n'''
        elif isinstance(exp,ExpresionBoleana):
            label1 = TS.getNextLabel()
            label2= TS.getNextLabel()
            TS.inst += f''' beqz {result},L{label1}
                            addi sp,sp,-4
	                        sw ra, 0(sp)
                            jal _print_true
                            lw ra,0(sp)
	                        addi sp,sp,4
                            j L{label2}
                        L{label1}:
                            addi sp,sp,-4
	                        sw ra, 0(sp)
                            jal _print_false
                            lw ra,0(sp)
	                        addi sp,sp,4
                        L{label2}:\n'''
        elif isinstance(exp,ExpresionID):
            if tipo==TIPOS_P.ENTERO:
                TS.inst += f''' add a0, {result},x0
                            li a7, 1 
                            ecall\n'''
            elif tipo==TIPOS_P.CHAR:
                TS.inst += f''' la a0, BufferChar
                            sb {result}, 0(a0)
                            la a1, BufferChar
                            li a2, 1
                            li a0, 1 
                            li a7, 64 
                            ecall\n'''
            elif tipo==TIPOS_P.BOOLEAN:
                label1 = TS.getNextLabel()
                label2= TS.getNextLabel()
                TS.inst += f''' beqz {result},L{label1}
                                addi sp,sp,-4
	                            sw ra, 0(sp)
                                jal _print_true
                                lw ra,0(sp)
	                            addi sp,sp,4
                                j L{label2}
                            L{label1}:
                                addi sp,sp,-4
	                            sw ra, 0(sp)
                                jal _print_false
                                lw ra,0(sp)
	                            addi sp,sp,4
                            L{label2}:\n'''
            elif tipo==TIPOS_P.ARRAY_INT:
                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Int
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
            elif tipo==TIPOS_P.ARRAY_CHAR:
                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Char
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
            elif tipo==TIPOS_P.ARRAY_STRING:
                pass
            elif tipo==TIPOS_P.ARRAY_BOOLEAN:
                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Bool
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
                
        elif isinstance(exp,call_func):
            if tipo==TIPOS_P.ENTERO:
                TS.inst += f''' add a0, {result},x0
                            li a7, 1 
                            ecall\n'''
            elif tipo==TIPOS_P.CHAR:
                TS.inst += f''' la a0, BufferChar
                            sb {result}, 0(a0)
                            la a1, BufferChar
                            li a2, 1
                            li a0, 1 
                            li a7, 64 
                            ecall\n'''
            elif tipo==TIPOS_P.BOOLEAN:
                label1 = TS.getNextLabel()
                label2= TS.getNextLabel()
                TS.inst += f''' beqz {result},L{label1}
                                addi sp,sp,-4
	                            sw ra, 0(sp)
                                jal _print_true
                                lw ra,0(sp)
	                            addi sp,sp,4
                                j L{label2}
                            L{label1}:
                                addi sp,sp,-4
	                            sw ra, 0(sp)
                                jal _print_false
                                lw ra,0(sp)
	                            addi sp,sp,4
                            L{label2}:\n'''
            elif tipo==TIPOS_P.ARRAY_INT:
                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Int
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
            elif tipo==TIPOS_P.ARRAY_CHAR:
                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Char
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
            elif tipo==TIPOS_P.ARRAY_STRING:
                pass
            elif tipo==TIPOS_P.ARRAY_BOOLEAN:
                TS.inst+= f'''   addi sp,sp,-4
                                sw ra,0(sp)
                                addi sp,sp,-16
                                sw t0, 0(sp)
                                sw t1,4(sp)
                                sw t2, 8(sp)
                                sw t3,12(sp)
                                
                                add t0,x0,{result}
                                call _print_Array_Bool
                                lw t0,0(sp)
                                lw t1,4(sp)
                                lw t2,8(sp)
                                lw t3,12(sp)
                                addi sp,sp,16
                                lw ra,0(sp)
                                addi sp,sp,4\n'''
        
        #Luego Escribe salto de linea
    TS.inst  += f'''la a1, msgSalto
                    li a2,1
                    li a0,1
                    li a7,64
                    ecall\n'''
            
        # elif isinstance(inst.cad, ExpresionID):
        #     temporal = ts.generateTemporal()
        #     ts.salida += f'''la t{temporal}, {exp}
        #                     lw a0, 0(t{temporal})
        #                     li a7, 1
        #                     ecall\n'''
        # elif isinstance(inst.cad, ExpresionEntero):
        #     ts.salida += f'''la a0, {exp}
        #                     li a7, 1
        #                     ecall\n'''
    
    

def ejec_expresion(exp,TS):
    if isinstance(exp,ExpresionAritmetica):
        return resolver_expresionAritmetica(exp,TS)
    elif isinstance(exp,ExpresionRelacional):
        return resolver_expresionRelacional(exp,TS)
    elif isinstance(exp,ExpresionDobleComilla):
        msg = TS.getNextMsg()
        cadena = exp.cad[1:len(exp.cad)-1]
        TS.Datos+= f'msg{msg}len: .word {len(cadena)}\n'
        TS.Datos+= f'msg{msg}: .asciz "{cadena}"\n'

        return f'msg{msg}' , TIPOS_P.CADENA
    elif isinstance(exp,ExpresionComillaSimple):
        temp = TS.getNextTemp(0)
        
        TS.inst += f'addi {temp}, x0, {ord(exp.cad[1:len(exp.cad)-1])}\n'

        return temp, TIPOS_P.CHAR

        #return exp.cad[1:len(exp.cad)-1]
    elif isinstance(exp,ExpresionBoleana):
        return resolver_expresionBoleana(exp,TS)
    elif isinstance(exp,ExpresionTernaria):
        return resolver_expresionTernaria(exp,TS)
    elif isinstance(exp,ExpresionID):
        
        return resolver_expresionId(exp,TS)
    elif isinstance(exp,call_func):
        return ejec_Funcion_exp(exp,TS)
       
    elif isinstance(exp,ExpresionArray):
        return resolver_expresionArray(exp,TS)
    elif isinstance(exp,Expresion_AccesoArray):
        return resolver_expresion_AccesoArray(exp,TS)
    elif isinstance(exp,Expresion_AccesoMatriz):
        return resolver_expresion_AccesoMatriz(exp,TS)
    elif isinstance(exp,funcionPush):
        return ejec_FuncionPush(exp,TS)
    elif isinstance(exp,funcionPop):
        return ejec_FuncionPop(exp,TS)
    elif isinstance(exp,funcionIndexOf):
        return ejec_FuncionIndexOf(exp,TS)
    elif isinstance(exp,funcionJoin):
        return ejec_FuncionJoin(exp,TS)
    elif isinstance(exp,funcionLength):
        return ejec_FuncionLength(exp,TS)
    elif isinstance(exp,funcionParseInt):
        return ejec_FuncionParseInt(exp,TS)
    elif isinstance(exp,funcionParseFloat):
        return ejec_FuncionParseFloat(exp,TS)
    elif isinstance(exp,funcionToString):
        return ejec_FuncionToString(exp,TS)
    elif isinstance(exp,funcionToLowerCase):
        return ejec_FuncionToLowerCase(exp,TS)
    elif isinstance(exp,funcionToUpperCase):
        return ejec_FuncionToUpperCase(exp,TS)
    elif isinstance(exp,funcionTypeOf):
        return ejec_FuncionTypeOf(exp,TS)


    elif isinstance(exp,ExpresionNull):
        return None , TIPOS_P.VOID
    else :
        return None , TIPOS_P.VOID
    
 

def resolver_expresionAritmetica(expNum,TS):
    if isinstance(expNum,ExpresionBinaria):
        exp1,tipo1 = ejec_expresion(expNum.exp1,TS)
        exp2,tipo2 = ejec_expresion(expNum.exp2,TS)

        if tipo1 == TIPOS_P.ENTERO and tipo2 == TIPOS_P.ENTERO:
            #Numeros o Caracteres o bool
            if expNum.operador == OPERACION_ARITMETICA.MAS : 
                temp= TS.getNextTemp(2)
                TS.inst += f'add {temp},{exp1},{exp2}\n'
                return temp , TIPOS_P.ENTERO
            if expNum.operador == OPERACION_ARITMETICA.MENOS : 
                temp= TS.getNextTemp(2)
                TS.inst += f'sub {temp},{exp1},{exp2}\n'
                return temp , TIPOS_P.ENTERO
            if expNum.operador == OPERACION_ARITMETICA.POR : 
                temp= TS.getNextTemp(2)
                TS.inst += f'mul {temp},{exp1},{exp2}\n'
                return temp , TIPOS_P.ENTERO
            if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                temp= TS.getNextTemp(2)
                TS.inst += f'beqz {exp2}, err_divisionZero\n'
                TS.inst += f'div {temp},{exp1},{exp2}\n'
                
                return temp , TIPOS_P.ENTERO
            if expNum.operador == OPERACION_ARITMETICA.MODULO : 
                temp= TS.getNextTemp(2)
                TS.inst += f'beqz {exp2}, err_divisionZero\n'
                TS.inst += f'rem {temp},{exp1},{exp2}\n'
                return temp , TIPOS_P.ENTERO
        else:
            listaErrores.append(error("Tipos no combatibles "+str(tipo1)+str(tipo2),0,0,"Semantico"))
            print("Tipos no combatibles "+str(tipo1)+str(tipo2))
            
            
    elif isinstance(expNum,ExpresionNegativa):
        exp1,tipo = resolver_expresionAritmetica(expNum.exp1,TS)
        temp= TS.getNextTemp(1)
        
        TS.inst += f'sub {temp},x0,{exp1}\n'
       
        return temp,tipo
        
    elif isinstance(expNum,ExpresionEntero):
        
        temp = TS.getNextTemp(0)
        
        TS.inst += f'addi {temp}, x0, {expNum.exp1}\n'

        return temp, TIPOS_P.ENTERO
        
    elif isinstance(expNum,ExpresionDecimal):
        return expNum.exp1
    

def resolver_expresionRelacional(exp,TS):
    if isinstance(exp,ExpresionRelacional):
        exp1,tipo1 = ejec_expresion(exp.exp1,TS)
        exp2,tipo2 = ejec_expresion(exp.exp2,TS)

        if tipo1==tipo2:

            if tipo1!=TIPOS_P.ENTERO and tipo1!=TIPOS_P.FLOAT:
                if exp.operador == OPERACION_REL.IGUAL :
                    label= f'L{TS.getNextLabel()}'
                    TS.inst += f'addi a0,x0,1\n'
                    TS.inst += f'beq {exp1},{exp2},{label}\n'
                    TS.inst += f'addi a0,x0,0\n'
                    TS.inst += f'{label}:\n'
                    temp = TS.getNextTemp(2)
                    TS.inst += f'add {temp},a0,x0\n'
                    
                    return temp , TIPOS_P.BOOLEAN
                elif exp.operador == OPERACION_REL.NO_IGUAL :
                    label= f'L{TS.getNextLabel()}'
                    TS.inst += f'addi a0,x0,1\n'
                    TS.inst += f'bne {exp1},{exp2},{label}\n'
                    TS.inst += f'addi a0,x0,0\n'
                    TS.inst += f'{label}:\n'
                    temp = TS.getNextTemp(2)
                    TS.inst += f'add {temp},a0,x0\n'
                    
                    return temp , TIPOS_P.BOOLEAN
            else:

                if exp.operador == OPERACION_REL.MAYOR_QUE : 
                    
                    label= f'L{TS.getNextLabel()}'
                    TS.inst += f'addi a0,x0,1\n'
                    TS.inst += f'bgt {exp1},{exp2},{label}\n'
                    TS.inst += f'addi a0,x0,0\n'
                    TS.inst += f'{label}:\n'
                    temp = TS.getNextTemp(2)
                    TS.inst += f'add {temp},a0,x0\n'
                    
                    return temp , TIPOS_P.BOOLEAN
                elif exp.operador == OPERACION_REL.MENOR_QUE :
                    label= f'L{TS.getNextLabel()}'
                    TS.inst += f'addi a0,x0,1\n'
                    TS.inst += f'blt {exp1},{exp2},{label}\n'
                    TS.inst += f'addi a0,x0,0\n'
                    TS.inst += f'{label}:\n'
                    temp = TS.getNextTemp(2)
                    TS.inst += f'add {temp},a0,x0\n'
                    
                    return temp , TIPOS_P.BOOLEAN
                elif exp.operador == OPERACION_REL.MAYORIGUAL :
                    label= f'L{TS.getNextLabel()}'
                    TS.inst += f'addi a0,x0,1\n'
                    TS.inst += f'bge {exp1},{exp2},{label}\n'
                    TS.inst += f'addi a0,x0,0\n'
                    TS.inst += f'{label}:\n'
                    temp = TS.getNextTemp(2)
                    TS.inst += f'add {temp},a0,x0\n'
                    
                    return temp , TIPOS_P.BOOLEAN
                elif exp.operador == OPERACION_REL.MENORIGUAL :
                    label= f'L{TS.getNextLabel()}'
                    TS.inst += f'addi a0,x0,1\n'
                    TS.inst += f'ble {exp1},{exp2},{label}\n'
                    TS.inst += f'addi a0,x0,0\n'
                    TS.inst += f'{label}:\n'
                    temp = TS.getNextTemp(2)
                    TS.inst += f'add {temp},a0,x0\n'
                    
                    return temp , TIPOS_P.BOOLEAN
                elif exp.operador == OPERACION_REL.IGUAL :
                    label= f'L{TS.getNextLabel()}'
                    TS.inst += f'addi a0,x0,1\n'
                    TS.inst += f'beq {exp1},{exp2},{label}\n'
                    TS.inst += f'addi a0,x0,0\n'
                    TS.inst += f'{label}:\n'
                    temp = TS.getNextTemp(2)
                    TS.inst += f'add {temp},a0,x0\n'
                    
                    return temp , TIPOS_P.BOOLEAN
                elif exp.operador == OPERACION_REL.NO_IGUAL :
                    label= f'L{TS.getNextLabel()}'
                    TS.inst += f'addi a0,x0,1\n'
                    TS.inst += f'bne {exp1},{exp2},{label}\n'
                    TS.inst += f'addi a0,x0,0\n'
                    TS.inst += f'{label}:\n'
                    temp = TS.getNextTemp(2)
                    TS.inst += f'add {temp},a0,x0\n'
                    
                    return temp , TIPOS_P.BOOLEAN
        else:
            listaErrores.append(error("Tipos no combatibles "+str(tipo1)+str(tipo2),0,0,"Semantico"))
            print("Tipos no combatibles "+str(tipo1)+str(tipo2))
    
def resolver_expresionBoleana(expBol,TS):
    if isinstance(expBol,ExpresionLogica):
        exp1,tipo1 = ejec_expresion(expBol.exp1,TS)
        exp2,tipo2 = ejec_expresion(expBol.exp2,TS)

        if tipo1 == TIPOS_P.BOOLEAN and tipo2 == TIPOS_P.BOOLEAN:


            if expBol.operador == OPERACION_LOGICA.AND :
                temp= TS.getNextTemp(2)
                TS.inst += f'and {temp},{exp1},{exp2}\n'
                return temp , TIPOS_P.BOOLEAN

            if expBol.operador == OPERACION_LOGICA.OR :
                temp= TS.getNextTemp(2)
                TS.inst += f'or {temp},{exp1},{exp2}\n'
                return temp , TIPOS_P.BOOLEAN
        else:
            listaErrores.append(error("Tipos no combatibles "+str(tipo1)+str(tipo2),0,0,"Semantico"))
            print("Tipos no combatibles "+str(tipo1)+str(tipo2))
    elif isinstance(expBol,ExpresionNot):

        exp1,tipo = ejec_expresion(expBol.exp1,TS)
        temp= TS.getNextTemp(1)
        
        TS.inst += f'not {temp},{exp1}\n'
        TS.inst += f'addi a0,x0,1\n'
        TS.inst += f'and {temp},{temp},a0\n'
       
        return temp,TIPOS_P.BOOLEAN
        #return not ejec_expresion(expBol.exp1,TS)
    elif isinstance(expBol,Expresion_True_False):
        if expBol.exp1 == "true": 
            temp = TS.getNextTemp(0)
        
            TS.inst += f'addi {temp}, x0, 1\n'

            return temp, TIPOS_P.BOOLEAN
            
        if expBol.exp1 == "false" :
            temp = TS.getNextTemp(0)
        
            TS.inst += f'addi {temp}, x0, 0\n'

            return temp, TIPOS_P.BOOLEAN

def resolver_expresionTernaria(expTer,TS):
    if ejec_expresion(expTer.exp1,TS):
        return ejec_expresion(expTer.exp2,TS)
    return ejec_expresion(expTer.exp3,TS)

def resolver_expresionId(expId,TS):
    exp_id =  TS.obtener(expId.id)
    if exp_id== None:
        listaErrores.append(error("Se quiere usar valor null con variable "+expId.id,0,0,"Semantico"))
        print("Se quiere usar valor null con variable "+expId.id)
        return
    
    
    
    #if TS.ambito=="Local":
    if exp_id.ambito=="Local":


        if exp_id.tipo_simbolo== TIPOS_Simbolos.ARRAY:
            
            temp = TS.getNextTemp(0)
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - exp_id.RA 

            TS.inst += f'lw {temp}, {offset}(sp)\n'
#       lw t0, 0(sp) # obtener var +8
        elif exp_id.tipo== TIPOS_P.ENTERO:
            
            temp = TS.getNextTemp(0)
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - exp_id.RA 

            TS.inst += f'lw {temp}, {offset}(sp)\n'
        elif exp_id.tipo == TIPOS_P.BOOLEAN:
            
            temp = TS.getNextTemp(0)
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - exp_id.RA 

            TS.inst += f'lb {temp}, {offset}(sp)\n'
        elif exp_id.tipo == TIPOS_P.CHAR:
            
            temp = TS.getNextTemp(0)
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - exp_id.RA 

            TS.inst += f'lb {temp}, {offset}(sp)\n'
        elif exp_id.tipo== TIPOS_P.CADENA:
            
            temp = TS.getNextTemp(0)
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - exp_id.RA 

            TS.inst += f'lw {temp}, {offset}(sp)\n'
    else:

        if exp_id.tipo_simbolo== TIPOS_Simbolos.ARRAY:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp}, {expId.id}\n'
            TS.inst += f'lw {temp}, 0({temp})\n'
        elif exp_id.tipo== TIPOS_P.ENTERO:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp}, {expId.id}\n'
            TS.inst += f'lw {temp}, 0({temp})\n'
        elif exp_id.tipo == TIPOS_P.BOOLEAN:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp}, {expId.id}\n'
            TS.inst += f'lb {temp}, 0({temp})\n'
        elif exp_id.tipo == TIPOS_P.CHAR:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp}, {expId.id}\n'
            TS.inst += f'lb {temp}, 0({temp})\n'

        elif exp_id.tipo== TIPOS_P.CADENA:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp}, {expId.id}\n'
            TS.inst += f'lw {temp}, 0({temp})\n'
    
    
    
#    temp = TS.getNextTemp(0)
#    TS.inst += f'la {temp}, {expId.id}\n'
#    TS.inst += f'lw {temp}, 0({temp})\n'
    return temp, exp_id.tipo


def ejec_declaracion_explicita(inst,TS):
    cont=1
    exp,tipo = ejec_expresion(inst.valor,TS)

   


    if TS.obtener(inst.id)!=None:
        print("Ya declarada variable "+inst.id)
        listaErrores.append(error("Ya declarada variable "+inst.id,0,0,"Semantico"))
        #return
    
    if inst.arrayList!=0:
        if inst.tipo == TIPOS_P.ENTERO:
            inst.tipo = TIPOS_P.ARRAY_INT
        elif inst.tipo == TIPOS_P.CADENA:
            inst.tipo = TIPOS_P.ARRAY_STRING
        elif inst.tipo == TIPOS_P.CHAR:
            inst.tipo = TIPOS_P.ARRAY_CHAR
        elif inst.tipo == TIPOS_P.BOOLEAN:
            inst.tipo = TIPOS_P.ARRAY_BOOLEAN
 
    if inst.tipo != tipo and exp!=None:
        print("Asignacion equivocada de tipos "+inst.id)
        listaErrores.append(error("Asignacion equivocada de tipos "+inst.id,0,0,"Semantico"))
        #aqui se pondria que se asigna null
        return
    
    if len(PilaDisplay)!=0:
        RA_var = PilaDisplay[len(PilaDisplay)-1].RA

        if inst.arrayList!=0:
            PilaDisplay[len(PilaDisplay)-1].RA+=4
        elif tipo== TIPOS_P.ENTERO:
            PilaDisplay[len(PilaDisplay)-1].RA+=4
        elif inst.tipo == TIPOS_P.BOOLEAN:
            PilaDisplay[len(PilaDisplay)-1].RA+=1
        elif inst.tipo == TIPOS_P.CHAR:
            PilaDisplay[len(PilaDisplay)-1].RA+=1
        elif inst.tipo == TIPOS_P.CADENA:
            PilaDisplay[len(PilaDisplay)-1].RA+=4


    else:
        RA_var =0

    if tipo==None and inst.arrayList!=0:
        if inst.tipo==TIPOS_P.ENTERO:
            tipo = TIPOS_P.ARRAY_INT
        elif inst.tipo==TIPOS_P.CADENA:
            tipo = TIPOS_P.ARRAY_STRING
        elif inst.tipo==TIPOS_P.CHAR:
            tipo = TIPOS_P.ARRAY_CHAR
        elif inst.tipo==TIPOS_P.BOOLEAN:
            tipo = TIPOS_P.ARRAY_BOOLEAN  
    else:
        tipo = inst.tipo

    if inst.const == True:
        if exp==None:
            print("No asigno valor a const "+inst.id)
            listaErrores.append(error("No asigno valor a const "+inst.id,0,0,"Semantico"))
            return
        else:
            simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.CONSTANTE,tipo=tipo,valor=exp,ambito=TS.ambito,RA=RA_var,linea=inst.linea,columna=inst.columna)
    elif inst.arrayList!=0:
        simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.ARRAY,tipo=tipo,valor=exp,ambito=TS.ambito,RA=RA_var,linea=inst.linea,columna=inst.columna)
    else:
        simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.VARIABLE,tipo=tipo,valor=exp,ambito=TS.ambito,RA=RA_var,linea=inst.linea,columna=inst.columna)
        
    TS.agregar(simbolo)
    if TS.ambito=="Local":
        # addi sp,sp,-4 #creacion var
        # addi t1,x0,0
        # sw t1,0(sp)

        if inst.arrayList!=0:
            TS.inst+= f'addi sp,sp,-4\n'
           
            TS.inst+= f'sw x0,0(sp)\n'
            if exp!=None:
               TS.inst+= f'sw {exp},0(sp)\n'

        elif inst.tipo== TIPOS_P.ENTERO:
          
           TS.inst+= f'addi sp,sp,-4\n'
           
           TS.inst+= f'sw x0,0(sp)\n'
           if exp!=None:
               TS.inst+= f'sw {exp},0(sp)\n'
           
        elif inst.tipo == TIPOS_P.BOOLEAN:
            TS.inst+= f'addi sp,sp,-1\n'
            TS.inst+= f'addi a0,x0,1\n'
            TS.inst+= f'sb a0,0(sp)\n'
            if exp!=None:
                TS.inst+= f'sb {exp},0(sp)\n'
        elif inst.tipo == TIPOS_P.CHAR:
            TS.inst+= f'addi sp,sp,-1\n'
            
            TS.inst+= f'sb x0,0(sp)\n'
            if exp!=None:
                TS.inst+= f'sb {exp},0(sp)\n'
        elif inst.tipo == TIPOS_P.CADENA:
            TS.inst+= f'addi sp,sp,-4\n'
           
            TS.inst+= f'sw x0,0(sp)\n'
            if exp!=None:
               TS.inst+= f'sw {exp},0(sp)\n'
        TS.restoreTemp(cont)
    else:

        if inst.arrayList!=0:
            TS.Datos += f'{inst.id}: .word 0\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sw {exp},0({temp})\n'

        elif inst.tipo == TIPOS_P.ENTERO:
            TS.Datos += f'{inst.id}: .word 0\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sw {exp},0({temp})\n'
        elif inst.tipo == TIPOS_P.BOOLEAN:
            TS.Datos += f'{inst.id}: .byte 1\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sb {exp},0({temp})\n'
        elif inst.tipo == TIPOS_P.CHAR:
            TS.Datos += f'{inst.id}: .byte 0\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sb {exp},0({temp})\n'
        elif inst.tipo == TIPOS_P.CADENA:
            TS.Datos += f'{inst.id}: .word 0\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sw {exp},0({temp})\n'
       
    
        TS.restoreTemp(cont)
 #   TSReporte.agregar(copy.deepcopy(simbolo))

def ejec_declaracion_implicita(inst,TS):
    cont=1
    exp,tipo = ejec_expresion(inst.valor,TS)
    if TS.obtener(inst.id)!=None:
        print("Ya declarada variable "+inst.id)
        listaErrores.append(error("Ya declarada variable "+inst.id,0,0,"Semantico"))
        return
    
    if len(PilaDisplay)!=0:
        RA_var = PilaDisplay[len(PilaDisplay)-1].RA
        if tipo== TIPOS_P.ARRAY_INT:
            PilaDisplay[len(PilaDisplay)-1].RA+=4
        elif tipo== TIPOS_P.ARRAY_CHAR:
            PilaDisplay[len(PilaDisplay)-1].RA+=4
        elif tipo== TIPOS_P.ARRAY_BOOLEAN:
            PilaDisplay[len(PilaDisplay)-1].RA+=4
        elif tipo== TIPOS_P.ARRAY_STRING:
            PilaDisplay[len(PilaDisplay)-1].RA+=4
        elif tipo== TIPOS_P.ENTERO:
            PilaDisplay[len(PilaDisplay)-1].RA+=4
        elif tipo == TIPOS_P.BOOLEAN:
            PilaDisplay[len(PilaDisplay)-1].RA+=1
        elif tipo == TIPOS_P.CHAR:
            PilaDisplay[len(PilaDisplay)-1].RA+=1
        elif tipo == TIPOS_P.CADENA:
            PilaDisplay[len(PilaDisplay)-1].RA+=4
    else:
        RA_var =0

    if tipo==TIPOS_P.ARRAY_STRING or tipo==TIPOS_P.ARRAY_INT or tipo==TIPOS_P.ARRAY_CHAR or tipo==TIPOS_P.ARRAY_BOOLEAN:
        tipoSimbolo = TIPOS_Simbolos.ARRAY
    else:
        tipoSimbolo = TIPOS_Simbolos.VARIABLE
    if inst.const == True:
        if exp==None:
            print("No asigno valor a const "+inst.id)
            listaErrores.append(error("No asigno valor a const "+inst.id,0,0,"Semantico"))
            return
        else:
            simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.CONSTANTE,tipo=tipo,valor=exp,ambito=TS.ambito,RA=RA_var,linea=inst.linea,columna=inst.columna)
        
    else:

        simbolo = Simbolos(id=inst.id,tipo_simbolo=tipoSimbolo,tipo=tipo,valor=exp,ambito=TS.ambito,RA=RA_var,linea=inst.linea,columna=inst.columna)


    TS.agregar(simbolo)

    if TS.ambito=="Local":
        # addi sp,sp,-4 #creacion var
        # addi t1,x0,0
        # sw t1,0(sp)
        if tipoSimbolo==TIPOS_Simbolos.ARRAY:
            TS.inst+= f'addi sp,sp,-4\n'
           
            TS.inst+= f'sw x0,0(sp)\n'
            if exp!=None:
               TS.inst+= f'sw {exp},0(sp)\n'

        elif tipo== TIPOS_P.ENTERO:
          
           TS.inst+= f'addi sp,sp,-4\n'
           
           TS.inst+= f'sw x0,0(sp)\n'
           if exp!=None:
               TS.inst+= f'sw {exp},0(sp)\n'
           
        elif tipo == TIPOS_P.BOOLEAN:
            TS.inst+= f'addi sp,sp,-1\n'
            TS.inst+= f'addi a0,x0,1\n'
            TS.inst+= f'sb a0,0(sp)\n'
            if exp!=None:
                TS.inst+= f'sb {exp},0(sp)\n'
        elif tipo == TIPOS_P.CHAR:
            TS.inst+= f'addi sp,sp,-1\n'
            
            TS.inst+= f'sb x0,0(sp)\n'
            if exp!=None:
                TS.inst+= f'sb {exp},0(sp)\n'
        elif tipoSimbolo==TIPOS_P.CADENA:
            TS.inst+= f'addi sp,sp,-4\n'
           
            TS.inst+= f'sw x0,0(sp)\n'
            if exp!=None:
               TS.inst+= f'sw {exp},0(sp)\n'
        TS.restoreTemp(cont)
    else:

        if tipoSimbolo==TIPOS_Simbolos.ARRAY:
            TS.Datos += f'{inst.id}: .word 0\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sw {exp},0({temp})\n'

        elif tipo== TIPOS_P.ENTERO:
            TS.Datos += f'{inst.id}: .word 0\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sw {exp},0({temp})\n'
        elif tipo == TIPOS_P.BOOLEAN:
            TS.Datos += f'{inst.id}: .byte 1\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sb {exp},0({temp})\n'
        elif tipo == TIPOS_P.CHAR:
            TS.Datos += f'{inst.id}: .byte 0\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sb {exp},0({temp})\n'
        elif tipo == TIPOS_P.CADENA:
            TS.Datos += f'{inst.id}: .word 0\n'
            if exp!= None:
                cont+=1
                temp = TS.getNextTemp(0)
                TS.inst += f'la {temp},{inst.id}\n'
                TS.inst += f'sw {exp},0({temp})\n'
        
        TS.restoreTemp(cont)
    
    #TSReporte.agregar(copy.deepcopy(simbolo))

def ejec_Asignacion(inst,TS):
    
    exp,tipo = ejec_expresion(inst.valor,TS)
    simbolo = TS.obtener(inst.id)
    
    if simbolo== None:
        print("No se encontro variable "+inst.id)
        listaErrores.append(error("No se encontro variable "+inst.id,0,0,"Semantico"))
        return

    if simbolo.tipo_simbolo==TIPOS_Simbolos.CONSTANTE:
        print("No se puede asignar a Constante "+inst.id)
        listaErrores.append(error("No se puede asignar a Constante "+inst.id,0,0,"Semantico"))
        return

    
    if simbolo.tipo!=tipo:
        print("Error, "+inst.id+" No se puede asignar un tipo de variable diferente")
        listaErrores.append(error(inst.id+" No se puede asignar un tipo de variable diferente",0,0,"Semantico"))

    
    # temp = TS.getNextTemp(0)
    # TS.inst += f'la {temp},{inst.id}\n'
    # TS.inst += f'sw {exp},0({temp})\n'
    # TS.actualizar(inst.id,exp)

    #if TS.ambito=="Local":
    if simbolo.ambito =="Local":

#        sw t0,0(sp) # asignacion
        if tipo== TIPOS_P.ARRAY_INT or tipo== TIPOS_P.ARRAY_STRING or tipo== TIPOS_P.ARRAY_CHAR or tipo== TIPOS_P.ARRAY_BOOLEAN:
            
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - simbolo.RA
            TS.inst += f'sw {exp},{offset}(sp)\n'
        if tipo== TIPOS_P.ENTERO:
            
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - simbolo.RA
            TS.inst += f'sw {exp},{offset}(sp)\n'
        if tipo == TIPOS_P.BOOLEAN:
            
            offset = PilaDisplay[len(PilaDisplay)-1].RA -1 - simbolo.RA
            TS.inst += f'sw {exp},{offset}(sp)\n'
        if tipo == TIPOS_P.CHAR:
            
            offset = PilaDisplay[len(PilaDisplay)-1].RA -1 - simbolo.RA
            TS.inst += f'sw {exp},{offset}(sp)\n'
        
        TS.restoreTemp(1)
        
    else:
        if tipo== TIPOS_P.ARRAY_INT or tipo== TIPOS_P.ARRAY_STRING or tipo== TIPOS_P.ARRAY_CHAR or tipo== TIPOS_P.ARRAY_BOOLEAN:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp},{inst.id}\n'
            TS.inst += f'sw {exp},0({temp})\n'
        elif tipo== TIPOS_P.ENTERO:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp},{inst.id}\n'
            TS.inst += f'sw {exp},0({temp})\n'
        elif tipo == TIPOS_P.BOOLEAN:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp},{inst.id}\n'
            TS.inst += f'sb {exp},0({temp})\n'
        elif tipo == TIPOS_P.CHAR:
            
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp},{inst.id}\n'
            TS.inst += f'sb {exp},0({temp})\n'
        
        TS.restoreTemp(2)
    #TSReporte.actualizar(copy.deepcopy(inst.id),copy.deepcopy(exp))


def ejec_controlFlujo(inst,TS):
    if isinstance(inst,inst_if): 
        #tupla = ejec_If(inst,TS)
        #if tupla != None:
            #return tupla
        ejec_If(inst,TS)

    elif isinstance(inst,inst_while): return ejec_While(inst,TS)
    elif isinstance(inst,inst_for): return ejec_For(inst,TS)
    elif isinstance(inst,inst_switch): return ejec_Switch(inst,TS)
    elif isinstance(inst,call_func): ejec_Funcion(inst,TS)
    elif isinstance(inst,inst_Continue): 
        if len(PilaDisplay)==0:
            print("Break no dentro de un ciclo")
            listaErrores.append(error("Break no dentro de un ciclo o switch",0,0,"Semantico"))
            return
        
        for i in range(1,len(PilaDisplay)+1):

            if PilaDisplay[len(PilaDisplay)-i].Lcontinue=="":
                continue

            TS.inst += f'j {PilaDisplay[len(PilaDisplay)-i].Lcontinue}\n'
            return
        
        
        print("Continue no dentro de un ciclo")
        listaErrores.append(error("Continue no dentro de un ciclo o switch",0,0,"Semantico"))
        
        
    elif isinstance(inst,inst_Break): 
        if len(PilaDisplay)==0:
            print("Break no dentro de un ciclo o switch")
            listaErrores.append(error("Break no dentro de un ciclo o switch",0,0,"Semantico"))
            return
        for i in range(1,len(PilaDisplay)+1):

            if PilaDisplay[len(PilaDisplay)-i].Lsalida=="":
                continue

            TS.inst += f'j {PilaDisplay[len(PilaDisplay)-i].Lsalida}\n'
            return
        
        print("Break no dentro de un ciclo o switch")
        listaErrores.append(error("Break no dentro de un ciclo o switch",0,0,"Semantico"))
        
    elif isinstance(inst,inst_Return):
        #fun_ = TS.obtener(PilaDisplay[len(PilaDisplay)-1].func)

        exp,tipo=ejec_expresion(inst.valor,TS)

        if exp==None:
            TS.inst+="ret\n"
            return

        if tipo!=PilaDisplay[len(PilaDisplay)-1].tipo:
            return


        if tipo == TIPOS_P.ENTERO:
            retorno = TS.obtener(PilaDisplay[len(PilaDisplay)-1].func+"Return")
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - retorno.RA
            
            #TS.inst+= f'addi sp,sp,-4\n'
            TS.inst+= f'sw {exp}, {offset}(sp)\n'
            TS.inst+="ret\n"
            
        elif tipo== TIPOS_P.BOOLEAN:
            retorno = TS.obtener(PilaDisplay[len(PilaDisplay)-1].func+"Return")
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - retorno.RA

            #TS.inst+= f'addi sp,sp,-1\n'
            TS.inst+= f'sb {exp}, {offset}(sp)\n'
            TS.inst+="ret\n"
            
        elif tipo== TIPOS_P.CHAR:
            retorno = TS.obtener(PilaDisplay[len(PilaDisplay)-1].func+"Return")
            offset = PilaDisplay[len(PilaDisplay)-1].RA -4 - retorno.RA

            #TS.inst+= f'addi sp,sp,-1\n'
            TS.inst+= f'sb {exp}, {offset}(sp)\n'
            TS.inst+="ret\n"
            


        #return inst,ejec_expresion(inst.valor,TS) 
    
def ejec_If(inst,TS):
    PilaDisplay.append(display("","",0))
    exp,tipo = ejec_expresion(inst.cond,TS)

    if tipo!= TIPOS_P.BOOLEAN:
        print("Expresion invalida en If")
        listaErrores.append(error("Expresion invalida en If",0,0,"Semantico"))
    Lt = f'L{TS.getNextLabel()}'
    Lf = f'L{TS.getNextLabel()}'
    Lsalida = f'L{TS.getNextLabel()}'

    TS.inst+= f'''  bnez {exp},{Lt}
                    j {Lf}
                {Lt}:\n'''
    
    ejec_instrucciones(inst.instruccionesIf,TS)

    TS.inst+= f'''  j {Lsalida}
                {Lf}:\n'''

    ejec_instrucciones(inst.instruccionesElse,TS)

    TS.inst+= f'''{Lsalida}:\n'''
    
    PilaDisplay.pop()
    
    #  	bnez t0,L1
    #     j L2
    # L1:
    #     jal _print_true
    #     j L3
    # L2:
    #     jal _print_false
    # L3:
 

def ejec_While(inst,TS):

    Linicio = f'L{TS.getNextLabel()}'
    Lsent = f'L{TS.getNextLabel()}'
    Lsalida=f'L{TS.getNextLabel()}'
    PilaDisplay.append(display(Lsalida,Linicio,0))
    TS.inst+=f'{Linicio}:\n'
    
    exp,tipo = ejec_expresion(inst.cond,TS)
    
    TS.inst+= f'''  bnez {exp},{Lsent}
                    j {Lsalida}
                {Lsent}:\n'''
    
    ejec_instrucciones(inst.instrucciones,TS)

    TS.inst+=f'j {Linicio}\n'
    TS.inst+=f'{Lsalida}:\n'
    PilaDisplay.pop()

    # while exp:
    #     TablaLocal = TablaSimbolos(simbolos=TS.simbolos.copy(),ambito=TS.ambito +"_While")

    #     tupla = ejec_instrucciones(inst.instrucciones,TablaLocal)
    #     if tupla!=None:

    #         if isinstance(tupla[0],inst_Break):
                
    #             break
    #         if isinstance(tupla[0],inst_Return):
                
    #             return tupla

    #     exp = ejec_expresion(inst.cond,TS)
        #TS.salida+= TablaLocal.salida
    
#     Linicio:
# 	la t0,i
# 	lw t0,0(t0)
# 	li t1,0
# 	bgt t0,t1,Ltrue
# 	j Lfalse
# Ltrue:
# 	la t0,i
# 	lw t0,0(t0)
# 	add a0,t0,x0
# 	li a7,1
# 	ecall
	
# 	la t0,i
# 	lw t0,0(t0)
# 	li t1,1
# 	sub t0,t0,t1
# 	la t1,i
# 	sw t0,0(t1)
# 	j Linicio
	
# Lfalse:
        
    
    

def ejec_For(inst,TS):
    
    
        
    Linicio = f'L{TS.getNextLabel()}'
    Lsent = f'L{TS.getNextLabel()}'
    Lcontinue = f'L{TS.getNextLabel()}'
    Lsalida = f'L{TS.getNextLabel()}'
    PilaDisplay.append(display(Lsalida,Lcontinue,0))
    ejec_instrucciones(inst.instruccion1,TS)

    TS.inst += f'{Linicio}:\n'
    exp,tipo = ejec_expresion(inst.cond,TS)

    TS.inst +=f'bnez {exp},{Lsent}\n'
    TS.inst +=f'j {Lsalida}\n'
    TS.inst += f'{Lsent}:\n'

    ejec_instrucciones(inst.instruccion_verdadero,TS)

    TS.inst += f'{Lcontinue}:\n'

    ejec_instrucciones(inst.instruccion2,TS)
    TS.inst +=f'j {Linicio}\n'
    TS.inst += f'{Lsalida}:\n'

    PilaDisplay.pop()
    # TablaLocal = TablaSimbolos(simbolos=TS.simbolos.copy(),ambito=TS.ambito +"_For")

  
    # ejec_instrucciones(copy.deepcopy(inst.instruccion1),TablaLocal)
    # exp= ejec_expresion(inst.cond,TablaLocal)

    # while exp:
    #     #TablaLocal2 = copy.deepcopy(TablaLocal)
    #     tupla = ejec_instrucciones(inst.instruccion_verdadero,TablaLocal)
    #     if tupla!=None:

    #         if isinstance(tupla[0],inst_Break):
                
    #             break
    #         if isinstance(tupla[0],inst_Return):
                
    #             return tupla
    #     ejec_instrucciones(inst.instruccion2,TablaLocal)
    #     #TablaLocal.actualizar(inst.instruccion2[0].id,ejec_expresion(inst.instruccion2[0].valor,TablaLocal))
    #     exp = ejec_expresion(inst.cond,TablaLocal)
    # #TS.salida+= TablaLocal.salida


#     Linicio:
# 	la t0,i
# 	lw t0,0(t0)
# 	addi t1,x0,10
# 	addi a0,x0,1
# 	blt t0,t1,Lv
# 	addi a0,x0,0
# Lv:
# 	add t0, a0,x0
# 	bnez t0,Lsent
# 	j Lsalida
# Lsent:
# 	call _print_true
	
# Lcontinue:
# 	la t0,i
# 	lw t0,0(t0)
# 	addi t0,t0,1
# 	la t1,i
# 	sw t0, 0(t1)
# 	j Linicio
# Lsalida:
        
def ejec_Switch(inst,TS):

    Ltest = f'L{TS.getNextLabel()}'
    Lsalida = f'L{TS.getNextLabel()}'
    PilaDisplay.append(display(Lsalida,"",0))
    listaLabels=[]
    labelDefault = ""
    TS.inst+= f'j {Ltest}\n'
    
    for i in range(0,len(inst.listaInst)):
        listaLabels.append(f'L{TS.getNextLabel()}')
        TS.inst+= f'{listaLabels[i]}:\n'
        ejec_instrucciones(inst.listaInst[i],TS)

    TS.inst += f'j {Lsalida}\n'
    TS.inst+= f'{Ltest}:\n'
    expId,tipoId = ejec_expresion(inst.id,TS)
    TS.inst+= f'add a1,x0,{expId}\n'
    TS.restoreTemp(1)

    for i in range(0,len(inst.listaExpresiones)):
        
        exp,tipo1 = ejec_expresion(inst.listaExpresiones[i],TS)

        if exp ==None:
            labelDefault = listaLabels[i]
            continue
        


        if tipoId != tipo1:
            print("Comparando tipos diferentes")
            listaErrores.append(error("Comparando tipos diferentes",0,0,"Semantico"))
            return
        
        TS.inst += f'beq a1,{exp},{listaLabels[i]}\n'
        TS.restoreTemp(1)
    
    if labelDefault!="":
        TS.inst += f'j {labelDefault}\n'
    TS.inst += f'{Lsalida}:\n'

    PilaDisplay.pop()
    





    # valorId = ejec_expresion(inst.id,TS)
    # posDefault=-1
    # contador=-1
    # for i in range(len(inst.listaExpresiones)):
    #     exp= ejec_expresion(inst.listaExpresiones[i],TS)
    #     if exp==None:
    #         posDefault=i
    #     elif valorId== exp:
    #         contador=i

    # TablaLocal = TablaSimbolos(simbolos=TS.simbolos.copy(),ambito=TS.ambito +"_Switch")
    # if contador!=-1:
    #     for i in range(contador,len(inst.listaInst)):
    #         tupla = ejec_instrucciones(inst.listaInst[i],TablaLocal)
            
    #         if tupla!=None:

    #             if isinstance(tupla[0],inst_Break):
                    
    #                 break
    #             if isinstance(tupla[0],inst_Return):
                    
    #                 return tupla
    # elif posDefault!=-1:
    #     for i in range(posDefault,len(inst.listaInst)):
    #         tupla = ejec_instrucciones(inst.listaInst[i],TablaLocal)
            
    #         if tupla!=None:

    #             if isinstance(tupla[0],inst_Break):
                    
    #                 break
    #             if isinstance(tupla[0],inst_Return):
                    
    #                 return tupla

    # #TS.salida+= TablaLocal.salida

#     	j test
# L1:
# 	li a0,1
# 	li a7,1
# 	ecall
# L2:
# 	li a0,2
# 	li a7,1
# 	ecall
# L3:
# 	li a0,3
# 	li a7,1
# 	ecall
# L4:
# 	li a0,4
# 	li a7,1
# 	ecall
# 	j Lsalida
# test:
# 	la t0,numero
# 	lw t0,0(t0)
# 	addi t1,x0,1
# 	beq t0,t1,L1
# 	addi t1,x0,2
# 	beq t0,t1,L2
# 	addi t1,x0,3
# 	beq t0,t1,L3
# 	j L4
# Lsalida:

def ejec_Guardar_Func(inst,TS):
    PilaDisplay.append(display("","",0,inst.id,inst.tipo))
    TS.ambito= "Local"
    sim =TS.obtener(inst.id)
    if sim!=None:
        if sim.tipo_simbolo==TIPOS_Simbolos.FUNCION:
            print("Ya declarada Funcion "+inst.id)
            listaErrores.append(error("Ya declarada Funcion "+inst.id,0,0,"Semantico"))
            return
        
    
    if inst.tipo == TIPOS_P.ENTERO:
        simboloReturn = Simbolos(inst.id+"Return",TIPOS_Simbolos.VARIABLE,inst.tipo,None,TS.ambito,RA=PilaDisplay[len(PilaDisplay)-1].RA)
        PilaDisplay[len(PilaDisplay)-1].RA+=4
        TS.agregar(simboloReturn)
    elif inst.tipo  == TIPOS_P.BOOLEAN:
        simboloReturn = Simbolos(inst.id+"Return",TIPOS_Simbolos.VARIABLE,inst.tipo,None,TS.ambito,RA=PilaDisplay[len(PilaDisplay)-1].RA)
        PilaDisplay[len(PilaDisplay)-1].RA+=1
        TS.agregar(simboloReturn)
    elif inst.tipo  == TIPOS_P.CHAR:
        simboloReturn = Simbolos(inst.id+"Return",TIPOS_Simbolos.VARIABLE,inst.tipo,None,TS.ambito,RA=PilaDisplay[len(PilaDisplay)-1].RA)
        PilaDisplay[len(PilaDisplay)-1].RA+=1
        TS.agregar(simboloReturn)

    for elem in inst.listaParametros:
        if elem.tipo == TIPOS_P.ENTERO:
            
            simbolo1 = Simbolos(elem.id,TIPOS_Simbolos.VARIABLE,elem.tipo,None,TS.ambito,RA=PilaDisplay[len(PilaDisplay)-1].RA)
            PilaDisplay[len(PilaDisplay)-1].RA+=4
            TS.agregar(simbolo1)
        elif elem.tipo == TIPOS_P.CHAR:
            simbolo1 = Simbolos(elem.id,TIPOS_Simbolos.VARIABLE,elem.tipo,None,TS.ambito,RA=PilaDisplay[len(PilaDisplay)-1].RA)
            PilaDisplay[len(PilaDisplay)-1].RA+=1
            TS.agregar(simbolo1)
        elif elem.tipo == TIPOS_P.BOOLEAN:
            simbolo1 = Simbolos(elem.id,TIPOS_Simbolos.VARIABLE,elem.tipo,None,TS.ambito,RA=PilaDisplay[len(PilaDisplay)-1].RA)
            PilaDisplay[len(PilaDisplay)-1].RA+=1
            TS.agregar(simbolo1)
        
    Lsiguiente=f'L{TS.getNextLabel()}'
    TS.inst += f'j {Lsiguiente}\n'
    TS.inst += f'{inst.id}:\n'

    fun_ = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.FUNCION,tipo=inst.tipo,valor=None,ambito=TS.ambito,parametros=inst.listaParametros,instrucciones=inst.instrucciones,RA=PilaDisplay[len(PilaDisplay)-1].RA)

    TS.agregar(fun_)

    ejec_instrucciones(inst.instrucciones,TS)
    TS.inst += 'ret\n'
    TS.inst += f'{Lsiguiente}:\n'
    
    fun_ = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.FUNCION,tipo=inst.tipo,valor=None,ambito=TS.ambito,parametros=inst.listaParametros,instrucciones=inst.instrucciones,RA=PilaDisplay[len(PilaDisplay)-1].RA)

    TS.agregar(fun_)

    PilaDisplay.pop()
    TS.ambito= "Global"
    
    #TSReporte.agregar(copy.deepcopy(simbolo))

#     j Lsiguiente
# _saludar1:
    
#     	la a1,msg0
#     	la a0,msg0len
#     	lw a2, 0(a0)
#     	li a0,1
#     	li a7,64
#     	ecall
    	
#     	ret
# Lsiguiente:


def ejec_Funcion(inst,TS):
    fun_ = TS.obtener(inst.id)
    param = inst.listaParametros
    if fun_==None:
        print("Funcion no existente "+inst.id)
        listaErrores.append(error("Funcion no existente "+inst.id,0,0,"Semantico"))
    #params_ = TS.obtener(inst.id).parametros


    TS.inst += f'addi sp,sp,-4\n'
    TS.inst += f'sw ra, 0(sp)\n'
   
    if fun_.tipo == TIPOS_P.ENTERO:
        TS.inst += f'addi sp,sp,-4\n'
    elif fun_.tipo == TIPOS_P.BOOLEAN:
        TS.inst += f'addi sp,sp,-1\n'
    elif fun_.tipo == TIPOS_P.CHAR:
        TS.inst += f'addi sp,sp,-1\n'

    for i in range(0,len(param)):
        exp,tipo = ejec_expresion(param[i],TS)
        TS.inst += f'addi sp,sp,-4\n'
        TS.inst += f'sw {exp}, 0(sp)\n'

    TS.inst += f'call {inst.id}\n'
    TS.inst += f'addi sp,sp,{fun_.RA}\n'
    TS.inst += f'lw ra ,0(sp)\n'
    TS.inst += f'addi sp,sp,4\n'

    # TablaLocal = copy.deepcopy(TS)
    # TablaLocal.ambito = inst.id
    # for i in range(len(inst.listaParametros)):

    #     exp = ejec_expresion(inst.listaParametros[i], TS)

    #     #aqui poner si es array o nel

    #     TablaLocal.agregar(Simbolos(params_[i].id,TIPOS_Simbolos.VARIABLE,params_[i].tipo,copy.deepcopy(exp),TablaLocal.ambito))
        
        

    # tupla = ejec_instrucciones(fun_, TablaLocal)
    # #print(tupla)
    # if tupla!= None:
    #     return tupla
    
    # addi sp,sp,-4
	# sw ra, 0(sp)
	# call _saludar1
	# lw ra ,0(sp)
	# addi sp,sp,4
    
def resolver_expresionArray(exp,TS):

    temp1 = TS.getNextTemp(0)
    #temp2 = TS.getNextTemp(0)
    TS.inst += f'addi a0,x0,{len(exp.valores)}\n'

    if len(exp.valores)!=0:
        if isinstance(exp.valores[0],ExpresionDobleComilla):
            #que hacer si es string
            TS.inst += f'addi {temp1},x0,4\n'
            tipo = TIPOS_P.CADENA
            i= 4
        elif isinstance(exp.valores[0],ExpresionAritmetica):
            #entero
            TS.inst += f'addi {temp1},x0,4\n'
            tipo = TIPOS_P.ENTERO
            i=4
        elif isinstance(exp.valores[0],ExpresionRelacional) or isinstance(exp.valores[0],ExpresionBoleana):
            #Bool
            TS.inst += f'addi {temp1},x0,1\n'
            tipo = TIPOS_P.BOOLEAN
            i=1
        elif isinstance(exp.valores[0],ExpresionComillaSimple):
            #Char
            TS.inst += f'addi {temp1},x0,1\n'
            tipo = TIPOS_P.CHAR
            i=1

    TS.inst += f'mul a0,a0,{temp1}\n'
    TS.inst += f'addi a0,a0,4\n'
    TS.inst += f'li a7,9\n'
    TS.inst += f'ecall\n'  #alojar memoria heap

    TS.inst += f'add {temp1},a0,x0\n' #direccion memoria

    TS.inst += f'addi a0,x0,{len(exp.valores)}\n' 

    TS.inst += f'sw a0, 0({temp1})\n' 


    for valor in exp.valores:
        exp,tipoExp = ejec_expresion(valor,TS)
        if tipo != tipoExp:
            print("Tipos diferentes en Lista")
            listaErrores.append(error("Tipos diferentes en Lista",0,0,"Semantico"))
            return None,TIPOS_P.VOID
        if tipo==TIPOS_P.ENTERO or tipo==TIPOS_P.CADENA:
            #TS.inst += f'add a0,{exp},x0\n'
            TS.inst += f'sw {exp}, {i}({temp1})\n'
            i+=4
            TS.restoreTemp(1)
        else:
            #TS.inst += f'add a0,{exp},x0\n'
            TS.inst += f'sb {exp},{i}({temp1})\n'
            i+=1
            TS.restoreTemp(1)

    if tipo==TIPOS_P.BOOLEAN:
        tipo= TIPOS_P.ARRAY_BOOLEAN
    elif tipo==TIPOS_P.CHAR:
        tipo= TIPOS_P.ARRAY_CHAR
    elif tipo==TIPOS_P.CADENA:
        tipo= TIPOS_P.ARRAY_STRING
    elif tipo==TIPOS_P.ENTERO:
        tipo= TIPOS_P.ARRAY_INT

    return temp1,tipo


            

    # resultado = []

    # for valor in exp.valores:
    #     exp = ejec_expresion(valor,TS)
    #     resultado.append(exp)

    # return resultado

    # addi a0,x0,4 #Cantidad elementos Array
	
	# addi a1,x0,4 #Tamano de entero
	
	# mul a0,a0,a1 #Tamano Array
	
	# addi a0,a0,4 #Tamano Array + 1 
			
	# li a7,9
	# ecall
	
	# add t0,x0,a0  #Direccion memoria en temp
	
	# addi a0,x0,4
	
	# sw a0,0(t0) #Agrego ptr a header
	
	# addi a0,x0,8
	
	# sw a0, 4(t0) #Agrego elem 8
	
	# addi a0,x0,4
	
	# sw a0, 8(t0) #Agrego elem 4
	
	# addi a0,x0,6
	
	# sw a0, 12(t0) #Agrego elem 6
	
	# addi a0,x0,2
	
	# sw a0, 16(t0) #Agrego elem 2

def ejec_AsignacionArray(inst,TS):
    exp = ejec_expresion(inst.valor,TS)
    index = ejec_expresion(inst.index,TS)
    simbolo = TS.obtener(inst.id)
    
    if simbolo== None:
        print("No se encontro variable "+inst.id)
        listaErrores.append(error("No se encontro variable "+inst.id,0,0,"Semantico"))
        return

    if simbolo.tipo_simbolo==TIPOS_Simbolos.CONSTANTE:
        print("No se puede asignar a Constante "+inst.id)
        listaErrores.append(error("No se puede asignar a Constante "+inst.id,0,0,"Semantico"))
        return

    try:
        simbolo.valor[index] = exp
    except:
        print("Error al asignar valor a Array "+inst.id)
        listaErrores.append(error("Error al asignar valor a Array "+inst.id,0,0,"Semantico"))
    
    TS.actualizar(inst.id,simbolo.valor)
    
    TSReporte.actualizar(copy.deepcopy(inst.id),copy.deepcopy(simbolo.valor))

def resolver_expresion_AccesoArray(exp,TS):
    simbolo =  TS.obtener(exp.id)
    index = ejec_expresion(exp.indice,TS)
    if simbolo== None:
        listaErrores.append(error("Se quiere usar valor null con variable "+simbolo.id,0,0,"Semantico"))
        print("Se quiere usar valor null con variable "+simbolo.id)
        return
    
    try:
        valor = copy.deepcopy(simbolo.valor[index])
    except:
        print("Error al acceder al valor de Array "+exp.id)
        listaErrores.append(error("Error al acceder al valor de Array "+exp.id,0,0,"Semantico"))
        return
    return valor

def ejec_FuncionPush(inst,TS):
    simbolo = TS.obtener(inst.id)
    exp = ejec_expresion(inst.listaParametros[0],TS)
    

    if simbolo== None:
        print("No se encontro variable "+inst.id)
        listaErrores.append(error("No se encontro variable "+inst.id,0,0,"Semantico"))
        return

    try:
        simbolo.valor.append(exp)
    except:
        print("Error al agregar valor a Array "+inst.id)
        listaErrores.append(error("Error al agregar valor a Array "+inst.id,0,0,"Semantico"))
    
    TS.actualizar(inst.id,simbolo.valor)
    
    TSReporte.actualizar(copy.deepcopy(inst.id),copy.deepcopy(simbolo.valor))

def ejec_FuncionPop(inst,TS):
    simbolo = TS.obtener(inst.id)
  
    if simbolo== None:
        print("No se encontro variable "+inst.id)
        listaErrores.append(error("No se encontro variable "+inst.id,0,0,"Semantico"))
        return
    
    try:
        resultado = simbolo.valor.pop()
        TS.actualizar(inst.id,simbolo.valor)
    
        TSReporte.actualizar(copy.deepcopy(inst.id),copy.deepcopy(simbolo.valor))

        return resultado
    except:
        print("Error al Pop a Array "+inst.id)
        listaErrores.append(error("Error al Pop a Array "+inst.id,0,0,"Semantico"))

def ejec_FuncionIndexOf(inst,TS):
    simbolo = TS.obtener(inst.id)
    exp = ejec_expresion(inst.listaParametros[0],TS)

    if simbolo== None:
        print("No se encontro variable "+inst.id)
        listaErrores.append(error("No se encontro variable "+inst.id,0,0,"Semantico"))
        return
    index = -1
    
    try:
        index =simbolo.valor.index(exp)

    except:
        #print("Error, no se encontro el index del valor "+ str(exp)+"del array "+inst.id)
        #listaErrores.append(error("Error, no se encontro el index del valor "+ str(exp)+"del array "+inst.id,0,0,"Semantico"))
        pass

    
    return index

def ejec_FuncionJoin(inst,TS):
    simbolo = TS.obtener(inst.id)

    if simbolo== None:
        print("No se encontro variable "+inst.id)
        listaErrores.append(error("No se encontro variable "+inst.id,0,0,"Semantico"))
        return
    
    cadena =""

    try:

        cadena = str(simbolo.valor)

        cadena = cadena[1:len(cadena)-1]

    except:
        #print("Error, no se encontro el index del valor "+ str(exp)+"del array "+inst.id)
        #listaErrores.append(error("Error, no se encontro el index del valor "+ str(exp)+"del array "+inst.id,0,0,"Semantico"))
        pass

    
    return cadena

def ejec_FuncionLength(inst,TS):
    simbolo = TS.obtener(inst.id)

    if simbolo== None:
        print("No se encontro variable "+inst.id)
        listaErrores.append(error("No se encontro variable "+inst.id,0,0,"Semantico"))
        return
    
    largo = 0

    try:

        largo = len(simbolo.valor)

    except:
        #print("Error, no se encontro el index del valor "+ str(exp)+"del array "+inst.id)
        #listaErrores.append(error("Error, no se encontro el index del valor "+ str(exp)+"del array "+inst.id,0,0,"Semantico"))
        pass

    
    return largo

def ejec_FuncionParseInt(inst,TS):
    exp = ejec_expresion(inst.listaExpresiones[0],TS)

    if isinstance(exp,str):

        try:
            result = float(exp)
            result = int(result)
            return result
        except:
            print("Error al Parsear valor a int")
            listaErrores.append(error("Error al Parsear valor a int",0,0,"Semantico"))
    else:
        print("Error,tipo invalido para Parse int")
        listaErrores.append(error("Error,tipo invalido para Parse int",0,0,"Semantico"))

def ejec_FuncionParseFloat(inst,TS):
    exp = ejec_expresion(inst.listaExpresiones[0],TS)

    if isinstance(exp,str):

        try:
            result = float(exp)
            return result
        except:
            print("Error al Parsear valor a float")
            listaErrores.append(error("Error al Parsear valor a float",0,0,"Semantico"))
    else:
        print("Error,tipo invalido para Parse float")
        listaErrores.append(error("Error,tipo invalido para Parse float",0,0,"Semantico"))

def ejec_FuncionToString(inst,TS):
    exp = ejec_expresion(inst.id,TS)

    try:
        result = str(exp)
        return result
    except:
        print("Error al Parsear valor a string")
        listaErrores.append(error("Error al Parsear valor a string",0,0,"Semantico"))

def ejec_FuncionToLowerCase(inst,TS):
    exp = ejec_expresion(inst.id,TS)

    try:
        
        return exp.lower()
    except:
        print("Error al Parsear valor a toLowerCase")
        listaErrores.append(error("Error al Parsear valor a toLowerCase",0,0,"Semantico"))

def ejec_FuncionToUpperCase(inst,TS):
    exp = ejec_expresion(inst.id,TS)

    try:
        
        return exp.upper()
    except:
        print("Error al Parsear valor a toUpperCase")
        listaErrores.append(error("Error al Parsear valor a toUpperCase",0,0,"Semantico"))

def ejec_FuncionTypeOf(inst,TS):
    exp = ejec_expresion(inst.exp,TS)

    try:
        if isinstance(exp,bool):
            return "boolean"
        elif isinstance(exp,float):
            return "float"
        elif isinstance(exp,str) and len(exp)==1:
            return "char"
        elif isinstance(exp,str):
            return "string"
        elif isinstance(exp,int):
            return "number"
        elif isinstance(exp,list):
            return "Array"
    except:
        print("Error al obtener typeOf valor")
        listaErrores.append(error("Error al obtener typeOf valor",0,0,"Semantico"))

def ejec_AsignacionMatriz(inst,TS):
    exp = ejec_expresion(inst.valor,TS)
    #index = ejec_expresion(inst.index,TS)
    simbolo = TS.obtener(inst.id)
    
    if simbolo== None:
        print("No se encontro variable "+inst.id)
        listaErrores.append(error("No se encontro variable "+inst.id,0,0,"Semantico"))
        return

    if simbolo.tipo_simbolo==TIPOS_Simbolos.CONSTANTE:
        print("No se puede asignar a Constante "+inst.id)
        listaErrores.append(error("No se puede asignar a Constante "+inst.id,0,0,"Semantico"))
        return

    try:
        temp = simbolo.valor
        temp = asignarValorMatrizRecursiva(temp,inst.listaIndices,TS,exp)

    except:
        print("Error al asignar valor a Array "+inst.id)
        listaErrores.append(error("Error al asignar valor a Array "+inst.id,0,0,"Semantico"))
    
    TS.actualizar(inst.id,temp)
    
    TSReporte.actualizar(copy.deepcopy(inst.id),copy.deepcopy(temp))

def asignarValorMatrizRecursiva(lista,index,TS,exp):
    if len(index)==0:
        return exp
    else:
        valorIndex = ejec_expresion(index[0],TS)
        lista[valorIndex] = asignarValorMatrizRecursiva(lista[valorIndex],index[1:len(index)],TS,exp)
        return lista


def resolver_expresion_AccesoMatriz(exp,TS):
    simbolo =  TS.obtener(exp.id)
    #index = ejec_expresion(exp.indice,TS)
    if simbolo== None:
        listaErrores.append(error("Se quiere usar valor null con variable "+simbolo.id,0,0,"Semantico"))
        print("Se quiere usar valor null con variable "+simbolo.id)
        return
    
    try:
        temp = simbolo.valor
        for index in exp.listaIndices:
            valorIndex = ejec_expresion(index,TS)
            temp = temp[valorIndex]
        
    except:
        print("Error al acceder al valor de Array "+exp.id)
        listaErrores.append(error("Error al acceder al valor de Array "+exp.id,0,0,"Semantico"))
        return
    return temp

def ejec_Funcion_exp(inst,TS):
    fun_ = TS.obtener(inst.id)
    param = inst.listaParametros
    if fun_==None:
        print("Funcion no existente "+inst.id)
        listaErrores.append(error("Funcion no existente "+inst.id,0,0,"Semantico"))
    #params_ = TS.obtener(inst.id).parametros


    TS.inst += f'addi sp,sp,-4\n'
    TS.inst += f'sw ra, 0(sp)\n'

    if fun_.tipo == TIPOS_P.ENTERO:
        TS.inst += f'addi sp,sp,-4\n'
    elif fun_.tipo == TIPOS_P.BOOLEAN:
        TS.inst += f'addi sp,sp,-1\n'
    elif fun_.tipo == TIPOS_P.CHAR:
        TS.inst += f'addi sp,sp,-1\n'

    for i in range(0,len(param)):
        exp,tipo = ejec_expresion(param[i],TS)
        TS.inst += f'addi sp,sp,-4\n'
        TS.inst += f'sw {exp}, 0(sp)\n'

    TS.inst += f'call {inst.id}\n'
    temp= TS.getNextTemp(0)
    if fun_.tipo==TIPOS_P.ENTERO:
        retorno = TS.obtener(fun_.id+"Return")
        offset = fun_.RA -4 - retorno.RA
        TS.inst += f'lw {temp},{offset}(sp)\n'
    elif fun_.tipo ==TIPOS_P.BOOLEAN:
        retorno = TS.obtener(fun_.id+"Return")
        offset = fun_.RA -4 - retorno.RA
        TS.inst += f'lb {temp},{offset}(sp)\n'
    elif fun_.tipo ==TIPOS_P.CHAR:
        retorno = TS.obtener(fun_.id+"Return")
        offset = fun_.RA -4 - retorno.RA
        TS.inst += f'lb {temp},{offset}(sp)\n'
    TS.inst += f'addi sp,sp,{fun_.RA}\n'
    TS.inst += f'lw ra ,0(sp)\n'
    TS.inst += f'addi sp,sp,4\n'

    return temp,fun_.tipo