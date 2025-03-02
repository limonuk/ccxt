# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import InvalidNonce
from ccxt.base.precise import Precise


class bitbank(Exchange):

    def describe(self):
        return self.deep_extend(super(bitbank, self).describe(), {
            'id': 'bitbank',
            'name': 'bitbank',
            'countries': ['JP'],
            'version': 'v1',
            'has': {
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchDepositAddress': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTrades': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '4h': '4hour',
                '8h': '8hour',
                '12h': '12hour',
                '1d': '1day',
                '1w': '1week',
            },
            'hostname': 'bitbank.cc',
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/37808081-b87f2d9c-2e59-11e8-894d-c1900b7584fe.jpg',
                'api': {
                    'public': 'https://public.{hostname}',
                    'private': 'https://api.{hostname}',
                    'markets': 'https://api.{hostname}',
                },
                'www': 'https://bitbank.cc/',
                'doc': 'https://docs.bitbank.cc/',
                'fees': 'https://bitbank.cc/docs/fees/',
            },
            'api': {
                'public': {
                    'get': [
                        '{pair}/ticker',
                        '{pair}/depth',
                        '{pair}/transactions',
                        '{pair}/transactions/{yyyymmdd}',
                        '{pair}/candlestick/{candletype}/{yyyymmdd}',
                    ],
                },
                'private': {
                    'get': [
                        'user/assets',
                        'user/spot/order',
                        'user/spot/active_orders',
                        'user/spot/trade_history',
                        'user/withdrawal_account',
                    ],
                    'post': [
                        'user/spot/order',
                        'user/spot/cancel_order',
                        'user/spot/cancel_orders',
                        'user/spot/orders_info',
                        'user/request_withdrawal',
                    ],
                },
                'markets': {
                    'get': [
                        'spot/pairs',
                    ],
                },
            },
            'exceptions': {
                '20001': AuthenticationError,
                '20002': AuthenticationError,
                '20003': AuthenticationError,
                '20005': AuthenticationError,
                '20004': InvalidNonce,
                '40020': InvalidOrder,
                '40021': InvalidOrder,
                '40025': ExchangeError,
                '40013': OrderNotFound,
                '40014': OrderNotFound,
                '50008': PermissionDenied,
                '50009': OrderNotFound,
                '50010': OrderNotFound,
                '60001': InsufficientFunds,
                '60005': InvalidOrder,
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.marketsGetSpotPairs(params)
        #
        #     {
        #       "success": 1,
        #       "data": {
        #         "pairs": [
        #           {
        #             "name": "btc_jpy",
        #             "base_asset": "btc",
        #             "quote_asset": "jpy",
        #             "maker_fee_rate_base": "0",
        #             "taker_fee_rate_base": "0",
        #             "maker_fee_rate_quote": "-0.0002",
        #             "taker_fee_rate_quote": "0.0012",
        #             "unit_amount": "0.0001",
        #             "limit_max_amount": "1000",
        #             "market_max_amount": "10",
        #             "market_allowance_rate": "0.2",
        #             "price_digits": 0,
        #             "amount_digits": 4,
        #             "is_enabled": True,
        #             "stop_order": False,
        #             "stop_order_and_cancel": False
        #           }
        #         ]
        #       }
        #     }
        #
        data = self.safe_value(response, 'data')
        pairs = self.safe_value(data, 'pairs', [])
        result = []
        for i in range(0, len(pairs)):
            entry = pairs[i]
            id = self.safe_string(entry, 'name')
            baseId = self.safe_string(entry, 'base_asset')
            quoteId = self.safe_string(entry, 'quote_asset')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            maker = self.safe_number(entry, 'maker_fee_rate_quote')
            taker = self.safe_number(entry, 'taker_fee_rate_quote')
            pricePrecisionString = self.safe_string(entry, 'price_digits')
            priceLimit = self.parse_precision(pricePrecisionString)
            precision = {
                'price': int(pricePrecisionString),
                'amount': self.safe_integer(entry, 'amount_digits'),
            }
            active = self.safe_value(entry, 'is_enabled')
            minAmountString = self.safe_string(entry, 'unit_amount')
            minCost = Precise.string_mul(minAmountString, priceLimit)
            limits = {
                'amount': {
                    'min': self.safe_number(entry, 'unit_amount'),
                    'max': self.safe_number(entry, 'limit_max_amount'),
                },
                'price': {
                    'min': self.parse_number(priceLimit),
                    'max': None,
                },
                'cost': {
                    'min': self.parse_number(minCost),
                    'max': None,
                },
            }
            result.append({
                'info': entry,
                'id': id,
                'symbol': symbol,
                'baseId': baseId,
                'quoteId': quoteId,
                'base': base,
                'quote': quote,
                'precision': precision,
                'limits': limits,
                'active': active,
                'maker': maker,
                'taker': taker,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'timestamp')
        last = self.safe_number(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_number(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = await self.publicGetPairTicker(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_ticker(data, market)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        response = await self.publicGetPairDepth(self.extend(request, params))
        orderbook = self.safe_value(response, 'data', {})
        timestamp = self.safe_integer(orderbook, 'timestamp')
        return self.parse_order_book(orderbook, symbol, timestamp)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'executed_at')
        symbol = None
        feeCurrency = None
        if market is not None:
            symbol = market['symbol']
            feeCurrency = market['quote']
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        id = self.safe_string_2(trade, 'transaction_id', 'trade_id')
        takerOrMaker = self.safe_string(trade, 'maker_taker')
        fee = None
        feeCost = self.safe_number(trade, 'fee_amount_quote')
        if feeCost is not None:
            fee = {
                'currency': feeCurrency,
                'cost': feeCost,
            }
        orderId = self.safe_string(trade, 'order_id')
        type = self.safe_string(trade, 'type')
        side = self.safe_string(trade, 'side')
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': orderId,
            'type': type,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = await self.publicGetPairTransactions(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        trades = self.safe_value(data, 'transactions', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     [
        #         "0.02501786",
        #         "0.02501786",
        #         "0.02501786",
        #         "0.02501786",
        #         "0.0000",
        #         1591488000000
        #     ]
        #
        return [
            self.safe_integer(ohlcv, 5),
            self.safe_number(ohlcv, 0),
            self.safe_number(ohlcv, 1),
            self.safe_number(ohlcv, 2),
            self.safe_number(ohlcv, 3),
            self.safe_number(ohlcv, 4),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        date = self.milliseconds()
        date = self.ymd(date)
        date = date.split('-')
        request = {
            'pair': market['id'],
            'candletype': self.timeframes[timeframe],
            'yyyymmdd': ''.join(date),
        }
        response = await self.publicGetPairCandlestickCandletypeYyyymmdd(self.extend(request, params))
        #
        #     {
        #         "success":1,
        #         "data":{
        #             "candlestick":[
        #                 {
        #                     "type":"5min",
        #                     "ohlcv":[
        #                         ["0.02501786","0.02501786","0.02501786","0.02501786","0.0000",1591488000000],
        #                         ["0.02501747","0.02501953","0.02501747","0.02501953","0.3017",1591488300000],
        #                         ["0.02501762","0.02501762","0.02500392","0.02500392","0.1500",1591488600000],
        #                     ]
        #                 }
        #             ],
        #             "timestamp":1591508668190
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        candlestick = self.safe_value(data, 'candlestick', [])
        first = self.safe_value(candlestick, 0, {})
        ohlcv = self.safe_value(first, 'ohlcv', [])
        return self.parse_ohlcvs(ohlcv, market, timeframe, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetUserAssets(params)
        #
        #     {
        #       "success": "1",
        #       "data": {
        #         "assets": [
        #           {
        #             "asset": "jpy",
        #             "amount_precision": "4",
        #             "onhand_amount": "0.0000",
        #             "locked_amount": "0.0000",
        #             "free_amount": "0.0000",
        #             "stop_deposit": False,
        #             "stop_withdrawal": False,
        #             "withdrawal_fee": {
        #               "threshold": "30000.0000",
        #               "under": "550.0000",
        #               "over": "770.0000"
        #             }
        #           },
        #           {
        #             "asset": "btc",
        #             "amount_precision": "8",
        #             "onhand_amount": "0.00000000",
        #             "locked_amount": "0.00000000",
        #             "free_amount": "0.00000000",
        #             "stop_deposit": False,
        #             "stop_withdrawal": False,
        #             "withdrawal_fee": "0.00060000"
        #           },
        #         ]
        #       }
        #     }
        #
        result = {
            'info': response,
            'timestamp': None,
            'datetime': None,
        }
        data = self.safe_value(response, 'data', {})
        assets = self.safe_value(data, 'assets', [])
        for i in range(0, len(assets)):
            balance = assets[i]
            currencyId = self.safe_string(balance, 'asset')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'free_amount')
            account['used'] = self.safe_string(balance, 'locked_amount')
            account['total'] = self.safe_string(balance, 'onhand_amount')
            result[code] = account
        return self.parse_balance(result)

    def parse_order_status(self, status):
        statuses = {
            'UNFILLED': 'open',
            'PARTIALLY_FILLED': 'open',
            'FULLY_FILLED': 'closed',
            'CANCELED_UNFILLED': 'canceled',
            'CANCELED_PARTIALLY_FILLED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'order_id')
        marketId = self.safe_string(order, 'pair')
        symbol = None
        if marketId and not market and (marketId in self.markets_by_id):
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'ordered_at')
        price = self.safe_number(order, 'price')
        amount = self.safe_number(order, 'start_amount')
        filled = self.safe_number(order, 'executed_amount')
        remaining = self.safe_number(order, 'remaining_amount')
        average = self.safe_number(order, 'average_price')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        type = self.safe_string_lower(order, 'type')
        side = self.safe_string_lower(order, 'side')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'cost': None,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': order,
        })

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'amount': self.amount_to_precision(symbol, amount),
            'side': side,
            'type': type,
        }
        if type == 'limit':
            request['price'] = self.price_to_precision(symbol, price)
        response = await self.privatePostUserSpotOrder(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return self.parse_order(data, market)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'pair': market['id'],
        }
        response = await self.privatePostUserSpotCancelOrder(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return data

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'pair': market['id'],
        }
        response = await self.privateGetUserSpotOrder(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return self.parse_order(data, market)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        if limit is not None:
            request['count'] = limit
        if since is not None:
            request['since'] = int(since / 1000)
        response = await self.privateGetUserSpotActiveOrders(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        orders = self.safe_value(data, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        request = {}
        if market is not None:
            request['pair'] = market['id']
        if limit is not None:
            request['count'] = limit
        if since is not None:
            request['since'] = int(since / 1000)
        response = await self.privateGetUserSpotTradeHistory(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        trades = self.safe_value(data, 'trades', [])
        return self.parse_trades(trades, market, since, limit)

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'asset': currency['id'],
        }
        response = await self.privateGetUserWithdrawalAccount(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        # Not sure about self if there could be more than one account...
        accounts = self.safe_value(data, 'accounts', [])
        firstAccount = self.safe_value(accounts, 0, {})
        address = self.safe_string(firstAccount, 'address')
        return {
            'currency': currency,
            'address': address,
            'tag': None,
            'info': response,
        }

    async def withdraw(self, code, amount, address, tag=None, params={}):
        if not ('uuid' in params):
            raise ExchangeError(self.id + ' uuid is required for withdrawal')
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'asset': currency['id'],
            'amount': amount,
        }
        response = await self.privatePostUserRequestWithdrawal(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        txid = self.safe_string(data, 'txid')
        return {
            'info': response,
            'id': txid,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = self.omit(params, self.extract_params(path))
        url = self.implode_hostname(self.urls['api'][api]) + '/'
        if (api == 'public') or (api == 'markets'):
            url += self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce
            url += self.version + '/' + self.implode_params(path, params)
            if method == 'POST':
                body = self.json(query)
                auth += body
            else:
                auth += '/' + self.version + '/' + path
                if query:
                    query = self.urlencode(query)
                    url += '?' + query
                    auth += '?' + query
            headers = {
                'Content-Type': 'application/json',
                'ACCESS-KEY': self.apiKey,
                'ACCESS-NONCE': nonce,
                'ACCESS-SIGNATURE': self.hmac(self.encode(auth), self.encode(self.secret)),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None, config={}, context={}):
        response = await self.fetch2(path, api, method, params, headers, body, config, context)
        success = self.safe_integer(response, 'success')
        data = self.safe_value(response, 'data')
        if not success or not data:
            errorMessages = {
                '10000': 'URL does not exist',
                '10001': 'A system error occurred. Please contact support',
                '10002': 'Invalid JSON format. Please check the contents of transmission',
                '10003': 'A system error occurred. Please contact support',
                '10005': 'A timeout error occurred. Please wait for a while and try again',
                '20001': 'API authentication failed',
                '20002': 'Illegal API key',
                '20003': 'API key does not exist',
                '20004': 'API Nonce does not exist',
                '20005': 'API signature does not exist',
                '20011': 'Two-step verification failed',
                '20014': 'SMS authentication failed',
                '30001': 'Please specify the order quantity',
                '30006': 'Please specify the order ID',
                '30007': 'Please specify the order ID array',
                '30009': 'Please specify the stock',
                '30012': 'Please specify the order price',
                '30013': 'Trade Please specify either',
                '30015': 'Please specify the order type',
                '30016': 'Please specify asset name',
                '30019': 'Please specify uuid',
                '30039': 'Please specify the amount to be withdrawn',
                '40001': 'The order quantity is invalid',
                '40006': 'Count value is invalid',
                '40007': 'End time is invalid',
                '40008': 'end_id Value is invalid',
                '40009': 'The from_id value is invalid',
                '40013': 'The order ID is invalid',
                '40014': 'The order ID array is invalid',
                '40015': 'Too many specified orders',
                '40017': 'Incorrect issue name',
                '40020': 'The order price is invalid',
                '40021': 'The trading classification is invalid',
                '40022': 'Start date is invalid',
                '40024': 'The order type is invalid',
                '40025': 'Incorrect asset name',
                '40028': 'uuid is invalid',
                '40048': 'The amount of withdrawal is illegal',
                '50003': 'Currently, self account is in a state where you can not perform the operation you specified. Please contact support',
                '50004': 'Currently, self account is temporarily registered. Please try again after registering your account',
                '50005': 'Currently, self account is locked. Please contact support',
                '50006': 'Currently, self account is locked. Please contact support',
                '50008': 'User identification has not been completed',
                '50009': 'Your order does not exist',
                '50010': 'Can not cancel specified order',
                '50011': 'API not found',
                '60001': 'The number of possessions is insufficient',
                '60002': 'It exceeds the quantity upper limit of the tender buying order',
                '60003': 'The specified quantity exceeds the limit',
                '60004': 'The specified quantity is below the threshold',
                '60005': 'The specified price is above the limit',
                '60006': 'The specified price is below the lower limit',
                '70001': 'A system error occurred. Please contact support',
                '70002': 'A system error occurred. Please contact support',
                '70003': 'A system error occurred. Please contact support',
                '70004': 'We are unable to accept orders as the transaction is currently suspended',
                '70005': 'Order can not be accepted because purchase order is currently suspended',
                '70006': 'We can not accept orders because we are currently unsubscribed ',
                '70009': 'We are currently temporarily restricting orders to be carried out. Please use the limit order.',
                '70010': 'We are temporarily raising the minimum order quantity as the system load is now rising.',
            }
            errorClasses = self.exceptions
            code = self.safe_string(data, 'code')
            message = self.safe_string(errorMessages, code, 'Error')
            ErrorClass = self.safe_value(errorClasses, code)
            if ErrorClass is not None:
                raise ErrorClass(message)
            else:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response
