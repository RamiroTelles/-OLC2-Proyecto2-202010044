from expresiones import *
from instrucciones import *
from simbolos import *
from tipos import TIPOS_P,TIPOS_Simbolos
from errores import error
import copy

listaErrores =[]


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
            elif isinstance(inst,guardar_func): pass
                
        else:
            if isinstance(inst,guardar_func): ejec_Guardar_Func(inst,TS)
        #else: print('Error: instruccion no valida')
        

def ejec_Imprimir(inst,TS):
    
    
    for exp in inst.lista:

        #print('>> ', ejec_expresion(exp,TS))
        result,tipo = ejec_expresion(exp,TS)
        

        if isinstance(exp, ExpresionDobleComilla) :
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
                            jal _print_true
                            j L{label2}
                        L{label1}:
                            jal _print_false
                        L{label2}:\n'''
        elif isinstance(exp,ExpresionBoleana):
            label1 = TS.getNextLabel()
            label2= TS.getNextLabel()
            TS.inst += f''' beqz {result},L{label1}
                            jal _print_true
                            j L{label2}
                        L{label1}:
                            jal _print_false
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
                                jal _print_true
                                j L{label2}
                            L{label1}:
                                jal _print_false
                            L{label2}:\n'''
        
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
        tupla =ejec_Funcion(exp,TS)
        if tupla!=None:
            return tupla[1]
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
        return None
    else :
        return None
    
 

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
    if ejec_expresion(expTer.exp1):
        return ejec_expresion(expTer.exp2,TS)
    return ejec_expresion(expTer.exp3,TS)

def resolver_expresionId(expId,TS):
    exp_id =  TS.obtener(expId.id)
    if exp_id== None:
        listaErrores.append(error("Se quiere usar valor null con variable "+expId.id,0,0,"Semantico"))
        print("Se quiere usar valor null con variable "+expId.id)
        return
    temp = TS.getNextTemp(0)
    TS.inst += f'la {temp}, {expId.id}\n'
    TS.inst += f'lw {temp}, 0({temp})\n'
    return temp, exp_id.tipo


def ejec_declaracion_explicita(inst,TS):
    cont=1
    exp,tipo = ejec_expresion(inst.valor,TS)

    if TS.obtener(inst.id)!=None:
        print("Ya declarada variable "+inst.id)
        listaErrores.append(error("Ya declarada variable "+inst.id,0,0,"Semantico"))
        #return
 
    if inst.tipo != tipo:
        print("Asignacion equivocada de tipos "+inst.id)
        listaErrores.append(error("Asignacion equivocada de tipos "+inst.id,0,0,"Semantico"))
        #aqui se pondria que se asigna null
        return

    if inst.const == True:
        if exp==None:
            print("No asigno valor a const "+inst.id)
            listaErrores.append(error("No asigno valor a const "+inst.id,0,0,"Semantico"))
            return
        else:
            simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.CONSTANTE,tipo=inst.tipo,valor=exp,ambito=TS.ambito,linea=inst.linea,columna=inst.columna)
    elif inst.arrayList!=0:
        simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.ARRAY,tipo=inst.tipo,valor=exp,ambito=TS.ambito,linea=inst.linea,columna=inst.columna)
    else:
        simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.VARIABLE,tipo=inst.tipo,valor=exp,ambito=TS.ambito,linea=inst.linea,columna=inst.columna)
        
    TS.agregar(simbolo)
    if inst.tipo == TIPOS_P.ENTERO:
        TS.Datos += f'{inst.id}: .word 0\n'
        if exp!= None:
            cont+=1
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp},{inst.id}\n'
            TS.inst += f'sw {exp},0({temp})\n'
    if inst.tipo == TIPOS_P.BOOLEAN:
        TS.Datos += f'{inst.id}: .byte 1\n'
        if exp!= None:
            cont+=1
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp},{inst.id}\n'
            TS.inst += f'sw {exp},0({temp})\n'
    if inst.tipo == TIPOS_P.CHAR:
        TS.Datos += f'{inst.id}: .byte 0\n'
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

    if inst.const == True:
        if exp==None:
            print("No asigno valor a const "+inst.id)
            listaErrores.append(error("No asigno valor a const "+inst.id,0,0,"Semantico"))
            return
        else:
            simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.CONSTANTE,tipo=tipo,valor=exp,ambito=TS.ambito,linea=inst.linea,columna=inst.columna)
    else:
        simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.VARIABLE,tipo=tipo,valor=exp,ambito=TS.ambito,linea=inst.linea,columna=inst.columna)
    TS.agregar(simbolo)

    if tipo== TIPOS_P.ENTERO:
        TS.Datos += f'{inst.id}: .word 0\n'
        if exp!= None:
            cont+=1
            temp = TS.getNextTemp(0)
            TS.inst += f'la {temp},{inst.id}\n'
            TS.inst += f'sw {exp},0({temp})\n'
    if inst.tipo == TIPOS_P.BOOLEAN:
        TS.Datos += f'{inst.id}: .byte 1\n'
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

    
    temp = TS.getNextTemp(0)
    TS.inst += f'la {temp},{inst.id}\n'
    TS.inst += f'sw {exp},0({temp})\n'
    TS.actualizar(inst.id,exp)
    
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
        if('While' in TS.ambito or 'For' in TS.ambito):
            return inst,None
        else:
            print("Sentencia continue fuera de un Ciclo")
            listaErrores.append(error("Sentencia continue fuera de un Ciclo",0,0,"Semantico"))
    elif isinstance(inst,inst_Break): 
       
        
        if('While' in TS.ambito or 'For' in TS.ambito or 'Switch' in TS.ambito):
            return inst,None
        else:
            print("Sentencia break fuera de flujo de control valido")
            listaErrores.append(error("Sentencia break fuera de flujo de control valido",0,0,"Semantico"))
    elif isinstance(inst,inst_Return):
        return inst,ejec_expresion(inst.valor,TS) 
    
def ejec_If(inst,TS):
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
    TS.inst+=f'{Linicio}:\n'
    
    exp,tipo = ejec_expresion(inst.cond,TS)
    
    TS.inst+= f'''  bnez {exp},{Lsent}
                    j {Lsalida}
                {Lsent}:\n'''
    
    ejec_instrucciones(inst.instrucciones,TS)

    TS.inst+=f'j {Linicio}\n'
    TS.inst+=f'{Lsalida}:\n'

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
    valorId = ejec_expresion(inst.id,TS)
    posDefault=-1
    contador=-1
    for i in range(len(inst.listaExpresiones)):
        exp= ejec_expresion(inst.listaExpresiones[i],TS)
        if exp==None:
            posDefault=i
        elif valorId== exp:
            contador=i

    TablaLocal = TablaSimbolos(simbolos=TS.simbolos.copy(),ambito=TS.ambito +"_Switch")
    if contador!=-1:
        for i in range(contador,len(inst.listaInst)):
            tupla = ejec_instrucciones(inst.listaInst[i],TablaLocal)
            
            if tupla!=None:

                if isinstance(tupla[0],inst_Break):
                    
                    break
                if isinstance(tupla[0],inst_Return):
                    
                    return tupla
    elif posDefault!=-1:
        for i in range(posDefault,len(inst.listaInst)):
            tupla = ejec_instrucciones(inst.listaInst[i],TablaLocal)
            
            if tupla!=None:

                if isinstance(tupla[0],inst_Break):
                    
                    break
                if isinstance(tupla[0],inst_Return):
                    
                    return tupla

    #TS.salida+= TablaLocal.salida

def ejec_Guardar_Func(inst,TS):
    sim =TS.obtener(inst.id)
    if sim!=None:
        if sim.tipo_simbolo==TIPOS_Simbolos.FUNCION:
            print("Ya declarada Funcion "+inst.id)
            listaErrores.append(error("Ya declarada Funcion "+inst.id,0,0,"Semantico"))
            return
    
    simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.FUNCION,tipo=inst.tipo,valor=None,ambito=TS.ambito,parametros=inst.listaParametros,instrucciones=inst.instrucciones)

    TS.agregar(simbolo)
    
    TSReporte.agregar(copy.deepcopy(simbolo))


def ejec_Funcion(inst,TS):
    fun_ = TS.obtener(inst.id).instrucciones
    params_ = TS.obtener(inst.id).parametros
    TablaLocal = copy.deepcopy(TS)
    TablaLocal.ambito = inst.id
    for i in range(len(inst.listaParametros)):

        exp = ejec_expresion(inst.listaParametros[i], TS)

        #aqui poner si es array o nel

        TablaLocal.agregar(Simbolos(params_[i].id,TIPOS_Simbolos.VARIABLE,params_[i].tipo,copy.deepcopy(exp),TablaLocal.ambito))
        
        

    tupla = ejec_instrucciones(fun_, TablaLocal)
    #print(tupla)
    if tupla!= None:
        return tupla
    
def resolver_expresionArray(exp,TS):
    resultado = []

    for valor in exp.valores:
        exp = ejec_expresion(valor,TS)
        resultado.append(exp)

    return resultado

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