import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setblocking(False)
host = "www.baidu.com"

try:
    client.connect((host, 80))  # 阻塞io  意味着CPU空闲
except BlockingIOError as e:
    # TO DO OTHER THINGS
    pass

while 1:
    try:
        client.send("GET {} HTTP/1.1\r\nHost:{}\r\nCOnnection:close\r\n\r\n".format("/", host).encode("utf8"))
        print("succsess")
        break
    except OSError as e:
        pass

data = b""
while 1:
    try:
        d = client.recv(1024)
        print("123")
    except BlockingIOError as e:
        continue
