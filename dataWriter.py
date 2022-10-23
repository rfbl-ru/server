import paho.mqtt.client as paho
import json
import time

client = paho.Client()
client.username_pw_set("app", "ss8Brl9UcW")
client.connect(host="82.146.32.180")

with open("logs/cam1.json") as file:
    cam1Data = json.load(file)

with open("logs/cam2.json") as file:
    cam2Data = json.load(file)

camData = []
for data in cam1Data:
    data.append("1")
    camData.append(data)

for data in cam2Data:
    data.append("2")
    camData.append(data)

camData.sort()
try:
    for i in range(len(camData)):
        ball = {'camId' : camData[i][2], 'ball': camData[i][1]}
        client.publish("MIPT-SportRoboticsClub/LunokhodFootball/RawBALL/"+camData[i][2], json.dumps(ball))
        sleepTime = camData[i+1][0]-camData[i][0]
        time.sleep(sleepTime)
except KeyboardInterrupt:
    client.disconnect()