import requests

headers = {
    "Content-Type": "application/x-www-form-urlencoded;",
}

# print(requests.get("http://127.0.0.1:8888/?name=ding&name=fei"))
requests.post("http://127.0.0.1:8888/", headers=headers, data={
    "name": "ding",
    "ptt": "fei"
})
