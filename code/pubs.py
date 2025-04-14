import RPi.GPIO as gpio
import picamera
import time
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
from urllib.parse import urlparse




gpio.setmode(gpio.BCM)
gpio.setup(13, gpio.IN)
gpio.setup(5,gpio.OUT)
gpio.setup(17, gpio.OUT)
gpio.setup(18, gpio.IN)

def on_connect(client, userdata, flags, rc):
  print ("on_connect:: Connected with result code "+ str ( rc ) )
  print('rc: ' + str(rc))
def on_message(client,obj,mid):
  print ("on_message:: this means  I got a message from brokerfor this topic")
  print('mid:'+str(mid))
def on_publish(client, obj, mid):
  print('mid:' + str(mid))
def on_subscribe(client, obj, mid, granted_qos):
  print("This means broker has acknowledged my subscribe request")
  print('Subscribed:' + str(mid)+' '+ str(granted_qos))
def on_log(client,obj,level,string):
  print(string)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.username_pw_set("ojg","20192387")
mqttc.connect('localhost',1883,60)

topic = 'dist'
video = 'video'
photo = 'picture'

mqttc.connect('localhost',1883)

mqttc.subscribe(topic,0)

def pics():
  with picamera.PiCamera() as camera:
      savepath = '/home/ojg/project/pictures'
      camera.resolution = (1024, 768)
      now = datetime.datetime.now()
      filename = now.strftime('%Y-%m-%d %H:%M:%S')
      camera.start_preview()
      time.sleep(1)
      camera.stop_preview()
      camera.capture(savepath + '/' + filename + '.jpg')
      f = open(savepath + '/' + filename + '.jpg', "rb")
      file = f.read()
      sfile = bytearray(file)
      return sfile

count = 0
while True:
  gpio.output(17, False)
  time.sleep(0.5)
        
  gpio.output(17, True)
  time.sleep(0.00001)
  gpio.output(17, False)
        
  while gpio.input(18) == 0:
    start = time.time()
            
  while gpio.input(18) == 1:
    stop = time.time()
            
  time_interval = stop - start
  distance = time_interval * 17000
  distance = round(distance,2)
  if(distance < 10):
    count += 1
  if((distance >= 10) or (count > 3)):
    count = 0
  print('Distance => ', distance, 'cm')
  if(count > 2):
    mqttc.publish(topic,'alert')
    payload2 = pics()
    publish.single(photo,payload2)

  if(gpio.input(13) == 0):
    savepath = '/home/ojg/project/videos'
    with picamera.PiCamera() as camera:
      camera.resolution = (640,480)
      now = datetime.datetime.now()
      filename = now.strftime('%Y-%m-%d %H:%M:%S')
      gpio.output(5,gpio.HIGH)
      camera.start_recording(output = savepath + '/' + filename + '.h264')
      camera.wait_recording(15)
      camera.stop_recording()
      gpio.output(5,gpio.LOW)
      f = open(savepath + '/' + filename + '.h264', "rb")
      file = f.read()
      sfile = bytearray(file)
      mqttc.publish(video, sfile)
  else:
    print(gpio.input(13))
    time.sleep(1)

