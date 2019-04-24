import requests

html = requests.get("http://www.baidu.com").text
print(html)