#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import json, time, os
from wepay import WePay
from wepay.exceptions import WePayError

CLIENT_ID = '47880'
CLIENT_SECRET = '486f0aed70'
ACCESS_TOKEN = 'STAGE_4c777f22e99bf2357d52977f8d7e17bf5e71caa9d0df37fb9b0e4a3ba762b1d9'
ACCOUNT_ID = 1607343250
IN_PRODUCTION = False

preapproval_id = None
saved_data = {}
wake_time = None
sleep_time = None
checkout_uri = None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if checkout_uri:
            self.redirect(checkout_uri)
        # self.write("")

class SuccessHandler(tornado.web.RequestHandler):
    def get(self):
        global wake_time, sleep_time
        wake_time = time.time() + sleep_time
        self.write("Success!")

class NewInvoiceHandler(tornado.web.RequestHandler):
    def post(self):
        global sleep_time
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
        sleep_time = int(saved_data['time'])
        preapproval_id = response['preapproval_id']

        d = response
        ret = json.dumps({
            'url' : d['preapproval_uri']
            })

        self.write(ret)

def periodic():
    global wake_time, checkout_uri
    if wake_time and wake_time < time.time():
        print "Trigger capture."
        wake_time = None

        wepay = WePay(IN_PRODUCTION, ACCESS_TOKEN)
        response = wepay.call('/checkout/create', {
            'account_id': ACCOUNT_ID,
            'amount': saved_data['amount'],
            'short_description': saved_data['desc'],
            'type': 'GOODS',
            'preapproval_id': preapproval_id
        })

        checkout_uri = response['checkout_uri']

class IntroHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('static/index.html')

application = tornado.web.Application([
    (r"/confirm", MainHandler),
    (r"/new", NewInvoiceHandler),
    (r"/success", SuccessHandler),
    (r"/intro", IntroHandler)
], static_path=os.path.join(os.path.dirname(__file__), 'static'))

if __name__ == "__main__":
    application.listen(8888)
    main_loop = tornado.ioloop.IOLoop.instance()
    ping_loop = tornado.ioloop.PeriodicCallback(periodic, 100, io_loop=main_loop)
    ping_loop.start()
    main_loop.start()