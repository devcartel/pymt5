import sys
sys.path.append('../')
import pymt5
import time
import signal
from collections import OrderedDict

client = ''
order = deal = OrderedDict()
m = None

def onConnected(client_info):
    global client
    client = client_info.get('client_id')
    print('[onConnected] client_address: ' + str(client_info))

def onDisconnected(client_info):
    global client
    client = ''
    print('[onDisconnected] client_address: ' + str(client_info))

def sendOrderConfirmed(client, order):
    order.update({'exchange_id':str(int(time.time()))})
    if order['type_order'] == '0':
        order.update({'price_order':'1.2665'})
    else:
        order.update({'price_order':'1.2661'})
    order.update({'state':'1'})
    order.update({'result':'10009'})
    m.send(client, order)

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

def sendDeal(client, order, price):
    global deal
    deal =  OrderedDict([('ver','3'),
                         ('type','7'),
                         ('exchange_id',str(int(time.time()))),
                         ('order',order['order']),
                         ('symbol',order['symbol']),
                         ('login',order['login']),
                         ('type_deal',order['type_order']),
                         ('volume',order['volume']),
                         ('volume_rem','0'),
                         ('price',price)])
    m.send(client, deal)

def sendDealExternal(client):
    m.send(client, OrderedDict([('ver','3'),('type','50'),('exchange_id',str(int(time.time()))),('order','0'),('symbol','XAUUSD.G9'),('login','1000014'),('type_deal','0'),('volume','1'),('volume_rem','0'),('price','1344.80')]))

def sendTick():
    m.broadcast(OrderedDict([('ver','3'),('type','4'),('symbol','EURUSD.TEST'),('bank','dc'),('bid','1.2661'),('ask','1.2665'),('last','1.2665'),('volume','1'),('datetime','0')]))

def onData(data):
    client = data.get('client_id')
    # Login
    if data.get('type') == '1':
        print('[onData] data: ' + str(data))
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
        m.send(client, OrderedDict([('ver','3'),
                                    ('type','3'),
                                    ('index','0'),
                                    ('symbol','XAUUSD.G9'),
                                    ('path','TestExchange'),
                                    ('description','test'),
                                    ('page','http://www.google.co/finance?q=XAUUSD.TEST'),
                                    ('currency_base','USD'),
                                    ('currency_profit','USD'),
                                    ('currency_margin','USD'),
                                    ('digits','2'),
                                    ('tick_flags','7'),
                                    ('calc_mode','0'),
                                    ('exec_mode','2'),
                                    ('chart_mode','0'),
                                    ('fill_flags','3'),
                                    ('expir_flags','15'),
                                    ('tick_value','0.00000'),
                                    ('tick_size','0.00000'),
                                    ('contract_size','100'),
                                    ('volume_min','0.10'),
                                    ('volume_max','100.00'),
                                    ('volume_step','0.01'),
                                    ('market_depth','0'),
                                    ('margin_flags','0'),
                                    ('margin_initial','0.00'),
                                    ('margin_maintenance','0.00'),
                                    ('margin_long','1.00'),
                                    ('margin_short','1.00'),
                                    ('margin_limit','0.00'),
                                    ('margin_stop','0.00'),
                                    ('margin_stop_limit','0.00'),
                                    ('settlement_price','0.00'),
                                    ('price_limit_max','0.00'),
                                    ('price_limit_min','0.00'),
                                    ('time_start','0'),
                                    ('time_expiration','0'),               
                                    ('trade_mode','4')]))
        # Send a tick
        sendTick()
    # New order
    elif data.get('type') == '5' and data.get('state') == '0':
        print('[onData] data: ' + str(data))
        global deal
        global order
        order = data
        del order['client_id']
#        sendOrderConfirmed(client, order)
#        sendOrderPlaced(client, order)
#        sendOrderNew(client, order)
#        time.sleep(0.1)

m = pymt5.PyMT5()
m.onConnected = onConnected
m.onDisconnected = onDisconnected
m.onData = onData



# Flow on new order
# sendOrderPlaced -> sendOrderNew -> sendDeal

#m.send(client, OrderedDict([('ver','3'),('type','7'),('exchange_id','3'),('order','4056'),('symbol','EURUSD.TEST'),('login','1000014'),('type_deal','0'),('volume','1'),('volume_rem','1'),('price','1.2665')]))
#
#OrderedDict([('ver', '3'), ('type', '5'), ('order_action', '1'), ('state', '0'), ('order', '4059'), ('exchange_id', '0'), ('custom_data', '0'), ('request_id', '12995002'), ('symbol', 'EURUSD.TEST'), ('login', '1000014'), ('type_order', '0'), ('type_time', '0'), ('action', '3'), ('price_order', '0.00000'), ('price_sl', '0.00000'), ('price_tp', '0.00000'), ('price_tick_bid', '0.00000'), ('price_tick_ask', '0.00000'), ('volume', '0'), ('expiration_time', '0'), ('result', '0'), ('client_id', 140558617073408)])
#
#m.send(client, OrderedDict([('ver', '3'), ('type', '5'), ('order_action', '1'), ('state', '2'), ('order', '4059'), ('exchange_id', '2'), ('custom_data', '0'), ('request_id', '12995002'), ('symbol', 'EURUSD.TEST'), ('login', '1000014'), ('type_order', '0'), ('type_time', '0'), ('action', '3'), ('price_order', '0.00000'), ('price_sl', '0.00000'), ('price_tp', '0.00000'), ('price_tick_bid', '0.00000'), ('price_tick_ask', '0.00000'), ('volume', '0'), ('expiration_time', '0'), ('result', '0')]))

