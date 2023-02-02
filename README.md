# PyMT5
[![version](https://img.shields.io/pypi/v/pymt5.svg)](https://pypi.org/project/pymt5)
[![pyversion](https://img.shields.io/pypi/pyversions/pymt5.svg)](#)
[![platform](https://img.shields.io/badge/platform-linux|%20win-lightgray.svg)](#platform-availability)
[![license](https://img.shields.io/pypi/l/pymt5.svg)](https://github.com/devcartel/pymt5/blob/master/LICENSE.txt)
[![downloads](https://img.shields.io/pypi/dm/pymt5.svg)](https://pypi.org/project/pymt5)
[![Sponsor](https://img.shields.io/badge/Sponsor%20PyMT5-%2419.99%2Fmonth-orange.svg?style=social&logo=paypal)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=CKHUBNTFNDCB8)

Provides simplified, multithreaded, socket-based Python interfaces to MT5 gateways. PyMT5 requires a [DevCartel MT5 gateway](https://github.com/devcartel/devcartelgateway64) installed on the MT5 platform to work with PyMT5.

<p align="center">
    <img src="https://user-images.githubusercontent.com/3415706/119602202-db221780-be14-11eb-859b-356969930613.png" alt="application" width="800"/>
</p>

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
                        'res':'0'})

m = pymt5.PyMT5()
m.onConnected = onConnected
m.onDisconnected = onDisconnected
m.onData = onData

```

Checkout more message [examples](https://github.com/devcartel/pymt5/tree/master/examples).

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

| Data type     | Header                 | Tags                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Login         | `'ver':'3','type':1'`  | `'login'`,`'password'`,`'res'`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Logout        | `'ver':'3','type':2'`  | _None_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Symbol        | `'ver':'3','type':3'`  | `'index'`,`'symbol'`,`'path'`,`'description'`,`'page'`,<br/>`'currency_base'`,`'currency_profit'`,`'currency_margin'`,<br/>`'digits'`,`'tick_flags'`,`'calc_mode'`,`'exec_mode'`,<br/>`'chart_mode'`,`'fill_flags'`,`'expir_flags'`,`'tick_value'`,<br/>`'tick_size'`,`'contract_size'`,`'volume_min'`,`'volume_max'`,<br/>`'volume_step'`,`'market_depth'`,`'margin_flags'`,<br/>`'margin_initial'`,`'margin_maintenance'`,`'margin_long'`,<br/>`'margin_short'`,`'margin_limit'`,<br/>`'margin_stop'`,`'margin_stop_limit'`,`'settlement_price'`,<br/>`'price_limit_max'`,`'price_limit_min'`,`'time_start'`,<br/>`'time_expiration'`,`'trade_mode'` |
| Tick          | `'ver':'3','type':4'`  | `'symbol'`,`'bank'`,`'bid'`,`'ask'`,`'last'`,`'volume'`,`'datetime'`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Order         | `'ver':'3','type':5'`  | `'symbol'`,`'bank'`,`'bid'`,`'ask'`,`'last'`,`'volume'`,`'datetime'`,<br/>`'order_action'`,`'state'`,`'order'`,`'exchange_id'`,<br/>`'custom_data'`,`'request_id'`,`'symbol'`,`'login'`,<br/>`'type_order'`,`'type_time'`,`'type_fill'`,`'action'`,`'price_order'`,<br/>`'price_sl'`,`'price_tp'`,`'price_tick_bid'`,`'price_tick_ask'`,<br/>`'volume'`,`'expiration_time'`,`'result'`                                                                                                                                                                                                                                                                               |
| Heartbeat     | `'ver':'3','type':6'`  | _None_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Deal          | `'ver':'3','type':7'`  | `'exchange_id'`,`'order'`,`'symbol'`,`'login'`,`'type_deal'`,<br/>`'volume'`,`'volume_rem'`,`'price'`,`'position'`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| External Deal | `'ver':'3','type':50'` | `'exchange_id'`,`'order'`,`'symbol'`,`'login'`,`'type_deal'`,<br/>`'volume'`,`'volume_rem'`,`'price'`,`'datetime'`,`'comment'`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

## Support
* Get a [DevCartel MT5 Gateway](http://devcartel.com/devcartelgateway64) in order to work with PyMT5
* Report an issue in [issue tracker](https://github.com/devcartel/pymt5/issues)

## Changelog
1.4.0
* 30 October 2022
* Fix potential data loss due to data fragmentation
 
1.3.0
* 8 August 2021
* Fix parsing data buffer

1.2.0
* 8 July 2019
* Support for Python 3.7
* Update support links
* Add examples

1.1.0
* 21 April 2018
* Released on PyPI
* Added README

1.0.0
* 13 April 2018
* Initial release
