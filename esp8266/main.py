import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, PWM
import json

# WIFI
SSID = "Wireless1"
PASSWORD = "@RcaNyabihu2023"

# MQTT
TEAM_ID = "team05"
BROKER = "10.12.73.101"
TOPIC = b"vision/team05/movement"

# Connect WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)

while not sta.isconnected():
    pass

# Servo setup
servo = PWM(Pin(5), freq=50)

angle = 90

def set_angle(a):
    duty = int(40 + (a / 180) * 75)
    servo.duty(duty)

set_angle(angle)

def callback(topic, msg):
    global angle
    data = json.loads(msg)

    if data["status"] == "MOVE_LEFT":
        angle -= 5
    elif data["status"] == "MOVE_RIGHT":
        angle += 5

    angle = max(0, min(180, angle))
    set_angle(angle)

client = MQTTClient("esp8266", BROKER)
client.set_callback(callback)
client.connect()
client.subscribe(TOPIC)

while True:
    client.check_msg()
    time.sleep(0.1)
