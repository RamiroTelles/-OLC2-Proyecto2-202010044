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
            elif isinstance(inst,AsignacionMatriz): ejec_AsignacionMatriz(inst,TS)
            elif isinstance(inst,funcionPush): ejec_FuncionPush(inst,TS)
            elif isinstance(inst,controlFlujo): #ejec_controlFlujo(inst,TS)
                tupla=ejec_controlFlujo(inst,TS)
                if tupla!=None:
                    return tupla
                    #pass
            elif isinstance(inst,guardar_func): pass
                
        else:
            if isinstance(inst,guardar_func): ejec_Guardar_Func(inst,TS)
        #else: print('Error: instruccion no valida')
        

def ejec_Imprimir(inst,TS):
    
    
    for exp in inst.lista:

        #print('>> ', ejec_expresion(exp,TS))
        result = ejec_expresion(exp,TS)
        

        if isinstance(exp, ExpresionDobleComilla) :
            TS.inst += f'''la a1, {result}
                            la a0, {result}len
                            lw a2, 0(a0)
                            li a0, 1 
                            li a7, 64 
                            ecall\n'''
        
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

        return f'msg{msg}'
    elif isinstance(exp,ExpresionComillaSimple):
        return exp.cad[1:len(exp.cad)-1]
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
        exp1 = ejec_expresion(expNum.exp1,TS)
        exp2 = ejec_expresion(expNum.exp2,TS)

        if len(exp1) == 2 and len(exp2)==2 or len(exp1) == 3 and len(exp2)==3:
            #Numeros o Caracteres o bool
            if expNum.operador == OPERACION_ARITMETICA.MAS : 
                temp= TS.getNextTemp(2)
                TS.inst += f'add {temp},{exp1},{exp2}\n'
                return temp
            if expNum.operador == OPERACION_ARITMETICA.MENOS : 
                temp= TS.getNextTemp(2)
                TS.inst += f'sub {temp},{exp1},{exp2}\n'
                return temp
            if expNum.operador == OPERACION_ARITMETICA.POR : 
                temp= TS.getNextTemp(2)
                TS.inst += f'mul {temp},{exp1},{exp2}\n'
                return temp
            if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                temp= TS.getNextTemp(2)
                TS.inst += f'div {temp},{exp1},{exp2}\n'
                return temp
            if expNum.operador == OPERACION_ARITMETICA.MODULO : 
                temp= TS.getNextTemp(2)
                TS.inst += f'rem {temp},{exp1},{exp2}\n'
                return temp
    elif isinstance(expNum,ExpresionNegativa):
        exp1 = resolver_expresionAritmetica(expNum.exp1,TS)
        temp= TS.getNextTemp(1)
        
        TS.inst += f'sub {temp},x0,{exp1}\n'
       
        return temp
        
    elif isinstance(expNum,ExpresionEntero):
        
        temp = TS.getNextTemp(0)
        
        TS.inst += f'addi {temp}, x0, {expNum.exp1}\n'

        return temp
        
    elif isinstance(expNum,ExpresionDecimal):
        return expNum.exp1
    

def resolver_expresionRelacional(exp,TS):
    if isinstance(exp,ExpresionRelacional):
        exp1 = ejec_expresion(exp.exp1,TS)
        exp2 = ejec_expresion(exp.exp2,TS)

        if exp.operador == OPERACION_REL.MAYOR_QUE : return exp1 > exp2
        if exp.operador == OPERACION_REL.MENOR_QUE : return exp1 < exp2
        if exp.operador == OPERACION_REL.MAYORIGUAL : return exp1 >= exp2
        if exp.operador == OPERACION_REL.MENORIGUAL : return exp1 <= exp2
        if exp.operador == OPERACION_REL.IGUAL : return exp1 == exp2
        if exp.operador == OPERACION_REL.NO_IGUAL : return exp1 != exp2
    
def resolver_expresionBoleana(expBol,TS):
    if isinstance(expBol,ExpresionLogica):
        exp1 = ejec_expresion(expBol.exp1,TS)
        exp2 = ejec_expresion(expBol.exp2,TS)

        if expBol.operador == OPERACION_LOGICA.AND : return exp1 and exp2
        if expBol.operador == OPERACION_LOGICA.OR : return exp1 or exp2
    elif isinstance(expBol,ExpresionNot):
        return not ejec_expresion(expBol.exp1,TS)
    elif isinstance(expBol,Expresion_True_False):
        if expBol.exp1 == "true": return True
        if expBol.exp1 == "false" : return False

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
    return exp_id.valor


