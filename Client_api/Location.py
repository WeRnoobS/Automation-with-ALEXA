import json
import os
import requests


def creating_url():
    try:
        os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
        with open('tunnels.json') as data_file:
            dataJson = json.load(data_file)
        return dataJson
    except Exception as e:
        print(e.args)
        print("start ngrok to get tunnel the localhost")


def posting_URL(_url):
    _main_url = "https://alexa2automation.onrender.com/add?url="
    try:
        respone = requests.post(_main_url+_url)
        return print(respone.text)
    except Exception as identifier:
        print(identifier)


if __name__ == "__main__":
    url = ""
    jsonData = creating_url()
    for i in jsonData['tunnels']:
        url = url+i['public_url']+'\n'
    print(posting_URL(url.split("\n")[0]))
