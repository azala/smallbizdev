#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import json
from wepay import WePay
from wepay.exceptions import WePayError

CLIENT_ID = '47880'
CLIENT_SECRET = '486f0aed70'
ACCESS_TOKEN = 'STAGE_4c777f22e99bf2357d52977f8d7e17bf5e71caa9d0df37fb9b0e4a3ba762b1d9'
ACCOUNT_ID = 1607343250
IN_PRODUCTION = False

preapproval_id = None
saved_data = {}

users = {
    "Alice" : {
        "password" : "Alice"
    }
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")

class SuccessHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Success!")

class NewInvoiceHandler(tornado.web.RequestHandler):
    def post(self):
        saved_data.update(json.loads(self.request.body))
        wepay = WePay(IN_PRODUCTION, ACCESS_TOKEN)
        response = wepay.call('/preapproval/create', {
            'account_id': ACCOUNT_ID,
            'period': 'once',
            'amount': saved_data['amount'],
            'mode': 'regular',
            'short_description': saved_data['desc'],
            'redirect_uri': 'http://54.84.158.190:8888/success'
        })
        preapproval_id = response['preapproval_id']

        d = json.loads(response)
        ret = json.dumps({
            'url' : d['preapproval_uri']
            })

        self.write(ret)

class GrabHandler(tornado.web.RequestHandler):
    def post(self):
        wepay = WePay(IN_PRODUCTION, ACCESS_TOKEN)
        response = wepay.call('/checkout/create', {
            'account_id': ACCOUNT_ID,
            'amount': saved_data['amount'],
            'short_description': saved_data['desc'],
            'type': 'GOODS',
            'preapproval_id': preapproval_id
        })

        d = json.loads(response)
        ret = json.dumps({
            'url' : d['checkout_uri']
            })
        
        self.write(response)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/new", NewInvoiceHandler),
    (r"/success", SuccessHandler),
    (r"/grab", GrabHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()