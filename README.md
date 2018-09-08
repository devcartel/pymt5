# PyMT5
[![version](https://img.shields.io/pypi/v/pymt5.svg)](https://pypi.org/project/pymt5)
[![pyversion](https://img.shields.io/pypi/pyversions/pymt5.svg)](#)
[![platform](https://img.shields.io/badge/platform-linux|%20win-lightgray.svg)](#platform-availability)
[![license](https://img.shields.io/pypi/l/pymt5.svg)](https://github.com/devcartel/pymt5/blob/master/LICENSE.txt)

Provides simplified, multithreaded, socket-based Python interfaces to MT5 gateways. PyMT5 requires a [DevCartel MT5 gateway](http://devcartel.com/devcartelgateway64) installed in the MT5 platform to work with PyMT5.

![application](http://media.virbcdn.com/cdn_images/resize_1024x1365/d3/bbfed93e2dab1106-ScreenShot2018-09-08at102030.png)

## Installation
PyMT5 supports both Python 2 and 3. Simply install from [PyPI](https://pypi.org/project/pymt5) using `pip`:

    pip install pymt5

## Example
```python
import pymt5

def onData(data):
    client = data.get('client_id')
    # Login
    if data.get('type') == '1':
        # Send heartbeat
        m.send(client, {'ver':'3','type':'6'})
        # Send login OK response
        m.send(client, {'ver':'3',
                        'type':'1',
                        'login':data.get('login'),
                        'password':data.get('password'),
                        'res','0'})

m = pymt5.PyMT5()
m.onConnected = onConnected
m.onDisconnected = onDisconnected
m.onData = onData

```

## API
__pymt5.PyMT5([_host=''_], [_port=16838_])__  
_host: str_  
_port: int_  
_➥return: object_  
Starts a PyMT5 server and listening on a port defined by _port_.

    >> m = pymt5.PyMT5()

Upon incoming connection from a gateway, PyMT5 stores client information in `pymt5.requests` in dict format as 

__pymt5.stop()__  
Disconnects all MT5 gateway connections and stop the server.

    >> m.stop()

__pymt5.broadcast(_data_)__  
_data: dict_  
Sends a message to all connected gateways. Consider using this when sending market data.
    
    >> #send a tick
    >> m.broadcast({'ver':'3','type':'4','symbol':'EURUSD.TEST','bank':'dc','bid':'1.2661','ask':'1.2665','last':'1.2665','volume':'1','datetime':'0'})

__pymt5.send(<i>client_id</i>, _data_)__  
<i>client_id: int</i>  
_data: dict_  
Sends a message to a connected gateway.

    >> #send heartbeat
    >> m.send(123145536110592, {'ver':'3','type':'6'})

__pymt5.disconnect(<i>client_id</i>)__  
<i>client_id: int</i>  
Terminates a connection.

    >> m.disconnect(123145536110592)

__pymt5.onConnected(<i>client_info</i>)__  
<i>client_info: dict</i>  
A callback `onConnected`, if assigned, is called upon a successful connection from a client. Client information can be accessed from `client_info`'s values as `client_id`, `client_address` and `client_port`.

    >> def onConnected(client_info):
    >>     print(str(client_info))
    >>     # print {'client_port': 64941, 'client_address': '127.0.0.1', 'client_id': 123145536110592}
    >>
    >> m = pymt5.PyMT5()
    >> m.onConnected = onConnected
    
__pymt5.onDisconnected(<i>client_info</i>)__   
<i>client_info: dict</i>  
A callback `onDisconnected`, if assigned, is called upon a disconnection from a client. Client information can be accessed from `client_info`'s values as `client_id`, `client_address` and `client_port`.

    >> def onDisonnected(client_info):
    >>     print(str(client_info))
    >>
    >> m = pymt5.PyMT5()
    >> m.onDisconnected = onDisconnected

__pymt5.onData(_data_)__  
_data: dict_  
A callback `onData`, if assigned, is called upon receiving messages from gateways. See [Data Format](#data-format) for more information.

    >> def onData(data):
    >>     print(json.dumps(data))
    >>
    >> m = pymt5.PyMT5()
    >> m.onData = onData

## Data Format
Data is to be composed as a dict with key/value defined below to be sent and received from a gateway.

Data type       | Header                | Tags
----------------|-----------------------|------
Login           | `'ver':'3','type':1'` | `'login'`,`'password'`,`'res'`
Logout          | `'ver':'3','type':2'` | _None_
Symbol          | `'ver':'3','type':3'` | `'index'`,`'symbol'`,`'path'`,`'description'`,`'page'`,`'currency_base'`,<br />`'currency_profit'`,`'currency_margin'`,`'digits'`,`'tick_flags'`,<br />`'calc_mode'`,`'exec_mode'`,`'chart_mode'`,`'fill_flags'`,<br />`'expir_flags'`,`'tick_value'`,`'tick_size'`,`'contract_size'`,<br />`'volume_min'`,`'volume_max'`,`'volume_step'`,`'market_depth'`,<br />`'margin_flags'`,`'margin_initial'`,`'margin_maintenance'`,<br />`'margin_long'`,`'margin_short'`,`'margin_limit'`,`'margin_stop'`,<br />`'margin_stop_limit'`,`'settlement_price'`,`'price_limit_max'`,<br />`'price_limit_min'`,`'time_start'`,`'time_expiration'`,`'trade_mode'`
Tick            | `'ver':'3','type':4'` | `'symbol'`,`'bank'`,`'bid'`,`'ask'`,`'last'`,`'volume'`,`'datetime'`
Order           | `'ver':'3','type':5'` | `'symbol'`,`'bank'`,`'bid'`,`'ask'`,`'last'`,`'volume'`,`'datetime'`,<br />`'order_action'`,`'state'`,`'order'`,`'exchange_id'`,`'custom_data'`,<br />`'request_id'`,`'symbol'`,`'login'`,`'type_order'`,`'type_time'`,<br />`'action'`,`'price_order'`,`'price_sl'`,`'price_tp'`,`'price_tick_bid'`,<br />`'price_tick_ask'`,`'volume'`,`'expiration_time'`,`'result'`
Heartbeat       | `'ver':'3','type':6'` | _None_
Deal            | `'ver':'3','type':7'` | `'exchange_id'`,`'order'`,`'symbol'`,`'login'`,`'type_deal'`,`'volume'`,<br />`'volume_rem'`,`'price'`
External Deal   | `'ver':'3','type':50'`| `'exchange_id'`,`'order'`,`'symbol'`,`'login'`,`'type_deal'`,`'volume'`,<br />`'volume_rem'`,`'price'`,`'datetime'`

## Support
* Get a [DevCartel MT5 Gateway](http://devcartel.com/devcartelgateway64) in order to work with PyMT5
* Report an issue in [issue tracker](https://github.com/devcartel/pymt5/issues)

## Changelog
1.1.0
* 21 April 2018
* Released on PyPI
* Added README

1.0.0
* 13 April 2018
* Initial release
