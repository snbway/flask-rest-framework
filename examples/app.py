# -*- coding:utf-8 -*-

from flask import Flask
from flask_restful import Api
from views.handler import HelloView

app = Flask(__name__)
api = Api(app)



api.add_resource(HelloView, '/')

if __name__ == '__main__':
    app.run(debug=True)
