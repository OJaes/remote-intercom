import cv2
import os
import datetime
import time
import paho.mqtt.client as mqtt

def convert_to_mp4(input_h264, output_mp4):
    cap = cv2.VideoCapture(input_h264)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_mp4, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def on_connect(client, userdata, flags, rc):
    print("connect.." + str(rc))
    if rc == 0:
        client.subscribe("video")
    else:
        print("연결 실패")

def on_message(client, userdata, msg):
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d %H-%M-%S')
    h264_path = 'C:\\ojg\\mqttvideo\\' + filename + '.h264'
    mp4_path = 'C:\\ojg\\mqttvideo\\' + filename + '.mp4'

    try:
        with open(h264_path, 'wb') as f:
            f.write(msg.payload)
        print("Video received")

        # Convert H.264 to MP4 using OpenCV
        convert_to_mp4(h264_path, mp4_path)
        print("Video converted to MP4")

        # Delete the original H.264 file
        os.remove(h264_path)
        print("H.264 file deleted")

    except Exception as e:
        print('Error:', e)

mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.connect("192.168.35.12", 1883, 60)
mqttClient.loop_forever()