def ejec_declaracion_explicita(inst,TS):
    cont=1
    exp = ejec_expresion(inst.valor,TS)

    if TS.obtener(inst.id)!=None:
        print("Ya declarada variable "+inst.id)
        listaErrores.append(error("Ya declarada variable "+inst.id,0,0,"Semantico"))
        #return
 

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
    
    TS.restoreTemp(cont)
 #   TSReporte.agregar(copy.deepcopy(simbolo))

def ejec_declaracion_implicita(inst,TS):
    exp = ejec_expresion(inst.valor,TS)
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
            simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.CONSTANTE,tipo=inst.tipo,valor=exp,ambito=TS.ambito,linea=inst.linea,columna=inst.columna)
    else:
        simbolo = Simbolos(id=inst.id,tipo_simbolo=TIPOS_Simbolos.VARIABLE,tipo=inst.tipo,valor=exp,ambito=TS.ambito,linea=inst.linea,columna=inst.columna)
    TS.agregar(simbolo)
    
    TSReporte.agregar(copy.deepcopy(simbolo))

def ejec_Asignacion(inst,TS):
    
    exp = ejec_expresion(inst.valor,TS)
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
        if simbolo.tipo==TIPOS_P.ENTERO:
            exp= int(exp)
        elif simbolo.tipo==TIPOS_P.FLOAT:
            exp= float(exp)
        elif simbolo.tipo==TIPOS_P.CADENA:
            exp= str(exp)
        elif simbolo.tipo==TIPOS_P.CHAR:
            exp= str(exp)
        elif simbolo.tipo==TIPOS_P.BOOLEAN:
            exp= bool(exp)
    except:
        print("Error, "+inst.id+" No se puede asignar un tipo de variable diferente")
        listaErrores.append(error(inst.id+" No se puede asignar un tipo de variable diferente",0,0,"Semantico"))
    TS.actualizar(inst.id,exp)
    
    TSReporte.actualizar(copy.deepcopy(inst.id),copy.deepcopy(exp))


def ejec_controlFlujo(inst,TS):
    if isinstance(inst,inst_if): 
        tupla = ejec_If(inst,TS)
        if tupla != None:
            return tupla

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
    exp = ejec_expresion(inst.cond,TS)
    if exp:
        TablaLocal = TablaSimbolos(simbolos=TS.simbolos.copy(),ambito=TS.ambito +"_If")

        tupla = ejec_instrucciones(inst.instruccionesIf,TablaLocal)
        #TS.salida+= TablaLocal.salida
        
    else:
        TablaLocal = TablaSimbolos(simbolos=TS.simbolos.copy(),ambito=TS.ambito +"_If")

        tupla = ejec_instrucciones(inst.instruccionesElse,TablaLocal)
        #TS.salida+= TablaLocal.salida
    
    return tupla

def ejec_While(inst,TS):
    
    exp = ejec_expresion(inst.cond,TS)
    while exp:
        TablaLocal = TablaSimbolos(simbolos=TS.simbolos.copy(),ambito=TS.ambito +"_While")

        tupla = ejec_instrucciones(inst.instrucciones,TablaLocal)
        if tupla!=None:

            if isinstance(tupla[0],inst_Break):
                
                break
            if isinstance(tupla[0],inst_Return):
                
                return tupla

        exp = ejec_expresion(inst.cond,TS)
        #TS.salida+= TablaLocal.salida
    
        
    
    

def ejec_For(inst,TS):
    
    
        


    TablaLocal = TablaSimbolos(simbolos=TS.simbolos.copy(),ambito=TS.ambito +"_For")

  
    ejec_instrucciones(copy.deepcopy(inst.instruccion1),TablaLocal)
    exp= ejec_expresion(inst.cond,TablaLocal)

    while exp:
        #TablaLocal2 = copy.deepcopy(TablaLocal)
        tupla = ejec_instrucciones(inst.instruccion_verdadero,TablaLocal)
        if tupla!=None:

            if isinstance(tupla[0],inst_Break):
                
                break
            if isinstance(tupla[0],inst_Return):
                
                return tupla
        ejec_instrucciones(inst.instruccion2,TablaLocal)
        #TablaLocal.actualizar(inst.instruccion2[0].id,ejec_expresion(inst.instruccion2[0].valor,TablaLocal))
        exp = ejec_expresion(inst.cond,TablaLocal)
    #TS.salida+= TablaLocal.salida
        
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