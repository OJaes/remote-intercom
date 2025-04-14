import paho.mqtt.client as mqtt
import os
import time

def on_connect(client, userdata, flags, rc):
    print("connect.." + str(rc))
    if rc == 0:
        client.subscribe("tts")
    else:
        print("연결 실패")

def on_message(client, userdata, msg):
    try:
        text = str(msg.payload.decode("utf-8"))
        print("recieved text : ", + text)
        os.system("espeak -v ko " + text)

mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.connect("localhost", 1883, 60)
mqttClient.loop_forever()