#      ORDER_STATE_UNKNOWN          =0,          // undefined state
#      ORDER_STATE_CONFIRMED        =1,          // order confirmed
#      ORDER_STATE_REQUEST_PLACED   =2,          // order generation request placed
#      ORDER_STATE_NEW              =3,          // create a new order
#      ORDER_STATE_REJECT_NEW       =4,          // order rejected
#      ORDER_STATE_DEAL             =5,          // a deal by order sent
#      ORDER_STATE_REQUEST_MODIFY   =6,          // order modification request received
#      ORDER_STATE_MODIFY           =7,          // order modified
#      ORDER_STATE_REJECT_MODIFY    =8,          // order modification rejected
#      ORDER_STATE_REQUEST_CANCEL   =9,          // order cancelation request received
#      ORDER_STATE_CANCEL           =10,         // order canceled
#      ORDER_STATE_REJECT_CANCEL    =11,         // order cancelation rejected
#      ORDER_STATE_COMPLETED        =20          // operation on the order complete, can be removed from the queue

#define MSG_TAG_ORDER_ACTION_TYPE         "order_action="         // order action
#define MSG_TAG_ORDER_STATE               "state="                // order state
#define MSG_TAG_ORDER_MT_ID               "order="                // order ticket
#define MSG_TAG_ORDER_EXCHANGE_ID         "exchange_id="          // order id in external system
#define MSG_TAG_ORDER_CUSTOM_DATA         "custom_data="          // custom data
#define MSG_TAG_ORDER_REQUEST_ID          "request_id="           // request id
#define MSG_TAG_ORDER_SYMBOL              "symbol="               // symbol
#define MSG_TAG_ORDER_LOGIN               "login="                // client's login
#define MSG_TAG_ORDER_TYPE_ORDER          "type_order="           // order type
#define MSG_TAG_ORDER_TYPE_TIME           "type_time="            // order expiration type
#define MSG_TAG_ORDER_ACTION              "action="               // action
#define MSG_TAG_ORDER_PRICE_ORDER         "price_order="          // order price
#define MSG_TAG_ORDER_PRICE_SL            "price_sl="             // Stop Loss level
#define MSG_TAG_ORDER_PRICE_TP            "price_tp="             // Take Profit level
#define MSG_TAG_ORDER_PRICE_TICK_BID      "price_tick_bid="       // symbol bid price in external trading system
#define MSG_TAG_ORDER_PRICE_TICK_ASK      "price_tick_ask="       // symbol ask price in external trading system
#define MSG_TAG_ORDER_VOLUME              "volume="               // order volume
#define MSG_TAG_ORDER_EXPIRATION_TIME     "expiration_time="      // expiration time
#define MSG_TAG_ORDER_RESULT              "result="               // result of message processing

#//+------------------------------------------------------------------+
#//| Deal message tags                                                |
#//+------------------------------------------------------------------+
#define MSG_TAG_DEAL_EXCHANGE_ID          "exchange_id="          // deal id in external system
#define MSG_TAG_DEAL_ORDER                "order="                // order ticket
#define MSG_TAG_DEAL_SYMBOL               "symbol="               // symbol
#define MSG_TAG_DEAL_LOGIN                "login="                // login
#define MSG_TAG_DEAL_TYPE                 "type_deal="            // action
#define MSG_TAG_DEAL_VOLUME               "volume="               // volume
#define MSG_TAG_DEAL_VOLUME_REM           "volume_rem="           // volume remaind
#define MSG_TAG_DEAL_PRICE                "price="                // price


#//--- form the string value of order action type
#   switch(order.action)
#     {
#      case IMTRequest::TA_PRICE              : res.Assign(L"prices for");                 break;
#      case IMTRequest::TA_REQUEST            : res.Assign(L"request");                    break;
#      case IMTRequest::TA_INSTANT            : res.Assign(L"instant");                    break;
#      case IMTRequest::TA_MARKET             : res.Assign(L"market");                     break;
#      case IMTRequest::TA_EXCHANGE           : res.Assign(L"exchange");                   break;
#      case IMTRequest::TA_PENDING            : res.Assign(L"pending");                    break;
#      case IMTRequest::TA_SLTP               : res.Assign(L"modify");                     break;
#      case IMTRequest::TA_MODIFY             : res.Assign(L"modify");                     break;
#      case IMTRequest::TA_REMOVE             : res.Assign(L"cancel");                     break;
#      case IMTRequest::TA_ACTIVATE           : res.Assign(L"activate");                   break;
#      case IMTRequest::TA_ACTIVATE_SL        : res.Assign(L"activate stop loss");         break;
#      case IMTRequest::TA_ACTIVATE_TP        : res.Assign(L"activate take profit");       break;
#      case IMTRequest::TA_ACTIVATE_STOPLIMIT : res.Assign(L"activate stop-limit order");  break;
#      case IMTRequest::TA_STOPOUT_ORDER      : res.Assign(L"delete stop-out order");      break;
#      case IMTRequest::TA_STOPOUT_POSITION   : res.Assign(L"close stop-out position");    break;
#      case IMTRequest::TA_EXPIRATION         : res.Assign(L"expire");                     break;
#      default                                : res.Assign(L"order");                      break;
#     }

#//+------------------------------------------------------------------+
#//| Position message tags                                            |
#//+------------------------------------------------------------------+
#define MSG_TAG_POSITION_SYMBOL           "pos_symbol="           // symbol
#define MSG_TAG_POSITION_LOGIN            "pos_login="            // client's login
#define MSG_TAG_POSITION_PRICE            "pos_price="            // position opening price
#define MSG_TAG_POSITION_VOLUME           "pos_volume="           // position volume
#define MSG_TAG_POSITION_DIGITS           "pos_digits="           // price digits
