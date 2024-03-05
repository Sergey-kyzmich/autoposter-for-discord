id = 679385458731384832
k = 2
import requests
import time
import json
import datetime
from websocket import create_connection
import os

def connection_web_socket(token):
    ws = create_connection("wss://gateway.discord.gg/")
    data = '''
            {
                "op": 2,
                "d":{
                    "token": "%s",
                    "properties": {
                        "$os": "linux",
                        "$browser": "ubuntu",
                        "$device": "ubuntu"
                    },
                }
            }
            ''' % token
    ws.send(data)
    return ws

derictori = os.getcwd().replace("\\", "/")+"/baze/"
with open(derictori+str(id)+"/"+str(k)+".json", "r") as read_file:
    message = json.load(read_file)
message["time"] = message["time"].split((","))[0]
def image_url(url, id, derictori):
    img_data = requests.get(url)
    handler = open(derictori +str(id) +"/"+ str(k) + ".png", 'wb')
    handler.write(img_data.content)
    handler.close

def chek_next_time(a, t, k):
    if message["id_chanal"] == "" or message["time"] == "" or message["text"] == "":  # проверка на корректность данных
        print(f"{id} {k} eror")
        return False
    else:
        dt1 = datetime.datetime(2023, 12,23, 0, 0, 0)
        dt2 = datetime.datetime.now()
        tdelta = dt2 - dt1
        if int(str(tdelta.total_seconds())[:str(tdelta.total_seconds()).index(".")])<a:
            if k=="0":
                time.sleep(a-int(str(tdelta.total_seconds())[:str(tdelta.total_seconds()).index(".")]))
            else:
                time.sleep(a-int(str(tdelta.total_seconds())[:str(tdelta.total_seconds()).index(".")])+int(t)*60)
        return True

print("reload ", k, id)
chek_time = chek_next_time(message["next_time"], message["time"], 0)

if "http" in message["image"]:
    image_url(message["image"], id, derictori)

with open(derictori+str(id)+"/on_list.json", "r") as read_file:
    on_list = json.load(read_file)

def check_subscription():
    with open(derictori+str(id)+"/pay_to.txt", "r") as read_file:
        a = read_file.read()
        d = a.split(",")
        dt1 = datetime.datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]))
        dt2 = datetime.datetime.now()
        tdelta = dt1 - dt2
        if int(tdelta.total_seconds()) > 0:
            return True
        else:
            return False

def send(on_list,chek_time):
    try:
        subscription = check_subscription()
        while on_list[str(k)]==True and subscription == True and chek_time==True:
            with open(derictori + str(id) + "/" + str(k) + ".json", "r") as read_file:
                message = json.load(read_file)
            message["time"] = message["time"].split((","))[0]
            if message["id_chanal"] == "" or message["time"] == "" or message["text"] == "":  # проверка на корректность данных
                print(f"{id} {k} eror")
                return False
            else:

                with open(derictori +str(id)+ r"/token.txt", "r+") as f:
                    token = f.read()# получение токена
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
                    'Authorization': token
                }
                ws = connection_web_socket(token)
                if "http" not in message["image"]:
                    json_data = {
                        'content': message["text"]
                    }
                    response = requests.post(f"https://discord.com/api/v9/channels/{message['id_chanal']}/messages", headers=headers, data=json_data)
                else:
                    json_data = {
                        'content': message["text"]
                    }
                    if "gif" not in message["image"]:
                        image_url(message["image"], id, derictori)

                        files = {
                            'file': open(derictori + str(id) + "/" + str(k) + '.png', 'rb')
                        }

                        response = requests.post(f"https://discord.com/api/v9/channels/{message['id_chanal']}/messages",
                                                 headers=headers, data=json_data,
                                                 files=files)
                    else:
                        json_data = {
                            'content': message["text"] + "\n " + message["image"]
                        }
                        response = requests.post(f"https://discord.com/api/v9/channels/{message['id_chanal']}/messages",
                                                 headers=headers, data=json_data)
                print(id, k, response.status_code)
                dt1 = datetime.datetime(2023, 12, 23, 0, 0, 0)
                dt2 = datetime.datetime.now()
                tdelta = dt2 - dt1
                data_w = {
                    "id_chanal": message["id_chanal"],
                    "text": message["text"],
                    "image": message["image"],
                    "time": message["time"],
                    "next_time": int(str(tdelta.total_seconds())[:str(tdelta.total_seconds()).index(".")])+int(message["time"])*60
                }
                ws.close()
                with open(derictori + str(id) + "/" + str(k) + ".json", "w") as write_file:
                    json.dump(data_w, write_file)
                time.sleep(int(message["time"])*60)
                with open(derictori+str(id)+"/on_list.json", "r") as read_file:
                    on_list = json.load(read_file)
                subscription = check_subscription()
        else:
            return False
    except:
        return True
reload = send(on_list,chek_time)
while reload == True:
    reload=send(on_list,chek_time)