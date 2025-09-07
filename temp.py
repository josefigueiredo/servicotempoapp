import sqlite3

bd = "databases/leituras.db"

def getLeituras():
    with sqlite3.connect(bd) as conn:
        cur = conn.cursor()
        sql = "SELECT * FROM tbl_leituras";
        cur.execute(sql);
        for row in cur:
            print(row)


def insereLeiturasBD(leituraJson):
    columns = ', '.join(leituraJson.keys())
    placeholders = ', '.join('?' * len(leituraJson))
    sql = 'INSERT INTO tbl_leituras ({}) VALUES ({})'.format(columns, placeholders)
    
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(sql, tuple(leituraJson.values()))
        con.commit()
    except sqlite3.Error as e:
        print(f"um erro ocorreu: {e}")
    finally:
        print(f"Leitura registrada com sucesso: {dt.now()}")
        if con:
            con.close()

def indexHeating(temp,umidade):
    umidade = ['40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100']
    temp = ['27', '28', '29', '30', '31', '32', '33', '34', '36', '37', '38', '39', '40', '41', '43', '47']
    dados = [
        [27, 27, 27, 27, 28, 28, 28, 29, 29, 29, 30, 30, 31],
        [27, 28, 28, 29, 29, 29, 30, 31, 32, 32, 33, 34, 35],
        [28, 29, 29, 30, 31, 32, 32, 33, 34, 36, 37, 38, 39],
        [29, 31, 31, 32, 33, 34, 35, 36, 38, 39, 41, 42, 44],
        [31, 32, 33, 34, 35, 37, 38, 39, 41, 43, 45, 47, 49],
        [33, 34, 35, 36, 38, 39, 41, 43, 45, 47, 50, 53, 56],
        [34, 36, 37, 38, 41, 42, 44, 47, 49, 52, 55],
        [36, 38, 39, 41, 43, 46, 48, 51, 54, 57],
        [38, 40, 42, 44, 47, 49, 52, 56],
        [41, 43, 45, 47, 51, 53, 57],
        [43, 46, 48, 51, 54, 58],
        [46, 48, 51, 54, 58],
        [48, 51, 55, 58],
        [51, 54, 58],
        [54, 58],
        [58],]
    matriz = pd.DataFrame(dados,index=temp,columns=umidade)
    l = str(temp)
    c = str(umidade)
    return matriz.loc[f'{temp}',c]


import pandas as pd

def lerCSV(temp,umidade):
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
        indexHeating = (r1+r2+r3+r4)/4
    indexHeatingCelcius = (indexHeatingFar-32)*5/9
    return round(indexHeatingCelcius,1)


csv_file = 'heat_index.csv'
df = pd.read_csv(csv_file,
                    sep=",",          # separador de coluna é vírgula
                    decimal=",",      # separador decimal é vírgula
                    quotechar='"',     # valores estão entre aspas
                    header=0,
                    index_col=0
                    )
print(df)