#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import pymt5
import time
import signal
from collections import OrderedDict

client = ''
order = deal = OrderedDict()
logged_in = False
m = None

def onConnected(client_info):
    global client
    client = client_info.get('client_id')
    print('[onConnected] client_address: ' + str(client_info))

def onDisconnected(client_info):
    global client
    client = ''
    print('[onDisconnected] client_address: ' + str(client_info))

def onData(data):
    global logged_in
    print('[onData] data: ' + str(data))
    client = data.get('client_id')
    # Login
    if data.get('type') == '1':
        # Send heartbeat
        m.send(client, OrderedDict([('ver','3'),
                                    ('type','6')]))
        # Send login OK response
        m.send(client, OrderedDict([('ver','3'),
                                    ('type','1'),
                                    ('login',data.get('login')),
                                    ('password',data.get('password')),
                                    ('res','0')]))
        # Sync a symbol
        time.sleep(0.5)
        m.send(client, OrderedDict([('ver','3'),
                                    ('type','3'),
                                    ('index','0'),
                                    ('symbol','XAUUSD.a'),
                                    ('path','TestExchange'),
                                    ('description','test'),
                                    ('page','http://www.google.co/finance?q=XAUUSD.a'),
                                    ('currency_base','XAU'),
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
                                    ('volume_min','0.00000'),
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
        logged_in = True

def onSIGINT(signum, frame):
    global end
    end = True

##################
# Main
##################
signal.signal(signal.SIGINT, onSIGINT)
m = pymt5.PyMT5(port=5533)
m.onConnected = onConnected
m.onDisconnected = onDisconnected
m.onData = onData
while not logged_in:
    time.sleep(1)
deal = OrderedDict([('ver','3'),
                    ('type','50'),
                    ('exchange_id', str(int(time.time()))),
                    ('order','1596687043'),
                    ('symbol','XAUUSD.a'),
                    ('login','999011'),
                    ('type_deal','0'),
                    ('volume','2'),
                    ('volume_rem','0'),
                    ('price','1355.80'),
                    ('datetime', '1596535624555'),
                    ('comment','TEST')])
m.send(client, deal)
print('[sendExternalDeal] deal: ' + str(deal))
end = False
while not end:
    time.sleep(1)
m.stop()
