import requests
import json
import time

speed = 50

t = 0

def wait():
	global t
	if t != 0:
		time.sleep(60 / speed)
	print(t)
	t = t + 1

def send(url,data):
	data["token"] = 1
	data = json.dumps(data)
	header = {"Content-Type": "application/json;charset=utf-8"}
	url = "http://127.0.0.1:5000/" + url
	res = requests.post(url=url,data=data,headers=header)
	res.content.decode("utf-8")
	time.sleep(0.02 / speed)
	return json.loads(res.text)


on = "/api/usr/poweron"
off = "/api/usr/poweroff"
wind = "api/usr/changefanspeed"
temp = "api/usr/changetargettemp"

#start 
wait()

data = {}
res = send("api/admin/poweron",data)

data = {
	"mode":1,
	"temp_h":27,
	"temp_l":16,
	"default_targetTemp":25,
	"default_fanSpeed":"1",
	"feeRate_h":1,
	"feeRate_m":1,
	"feeRate_l":1
}
res = send("api/admin/setpara",data)

data = {}
res = send("api/admin/startup",data)

wait()
# min 1

data = {
    "roomId":"101",
    "targetTemp":30,
    "fanSpeed":"1",
    "currentTemp":26
}
res = send(on,data)


# min 2

wait()

data = {
    "roomId":"102",
    "targetTemp":30,
    "fanSpeed":"1",
    "currentTemp":26
}
res = send(on,data)

data = {
	"roomId":"101",
    "targetTemp":18
}
res = send(temp,data)

# min 3

wait()

data = {
    "roomId":"103",
    "targetTemp":30,
    "fanSpeed":"1",
    "currentTemp":26
}
res = send(on,data)

# min 4

wait()

data = {
    "roomId":"104",
    "targetTemp":30,
    "fanSpeed":"1",
    "currentTemp":26
}
res = send(on,data)

data = {
	"roomId":"102",
    "targetTemp":19
}
res = send(temp,data)

# min 5

wait()

# min 6

wait()

data = {
	"roomId":"101",
    "fanSpeed":"2"
}
res = send(wind,data)

# min 7

wait()

data = {
    "roomId":"102",
}
res = send(off,data)

# min 8

wait()

data = {
    "roomId":"102",
    "targetTemp":30,
    "fanSpeed":"1",
    "currentTemp":26
}
res = send(on,data)

# min 9

wait()

# min 10

wait()

data = {
    "roomId":"101",
    "targetTemp":22,
}
res = send(temp,data)

data = {
	"roomId":"104",
    "fanSpeed":"2"
}
res = send(wind,data)

# min 11

wait()

# min 12

wait()


data = {
	"roomId":"102",
    "targetTemp":22
}
res = send(temp,data)

# min 13

wait()

# min 14

wait()

# min 15

wait()

data = {
    "roomId":"101",
}
res = send(off,data)

data = {
	"roomId":"103",
    "targetTemp":24
}
res = send(temp,data)

data = {
	"roomId":"103",
	"fanSpeed":"0"
}
res = send(wind,data)

# min 16

wait()

# min 17

wait()

data = {
    "roomId":"102"
}
res = send(off,data)

# min 18

wait()

data = {
	"roomId":"103",
    "fanSpeed":"2"
}
res = send(wind,data)

# min 19

wait()

data = {
    "roomId":"101",
    "targetTemp":30,
    "fanSpeed":"1",
    "currentTemp":26
}
res = send(on,data)

data = {
	"roomId":"104",
    "targetTemp":20
}
res = send(temp,data)

data = {
	"roomId":"104",
	"fanSpeed":"1"
}

res = send(wind,data)
# min 20

wait()

data = {
    "roomId":"102",
    "targetTemp":30,
    "fanSpeed":"1",
    "currentTemp":26
}
res = send(on,data)

# min 21

wait()

# min 22

wait()

# min 23

wait()

data = {
    "roomId":"103",
}
res = send(off,data)

# min 24

wait()

# min 25

wait()

data = {
    "roomId":"101"
}
res = send(off,data)

# min 26

wait()

data = {
    "roomId":"102",
}
res = send(off,data)

data = {
	"roomId":"104",
}
res = send(off,data)