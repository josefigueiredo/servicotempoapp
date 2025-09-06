#!/usr/bin/env python3

# A versão do paho-mqtt no rasp é 1.6.1
# fonte
# https://pypi.org/project/paho-mqtt/1.6.1/#client

import paho.mqtt.publish as publish 
import time,schedule
from datetime import datetime

# para testes: sincroniza leituras a cada 10 miutos
intervalo = 2

class HoraCerta:
    def getTimestamp():
        from datetime import datetime
        return datetime.now().timestamp() 


class Sincronizador:
    def __init__(self,host):
        self.broker = host

    def sincronizar(self):
        import paho.mqtt.publish as publish 
        port = 1883
        userdata = {'username':"sincronizador",'password':"teste"}
        client_id = 'sincronizador'
        topico = "/estacaoIoT/syncleituras"
        timestamp = HoraCerta.getTimestamp()
        publish.single(topico,timestamp,qos=0,hostname=self.broker,port=1883,client_id="",auth=userdata)
        #publish.single(topico,timestamp,qos=0,hostname="127.0.0.1",port=1883,client_id="")
        print(datetime.now())

# para testes: sincroniza leituras a cada 10 miutos
intervalo = 15
sync = Sincronizador('192.168.18.118')
schedule.every(intervalo).minutes.do(sync.sincronizar)

def run():
    sync.sincronizar()
    while True:
        schedule.run_pending()
        time.sleep(5)

if __name__ == '__main__':
    run()