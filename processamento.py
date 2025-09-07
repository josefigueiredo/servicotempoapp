# python 3.11

import sqlite3,json
import pandas as pd


bd = "databases/leituras.db"

def conectaBD():
    try:
        con = sqlite3.connect(bd)
    except sqlite3.Error as e:
        print(f"um erro ocorreu: {e}")
    finally:
        return con

def fechaBD(conn):
    conn.close()

def buscaUltimo(conn):
    cur = conn.cursor()
    statement = '''SELECT * FROM tbl_ultimoProcessado'''
    res = cur.execute(statement)
    return res.fetchone()

def buscaLeituras(conn,ultimoProcessado):
    cur = conn.cursor()
    statement = '''SELECT * FROM tbl_leituras WHERE time > ?'''
    res =  cur.execute(statement,ultimoProcessado)
    return res.fetchall()
    
def getHeatingIndex(temp,umidade):
    csv_file = 'heat_index.csv'
    df = pd.read_csv(csv_file,
                    sep=",",          # separador de coluna é vírgula
                    decimal=",",      # separador decimal é vírgula
                    quotechar='"',     # valores estão entre aspas
                    header=0,
                    index_col=0
                    )
    farenheitInt = round(32+temp*9/5)
    umidInt = round(umidade)
    
    if farenheitInt%2 == 0 and umidInt%2 == 0:
        indexHeatingFar = df.loc[farenheitInt,str(umidInt)]
    elif farenheitInt%2 == 0 and umidInt%2 != 0:
        r1 = df.loc[farenheitInt,str(umidInt-1)]
        r2 = df.loc[farenheitInt,str(umidInt+1)]
        indexHeatingFar = (r1+r2)/2
    elif farenheitInt%2 != 0 and umidInt%2 == 0:
        r1 = df.loc[farenheitInt-1,str(umidInt)]
        r2 = df.loc[farenheitInt+1,str(umidInt)]
        indexHeatingFar = (r1+r2)/2
    else:
        r1 = df.loc[farenheitInt-1,str(umidInt-1)]
        r2 = df.loc[farenheitInt-1,str(umidInt+1)]
        r3 = df.loc[farenheitInt+1,str(umidInt-1)]
        r4 = df.loc[farenheitInt+1,str(umidInt+1)]
        indexHeatingFar = (r1+r2+r3+r4)/4
    indexHeatingCelcius = (indexHeatingFar-32)*5/9
    return round(indexHeatingCelcius,1)

def calcTempAparente(temperatura,umidade,velVento):
    # calculos com formulas obtidas em   
    if temperatura < 24.2:
        # calculo com equação Wind-Chill 
        #https://s.campbellsci.com/documents/es/technical-papers/windchil.pdf
        #tApar = 13.127 + 0.6215*T - 13.947*a + 0.486*T*a
        #tApar = 13.127 + 0.6215T - 13.947 v^(0.16) + 0.486 Tv^(0.16)
        #T em celcius, v em m/s, tApar em celcius
        
        a = velVento**0.16
        tApar = round(13.127 + 0.6215*temperatura - 13.947*a + 0.486*temperatura*a,1)
    else:
        tApar = getHeatingIndex(temperatura,umidade)

    return tApar

def insereTempAparente(conn,tempAparJson):
    print(tempAparJson)
    cur = conn.cursor()
    columns = ', '.join(tempAparJson.keys())
    placeholders = ', '.join('?' * len(tempAparJson))
    sql = 'INSERT INTO tbl_tempaparente ({}) VALUES ({})'.format(columns, placeholders)

    cur.execute(sql, tuple(tempAparJson.values()))
    conn.commit()

def updateUltimoProcessado(conn,ultimoProcessado):
    cur = conn.cursor()
    cur.execute("delete from tbl_ultimoProcessado")
    conn.commit()
    
    columns = ', '.join(ultimoProcessado.keys())
    placeholders = ', '.join('?' * len(ultimoProcessado))
    sql = 'INSERT INTO tbl_ultimoprocessado ({}) VALUES ({})'.format(columns, placeholders)

    cur.execute(sql, tuple(ultimoProcessado.values()))
    conn.commit()

def run():
    con = conectaBD()
    ultimo = buscaUltimo(con)
    pendentes = buscaLeituras(con,ultimo)

    for e in pendentes:
        print(e)
        time = e[0]
        temp = e[3]
        umid = e[2]
        tAp = calcTempAparente(temp,umid,5)
        dadosTempApJson = {"time":time,"tempaparente":tAp}
        insereTempAparente(con,dadosTempApJson)
    ultimoProcessado = {"time":e[0]}
    updateUltimoProcessado(con,ultimoProcessado)

    fechaBD(con)
