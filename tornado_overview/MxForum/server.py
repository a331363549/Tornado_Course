from peewee_async import Manager
from tornado import web
import tornado

from MxForum.MxForm.urls import urlpattern
from MxForum.MxForm.settings import settings, database

import wtforms_json

if __name__ == '__main__':
    wtforms_json.init()
    app = web.Application(urlpattern, debug=True, **settings)
    app.listen(8888)

    objects = Manager(database)
    database.set_allow_sync(False)

    app.objects = objects

    tornado.ioloop.IOLoop.current().start()
