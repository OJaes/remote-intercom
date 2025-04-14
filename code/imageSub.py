import paho.mqtt.client as mqtt
import os
import time
import datetime

def on_connect(client, userdata, flags, rc):
    print("connected" + str(rc))
    if rc == 0:
        client.subscribe("picture")
    else:
        print("연결 실패")

def on_message(client, userdata, msg):
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d %H-%M-%S')  # ':'은 파일 이름에 사용할 수 없는 문자
    savepath = 'C:\\ojg\\mqttimage'
    try:
        print("try in")
        os.makedirs(savepath, exist_ok=True)  # 디렉터리가 없으면 생성
        full_path = os.path.join(savepath, filename + '.jpg')
        print("open")
        with open(full_path, "wb") as f:
            f.write(msg.payload)
        print("image received")
    except Exception as e:
        print("error:", e)
        print("error..")

mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.connect("192.168.35.12", 1883, 60)
mqttClient.loop_forever()
