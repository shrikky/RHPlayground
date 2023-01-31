import config
import robin_stocks.robinhood as rh
import datetime as dt
import time
import trade_strat

def login(days):
    time_logged_in = 60*60*24*days
    rh.authentication.login(username=config.USERNAME,
                            password=config.PASSWORD,
                            expiresIn=time_logged_in,
                            scope='internal',
                            by_sms=True,
                            store_session=True)

def logout():
    rh.authentication.logout()

def get_stocks():
    stocks = list()
    stocks.append('AAPL')
    stocks.append('ABBV')
    stocks.append('O')
    return(stocks)

def open_market():
    market = True
    time_now = dt.datetime.now().time()

    market_open = dt.time(9,30,0)
    market_close = dt.time(15,59,0)

    if time_now > market_open and time_now < market_close:
        market = True
    return market

if __name__ == "__main__":
    login(1)
    stocks = get_stocks()
    #print('stocks',stocks)
    ts = trade_strat.trader(stocks)

    while open_market():
        prices = rh.stocks.get_latest_price(stocks)

        for i, stock in enumerate(stocks):
            price = float(prices[i])
            print('{} = ${}'.format(stock,price))

            data = ts.get_historical_price(stock,span='day')
            time.sleep(30)
    logout()