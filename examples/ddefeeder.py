# -*- coding: utf-8 -*-
import pymt5
import time
import signal
from collections import OrderedDict
import json
exec(open('./ddeclient.py').read())

symbols = [

'CRUDEOIL V19-MCX',
'GOLD Z19-MCX',
'BANKNIFTY U19-NSF',

]
maps = {

'CRUDEOIL V19-MCX' : 'CRUDEOIL-1',
'GOLD Z19-MCX' : 'GOLD-1',
'BANKNIFTY U19-NSF' : 'BANKNIFTY-1',

}
clients = {}
indices = {}
quotes = {}

##################
# PyMT5 handlers
##################
def onConnected(client_info):
    client = client_info.get('client_id')
    clients[client] = client_info
    clients[client]['logged_in'] = False
    print("MT5 - onConnected - client_info:{}".format(str(client_info)))
    print("MT5 - onConnected - clients:{}".format(str(list(clients))))

def onDisconnected(client_info):
    client = client_info.get('client_id')
    del clients[client]
    print("MT5 - onDisconnected - client_info:{}".format(str(client_info)))
    print("MT5 - onDisconnected - clients:{}".format(str(list(clients))))

def sendSymbol(client, symbol):
    data = OrderedDict([('ver','3'),
                        ('type','3'),
                        ('index',str(indices[client])),
                        ('symbol',symbol),
                        ('path','DDE'),
                        ('description','DDE'),
                        ('page',''),
                        ('currency_base',''),
                        ('currency_profit',''),
                        ('currency_margin',''),
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
                        ('trade_mode','4')])
    m.send(client, data)
    indices[client] += 1

def onData(data):
    if data.get('type') == '1':
        onLogin(data)
    elif data.get('type') == '2':
        onLogout(data)
    elif data.get('type') == '6':
        onHeartbeat(data)
    else:
        print("MT5 - onData - data:{}".format(json.dumps(data)))

def onSIGINT(signum, frame):
    global end
    end = True

def onHeartbeat(data):
    print("MT5 - onHeartbeat - data:{}".format(json.dumps(data)))

def onLogin(data):
    print("MT5 - onLogin - data:{}".format(json.dumps(data)))
    client = data.get('client_id')
    login = data.get('login')
    password = data.get('password')
    # Send login OK response
    if login and password:
        clients[client]['logged_in'] = True
        m.send(client, OrderedDict([('ver','3'),
                                    ('type','1'),
                                    ('login',login),
                                    ('password',password),
                                    ('res','0')]))
        # Send a test symbol to make gateway status online
        indices[client] = 0
        for symbol in symbols:
            sendSymbol(client, maps[symbol])
    else:
        m.disconnect(client)
        del clients[client]
        print("MT5 - onLogin - not authorized - client_id:{}".format(client))

def onLogout(data):
    print("MT5 - onLogout - data:{}".format(json.dumps(data)))
    client = data.get('client_id')
    del clients[client]
    m.disconnect(client)
    print("MT5 - onLogout - data:{}".format(json.dumps(data)))
    print("MT5 - onLogout - clients:{}".format(str(list(clients))))

######################
# DDE client callback
######################
class ESignal(DDEClient):
    def callback(self, value, topic=None, item=None):
        print("eSignal - %s - %s=%s" % (item.decode('euc-kr'), topic.decode('euc-kr'), value.decode('euc-kr')))
        symbol = item.decode('euc-kr')
        #quotes[maps[symbol]]['datetime'] = str(int(round(time.time() * 1000))).replace('L','')[:-3]
        # Best bid/ask
        if topic.decode('euc-kr') == 'bid':
            quotes[maps[symbol]]['bid'] = value.decode('euc-kr')
        if topic.decode('euc-kr') == 'ask':
            quotes[maps[symbol]]['ask'] = value.decode('euc-kr')
            quotes[maps[symbol]]['last'] = '0'
            quotes[maps[symbol]]['volume'] = '0'
            print("MT5 - sendTick - data:{}".format(str(dict(quotes[maps[symbol]]))))
            m.broadcast(quotes[maps[symbol]])
        # Last and volume
        if topic.decode('euc-kr') == 'last':
            quotes[maps[symbol]]['last'] = value.decode('euc-kr')
        if topic.decode('euc-kr') == 'tradesize':
            quotes[maps[symbol]]['bid'] = ''
            quotes[maps[symbol]]['ask'] = ''
            quotes[maps[symbol]]['volume'] = value.decode('euc-kr')
            print("MT5 - sendTick - data:{}".format(str(dict(quotes[maps[symbol]]))))
            m.broadcast(quotes[maps[symbol]])

##################
# Main
##################
signal.signal(signal.SIGINT, onSIGINT)

# MT5 gateway
m = pymt5.PyMT5()
m.onConnected = onConnected
m.onDisconnected = onDisconnected
m.onData = onData

time.sleep(10)

# eSignal DDE client
bid = ESignal("WINROS", "bid")
ask = ESignal("WINROS", "ask")
last = ESignal("WINROS", "last")
tradesize = ESignal("WINROS", "tradesize")
for symbol in symbols:
    quotes[maps[symbol]] = OrderedDict([('ver','3'),
                                        ('type','4'),
                                        ('symbol',maps[symbol]),
                                        ('bank','esignal'),
                                        ('bid','0'),
                                        ('ask','0'),
                                        ('last','0'),
                                        ('volume','0'),
                                        ('datetime','0')])
    bid.advise(symbol)
    ask.advise(symbol)
    last.advise(symbol)
    tradesize.advise(symbol)

# Event loop
end = False
LPMSG = POINTER(MSG)
LRESULT = c_ulong
GetMessage = get_winfunc("user32", "GetMessageW", BOOL, (LPMSG, HWND, UINT, UINT))
TranslateMessage = get_winfunc("user32", "TranslateMessage", BOOL, (LPMSG,))
DispatchMessage = get_winfunc("user32", "DispatchMessageW", LRESULT, (LPMSG,))
msg = MSG()
lpmsg = byref(msg)
while GetMessage(lpmsg, HWND(), 0, 0) > 0 and not end:
    TranslateMessage(lpmsg)
    DispatchMessage(lpmsg)

m.stop()
