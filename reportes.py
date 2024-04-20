from tipos import TIPOS_P,TIPOS_Simbolos

def crearReporteErroes(listaErrores):
    txt = '''
    <html>
        <head><title> Reporte Errores </title></head>
            <body>
                <div align="center">
                    <h1> Reporte Errores</h1>
                        <br></br>
                            <table border=1>
                                <tr>
                                    <td>Descripcion</td>
                                    <td>Linea</td>
                                    <td>Columna</td>
                                    <td>Tipo</td>
                                </tr>                
    '''

    for err in listaErrores:
        txt+= "<tr>"
        txt+= "<td>"+ err.descripcion+ "</td>"
        txt+= "<td>"+ str(err.linea)+ "</td>"
        txt+= "<td>"+ str(err.columna)+ "</td>"
        txt+= "<td>"+ err.tipo+ "</td>"
        txt+= "</tr>"
    
    txt+= "</table>\n</div>\n</body>\n</html>"

    try:

        with open("reporteErrores.html", "w") as file:
            file.write(txt)
            file.close() 

    except:
        print("No se pudo crear el Reporte Errores")

def crearReporteTablaSimbolos(ts):
    txt = '''
    <html>
        <head><title> Reporte Tabla Simbolos </title></head>
            <body>
                <div align="center">
                    <h1> Reporte Tabla Simbolos</h1>
                        <br></br>
                            <table border=1>
                                <tr>
                                    <td>Id</td>
                                    <td>Tipo</td>
                                    <td>Tipo Dato</td>
                                    <td>Valor</td>
                                    <td>Ambito</td>
                                    <td>Linea</td>
                                    <td>Columna</td>
                                </tr>                
    '''

    for simbol in ts.simbolos.values():
        txt+= "<tr>"
        txt+= "<td>"+ simbol.id+ "</td>"
        if simbol.tipo_simbolo == TIPOS_Simbolos.FUNCION:
            txt+= "<td> Funcion</td>"
        elif simbol.tipo_simbolo == TIPOS_Simbolos.CONSTANTE:
            txt+= "<td> Constante</td>"
        elif simbol.tipo_simbolo == TIPOS_Simbolos.ARRAY:
            txt+= "<td> Array</td>"
        else:
            txt+= "<td> Variable</td>"
        if simbol.tipo ==TIPOS_P.ENTERO:
            txt+= "<td> Number</td>"
        elif simbol.tipo==TIPOS_P.FLOAT:
            txt+= "<td> Float</td>"
        elif simbol.tipo==TIPOS_P.CADENA:
            txt+= "<td> Cadena</td>"
        elif simbol.tipo==TIPOS_P.BOOLEAN:
            txt+= "<td> Boolean</td>"
        elif simbol.tipo==TIPOS_P.CHAR:
            txt+= "<td> Char</td>"
        else:
            txt+= "<td> Void</td>"
        if simbol.valor ==None:
            txt+= "<td> Null</td>"
        else:
            txt+= "<td> "+ str(simbol.valor)+"</td>"
        txt+= "<td>"+ simbol.ambito+ "</td>"
        txt+= "<td>"+ str(simbol.linea)+ "</td>"
        txt+= "<td>"+ str(simbol.columna)+ "</td>"
        txt+= "</tr>"
    
    txt+= "</table>\n</div>\n</body>\n</html>"

    try:

        with open("reporteTS.html", "w") as file:
            file.write(txt)
            file.close() 

    except:
        print("No se pudo crear el Reporte TS")