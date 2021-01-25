#!/usr/bin/python
import pymt5
import time
import signal
from collections import OrderedDict
import json
import random
import string

clients = []
bid = float(random.randrange(12660, 12680))/10000
spread = 0.0004
ask = bid+spread
last = 0
vol = 0

def onConnected(client_info):
    clients.append(client_info.get('client_id'))
    print('[onConnected] client_address: ' + str(client_info))
    print('[clients] ' + str(clients))

def onDisconnected(client_info):
    clients.remove(client_info.get('client_id'))
    print('[onDisconnected] client_address: ' + str(client_info))
    print('[clients] ' + str(clients))

def sendOrderConfirmed(client, order):
    global last
    global vol
    order.update({'exchange_id':str(int(time.time()))})
    if order['type_order'] == '0':
        order.update({'price_order':str(ask)})
        last = ask
    else:
        order.update({'price_order':str(bid)})
        last = bid
    vol = float(order['volume'])
    order.update({'state':'1'})
    order.update({'result':'10009'})
    m.send(client, order)
    m.broadcast(OrderedDict([('ver','3'),('type','4'),('symbol','EURUSD.TEST'),('bank','dc'),('bid',str(bid)),('ask',str(ask)),('last',str(last)),('volume',str(vol)),('datetime','0')]))

def sendOrderPlaced(client, order):
    order.update({'state':'2'})
    order.update({'result':'10008'})
    m.send(client, order)

def sendOrderNew(client, order):
    order.update({'state':'3'})
    order.update({'result':'1'})
    m.send(client, order)

def sendOrderDeal(client, order):
    order.update({'state':'5'})
    order.update({'result':'1'})
    m.send(client, order)

def sendOrderRejectNew(client, order):
    order.update({'state':'4'})
    order.update({'result':'10006'})
    m.send(client, order)

def sendOrderCancel(client, order):
    order.update({'state':'10'})
    order.update({'result':'10007'})
    m.send(client, order)

def sendOrderComplete(client, order):
    order.update({'state':'20'})
    order.update({'result':'10009'})
    m.send(client, order)

def sendDeal(client, order):
    exchange_id = '0'
    while exchange_id.startswith('0'):
        exchange_id = ''.join(random.choice(string.digits) for i in range(8))
    deal =  OrderedDict([('ver','3'),
                         ('type','7'),
                         ('exchange_id',exchange_id),
                         ('order',order['order']),
                         ('symbol',order['symbol']),
                         ('login',order['login']),
                         ('type_deal',order['type_order']),
                         ('volume',order['volume']),
                         ('volume_rem','0'),
                         ('price','1.2679')])
    m.send(client, deal)

def sendDealExternal(client, exchange_id, symbol, login, type_deal, volume, price, datetime='1611339821000'):
    deal =  OrderedDict([('ver','3'),
                         ('type','50'),
                         ('exchange_id',exchange_id),
                         ('order','0'),
                         ('symbol',symbol),
                         ('login',login),
                         ('type_deal',type_deal),
                         ('volume',volume),
                         ('volume_rem','0'),
                         ('price',price),
                         ('datetime',datetime)])
    m.send(client, deal)

def sendTick():
    global bid
    global ask
    bid = float(random.randrange(12660, 12680))/10000
    ask = bid+spread
    m.broadcast(OrderedDict([('ver','3'),('type','4'),('symbol','EURUSD.TEST'),('bank','dc'),('bid',str(bid)),('ask',str(ask)),('last',str(last)),('volume',str(vol)),('datetime','0')]))

def onData(data):
    print('[onData] data: ' + json.dumps(data))
    client = data.get('client_id')
    # Login
    if data.get('type') == '1':
        # Send heartbeat
        m.send(client, OrderedDict([('ver','3'),
                                    ('type','6')]))
        # Send login OK response (no auth)
        m.send(client, OrderedDict([('ver','3'),
                                    ('type','1'),
                                    ('login',data.get('login')),
                                    ('password',data.get('password')),
                                    ('res','0')]))
        # Send symbol with index starting at 0
        time.sleep(0.5)
        m.send(client, OrderedDict([('ver','3'),
                                    ('type','3'),
                                    ('index','0'),
                                    ('symbol','EURUSD.TEST'),
                                    ('path','TestExchange'),
                                    ('description','test'),
                                    ('page','http://www.google.co/finance?q=EURUSD.TEST'),
                                    ('currency_base','EUR'),
                                    ('currency_profit','USD'),
                                    ('currency_margin','USD'),
                                    ('digits','4'),
                                    ('tick_flags','7'),
                                    ('calc_mode','0'),
                                    ('exec_mode','2'),
                                    ('chart_mode','0'),
                                    ('fill_flags','3'),
                                    ('expir_flags','15'),
                                    ('tick_value','0.00000'),
                                    ('tick_size','0.00000'),
                                    ('contract_size','100000.00000'),
                                    ('volume_min','0.01000'),
                                    ('volume_max','10000.00000'),
                                    ('volume_step','0.01000'),
                                    ('market_depth','0'),
                                    ('margin_flags','0'),
                                    ('margin_initial','0.00000'),
                                    ('margin_maintenance','0.00000'),
                                    ('margin_long','1.00000'),
                                    ('margin_short','1.00000'),
                                    ('margin_limit','0.00000'),
                                    ('margin_stop','0.00000'),
                                    ('margin_stop_limit','0.00000'),
                                    ('settlement_price','1.22804'),
                                    ('price_limit_max','0.00000'),
                                    ('price_limit_min','0.00000'),
                                    ('time_start','0'),
                                    ('time_expiration','0'),
                                    ('trade_mode','4')]))
    # Logout
    elif data.get('type') == '2':
        m.disconnect(client)
    # New order
    elif data.get('type') == '5' and data.get('state') == '0':
        order = data
        del order['client_id']
        # Market
        if order['action'] == '2':
            sendOrderConfirmed(client, order)
        elif order['action'] == '3':
            sendOrderConfirmed(client, order)
        elif order['action'] in ('4','5'):
            sendOrderPlaced(client, order)
            sendOrderNew(client, order)
            sendDeal(client, order)
        else:
            sendOrderRejectNew(client, order)

def onSIGINT(signum, frame):
    global end
    end = True

##################
# Main
##################
signal.signal(signal.SIGINT, onSIGINT)
m = pymt5.PyMT5()
m.onConnected = onConnected
m.onDisconnected = onDisconnected
m.onData = onData

end = False
while not end:
    time.sleep(1)
    sendTick()
m.stop()
