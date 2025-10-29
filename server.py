from flask import Flask, request, jsonify, send_from_directory
import paho.mqtt.client as mqtt
from threading import Lock

app= Flask(__name__)

broker= "broker.hivemq.com" #servidor que atua como intermediário
topico="simulador/mqtt/mensagens" #tópico: categoria para troca de mensagens 
mensagens= []
lock= Lock() #objeto de sincronização
#O broker é o entregador das mensagens.
#O tópico é o endereço para onde as mensagens são enviadas e recebidas.

#configurar o cliente MQTT 
cliente= mqtt.Client()
def on_connect(cliente, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código {rc}")
    cliente.subscribe(topico)  #Essa linha quer dizer que o cliente (ou seja, o seu programa) está “se inscrevendo” em um endereço específico — o tópico.

def on_message(client, userdata, msg):
    msg_text= msg.payload.decode()
    with lock:
        mensagens.append(msg_text)
        if len(mensagens) > 50: #limita o tamanho da lista para 50 msg 
            mensagens.opo(0)
            
cliente.on_connect= on_connect
cliente.on_message= on_message
cliente.connect(broker) #conecta ao broker MQTT
cliente.loop_start()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/enviar', methods=["POST"])
def enviar(): data= request.json
msg= data.get('mensagem')