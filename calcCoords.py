import paho.mqtt.client as paho
import json
import time

L = 293
D = 30
ballDelta = 50
ballDeltaTime = 500
hostName = "localhost"
mqtt_login = "login"
mqtt_pwd = "password"

prevBall1 = 0, 0
prevTime1 = 0
prevBall2 = 0, 0
prevTime2 = 0
prevYTime = 0
prevY = -1


def calcWeight(y, camType):
    if camType == "1":
        if y < (L / 2 - D / 2):
            w = 1
        elif y > (L / 2 + D / 2):
            w = 0
        else:
            w = 1 - ((y - (L / 2 - D / 2)) / D)
    elif camType == "2":
        if y < (L / 2 - D / 2):
            w = 0
        elif y > (L / 2 + D / 2):
            w = 1
        else:
            w = (y - (L / 2 - D / 2)) / D
    return w


def onMessage(client, userdata, msg):
    global prevBall1, prevBall2, prevTime1, prevTime2, prevY, prevYTime, ballDeltaTime
    ballC = 0, 0
    deltaTime = time.time()
    data = json.loads(msg.payload.decode('utf-8'))
    if data['ball'] != "None":
        if data['camId'] == "1":
            if len(data['ball']) == 1:
                wN = calcWeight(data['ball'][0]['center']['y'], data['camId'])
                ballC = data['ball'][0]['center']['x'], data['ball'][0]['center']['y'] * wN + prevBall2[1] * (1 - wN)
                prevBall1 = data['ball'][0]['center']['x'], data['ball'][0]['center']['y']
                if prevBall2[1] != 0:
                    deltaTime -= prevTime2
                else:
                    deltaTime -= prevTime1
                prevTime1 = time.time()
                print(abs(ballC[0] - prevBall2[0]), abs(ballC[1] - prevBall2[1]))
        if data['camId'] == "2":
            if len(data['ball']) == 1:
                wN = calcWeight(data['ball'][0]['center']['y'], data['camId'])
                ballC = data['ball'][0]['center']['x'], data['ball'][0]['center']['y'] * wN + prevBall1[1] * (1 - wN)
                prevBall2 = data['ball'][0]['center']['x'], data['ball'][0]['center']['y']
                if prevBall1[1] != 0:
                    deltaTime -= prevTime1
                else:
                    deltaTime -= prevTime2
                prevTime2 = time.time()
                print(abs(ballC[0] - prevBall1[0]), abs(ballC[1] - prevBall1[1]))
    else:
        if data['camId'] == "1":
             prevBall1 = 0, 0
        else:
             prevBall2 = 0, 0
    if ballC[0] != 0 and ballC[1] != 0 and (abs(deltaTime) <= 1000):
        print(ballC)
        client.publish("MIPT-SportRoboticsClub/LunokhodFootball/Ball", json.dumps(ballC))


client = paho.Client()
client.on_message = onMessage
client.username_pw_set(mqtt_login, mqtt_pwd)
client.connect(host=hostName)

client.subscribe("MIPT-SportRoboticsClub/LunokhodFootball/RawBALL/#")

client.loop_forever()

