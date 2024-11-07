import ccxt

# Инициализация биржи Binance
binance = ccxt.binance()

# Получение последних 100 сделок BTC/USDT
trades = binance.fetch_trades("BTC/USDT", limit=100)

# Парсинг и вывод информации о покупателях (мейкер/тейкер)
for trade in trades:
    print(trade.keys())

    print(trade["datetime"])

    # print({
    #     'timestamp': trade['timestamp'],
    #     'datetime': trade['datetime'],
    #     'price': trade['price'],
    #     'amount': trade['amount'],
    #     'side': trade['side'],  # buy/sell
    #     'makerOrTaker': trade['takerOrMaker']  # taker/maker
    # })
