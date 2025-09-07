# python 3.11

from paho.mqtt import client as mqtt_client
import sqlite3,json
from datetime import datetime as dt


def insereLeiturasBD(leituraJson):
    bd = "databases/leituras.db"
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

def tratarDados(msg):
    strMsg = msg.decode("utf-8")
    print(strMsg)
    leituraJson = json.loads(strMsg)
    insereLeiturasBD(leituraJson)

def on_connect(client,userdata,flags,reason_code,properties):
    if reason_code.is_failure:
        print(f"falhou {reason_code}")
    else:
        client.subscribe(topic)

def on_subscribe(client,userdata,mid,reasonCodeList, properties):
    if reasonCodeList[0].is_failure:
        print(f"Erro de conexão com broker: {reasonCodeList[0]}")
    else:
        print(f"Conecatdo com QoS: {reasonCodeList[0].value}")

def on_message(client,userdata,msg):
    #print(f"recebido isso: {msg.payload}")
    tratarDados(msg.payload)


broker = '192.168.18.118'
port = 1883
topic = "/estacaoIoT/leituras/"

mqttc = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

mqttc.user_data_set([])
mqttc.username_pw_set(username="leitor",password="teste")
mqttc.connect(broker)
mqttc.loop_forever()
print(f"redebido {mqttc.user_data_get()}")
