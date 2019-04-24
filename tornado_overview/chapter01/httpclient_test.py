from tornado import httpclient


# http_client = httpclient.HTTPClient()
#
# try:
#     response = http_client.fetch("http://www.tornadoweb.org/en/stable/")
#     print(response.body.decode("utf8"))
# except httpclient.HTTPError as e:
#     print("Error: " + str(e))
# except Exception as e:
#     print("Error: " + str(e))
#
# http_client.close()

async def f():
    client = httpclient.AsyncHTTPClient()
    try:
        response = await client.fetch("http://www.tornadoweb.org/en/stable/")
    except Exception as e:
        print("Error: " + str(e))
    else:
        print(response.body.decode("utf8"))


if __name__ == '__main__':
    import tornado

    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(f)
