import requests


def main():
    data = requests.get('https://www.modularfinance.se/api/puzzles/index-trader.json').json()

    best_trade_lowest = None
    best_trade_highest = None
    best_trade = None

    local_lowest = None
    local_highest = None
    local_best_trade = None

    for v in data['data']:
        if local_lowest is None or v['low'] < local_lowest['low']:
            local_lowest = v
            local_highest = None

        if local_highest is None or v['high'] > local_highest['high']:
            local_highest = v
            local_best_trade = local_highest['high'] - local_lowest['low']

        if best_trade is None or local_best_trade > best_trade:
            best_trade = local_best_trade
            best_trade_lowest = local_lowest
            best_trade_highest = local_highest

    print 'Buy at date ', best_trade_lowest['quote_date'], " at price ", best_trade_lowest['low']
    print 'Sell at date ', best_trade_highest['quote_date'], " at price ", best_trade_highest['high']

    profit_percentage = ((best_trade_highest['high'] - best_trade_lowest['low']) / best_trade_lowest['low']) * 100
    print 'Percentage profit %.2f %%' % profit_percentage

if __name__ == "__main__":
    main()
