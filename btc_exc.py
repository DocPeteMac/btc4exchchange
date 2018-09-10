import requests
import json
import datetime
import gdax
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup


def get_coin_data(exchange_site):
    """
    :param exchange_site:
    :return: json data as a dict
    """
    exchange_data = requests.get(exchange_site)
    exchange_data_py_obj = json.loads(exchange_data.text)
    return exchange_data_py_obj


def status_code():
    """
    :return: response.status_code
    """
    try:
        response = requests.get("http://www.google.com")
        print("response code: " + str(response.status_code))
    except requests.ConnectionError:
        print("Could not connect to the internet")


def data_type():
    """
    check the type
    :return: type exchange_data_obj
    """
    # type(exchange_dat_obj)
    pass


def usd_btc_info():
    """
    find the USD price from the web site and
    extract the price as number (digit str)
    :return:
    """
    requ = requests.get("https://bitcoin.info/price/USD")
    con = requ.content
    soup = BeautifulSoup(con, 'html.parser')
    price = soup.find_all("div", {"id" : "currencypageprice"})
    p = price[0].find_all('b')[0].text
    return p


def conv_str_in_flt():
    """
    convert the text str in a float number
    :return: float number
    """
    pl = []
    for i in usd_btc_info():
        if i == ',':
            continue
        pl.append(i)
    npl = ''
    pr = npl.join(pl)
    fpr = float(pr)
    return fpr


def current_utc_time():
    """
    UTC time in seconds since Epoch
    :return: UTC time now
    """
    utc_time = datetime.datetime.timestamp(datetime.datetime.utcnow())
    return utc_time


def utc_in_string():
    """
    converting into a string
    :return: UTC time string
    """
    return datetime.datetime.fromtimestamp(current_utc_time()).strftime('%c')


def current_local_time():
    """
    local time in seconds since Epoch
    :return: local time
    """
    local_time = datetime.datetime.timestamp(datetime.datetime.now())
    return local_time


def local_in_string():
    """
    converting Epoch seconds into a string
    :return: local to a string
    """
    return datetime.datetime.fromtimestamp(current_local_time()).strftime('%c')



# status_code()
# print("Collecting data from the Exchanges")
# time.sleep(3)


def coin_market_cap():
    """ Coin Market Cap (cmc) data """
    cmc = get_coin_data("https://api.coinmarketcap.com/v2/ticker/1/?convert=USD")
    cmc_btc = float(cmc['data']['quotes']['USD']['price'])
    return cmc_btc


def bittrex():
    """ Bittrex data """
    bittrex = get_coin_data("https://bittrex.com/api/v1.1/public/getticker?market=usdt-btc")
    bittrex_btc = float(bittrex['result']['Last'])
    return bittrex_btc


def binance():
    """ Binance data """
    binance = get_coin_data("https://api.binance.com/api/v3/ticker/price")
    ind = -1
    for i in binance:
        ind += 1
        if i['symbol'] == 'BTCUSDT':
            ind_btcusdt = ind
    binance_btc = float(binance[ind_btcusdt]['price'])
    return binance_btc


def poloniex():
    """Poloniex data """
    poloniex = get_coin_data("https://poloniex.com/public?command=returnTicker")
    poloniex_btc = float(poloniex['USDT_BTC']['last'])
    return poloniex_btc


def kraken():
    """ Kraken data """
    kraken = get_coin_data("https://api.kraken.com/0/public/Ticker?pair=xbtusd")
    kraken_btc = float(kraken['result']['XXBTZUSD']['c'][0])
    return kraken_btc


def hitbtc():
    """ Hitbtc data """
    hitbtc = get_coin_data("https://api.hitbtc.com/api/2/public/ticker/BTCUSD")
    hitbtc_btc = float(hitbtc['last'])
    return hitbtc_btc


def bitstamp():
    """ Bitstamp data """
    bitstamp = get_coin_data("https://www.bitstamp.net/api/ticker/")
    bitstamp_btc = float(bitstamp['last'])
    return bitstamp_btc


def bitfinex():
    """ Bitfinex data """
    bitfinex = get_coin_data("https://api.bitfinex.com/v1/pubticker/btcusd")
    bitfinex_btc = float(bitfinex['mid'])
    return bitfinex_btc


def coinbase_pro():
    """ Coinbase Pro data """
    public_client = gdax.PublicClient()
    tic = public_client.get_product_ticker(product_id='BTC-USD')
    coinbase_btc = float(tic['price'])
    return coinbase_btc


def btc_data_table():
    conn = sqlite3.connect("exchanges.db")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS btc_data(_id INTEGER PRIMARY KEY, utc REAL, loc_time REAL, cmc REAL,'
                'bittrex REAL, binance REAL, poloniex REAL, kraken REAL, hitbtc REAL, bitstamp REAL, bitfinex REAL,'
                'coinbase REAL)')
    conn.commit()
    conn.close()


def insert_btc_data(utc, loc_time, cmc, bittrex, binance, poloniex, kraken, hitbtc, bitstamp, bitfinex, coinbase):
    conn = sqlite3.connect("exchanges.db")
    cur = conn.cursor()
    cur.execute('INSERT INTO btc_data VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (utc, loc_time, cmc, bittrex, binance, poloniex, kraken, hitbtc, bitstamp, bitfinex, coinbase))
    conn.commit()
    conn.close()


def view_btc_data():
    conn = sqlite3.connect("exchanges.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM btc_data")
    rows = cur.fetchall()
    conn.close()
    return rows


def btc_diff_table():
    conn = sqlite3.connect("exchanges.db")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS btc_diff(_id INTEGER PRIMARY KEY, utc REAL, loc_time REAL,'
                'difference_procent REAL, maximum_exch REAL, maximum_cur REAL, minimum_exch REAL, minimum_cur REAL)')
    conn.commit()
    conn.close()


def insert_diff_data(utc, loc_time, difference_procent, maximum_exc, maximum_cur, minimum_exc, minimum_cur):
    conn = sqlite3.connect("exchanges.db")
    cur = conn.cursor()
    cur.execute('INSERT INTO btc_diff VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)',
                (utc, loc_time, difference_procent, maximum_exc, maximum_cur, minimum_exc, minimum_cur))
    conn.commit()
    conn.close()


def view_diff_data():
    conn = sqlite3.connect("exchanges.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM btc_diff")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_exch_btc_data():
    conn = sqlite3.connect('exchanges.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM btc_data")
    rows = cur.fetchall()
    conn.close()
    return rows


# for lines in get_exch_btc_data():
#     print(lines)
# print(type(lines))


def btc_data_db():
    df2 = pd.DataFrame(get_exch_btc_data(), columns=['_id', 'utc', 'loc_time', 'cmc', 'bittrex', 'binance', 'poloniex',
                                                     'kraken', 'hitbtc', 'bitstamp', 'bitfinex', 'coinbase'])
    return df2


def get_last_data_row():
    """
     get the last row of the records
    :return: the last row of data
    """
    last_data_row = len(btc_data_db()) - 1
    lr = btc_data_db().loc[last_data_row]
    return lr


def exch_data_only():
    """
    extract the exchange data only = create a pandas series
    :return: pandas series
    """
    ex_data_only = get_last_data_row()[4:]
    return ex_data_only


def get_data_average():
    """
    get the average of the current data
    :return: the average btc price at the current time
    """
    return exch_data_only().mean(axis=0)


def max_last_val():
    """
    get max value
    :return: last maximum value
    """
    l_max_val = exch_data_only().max()
    return l_max_val


def min_last_val():
    """
    get min value
    :return: last minimal value
    """
    l_min_val = exch_data_only().min()
    return l_min_val


def get_columns():
    """
    invert / (transpose) the data and the index to grab the column name of the value (max or min)
    important: keep the order
    :return: new transposed series
    """
    new_ser = pd.Series(data=['bittrex', 'binance', 'poloniex','kraken', 'hitbtc', 'bitstamp', 'bitfinex', 'coinbase'],
                        index=exch_data_only())
    return new_ser


def last_max_exch():
    """
    name of the maximum value exchange
    :return: exchange name
    """
    max_exch = get_columns()[max_last_val()]
    return max_exch


def last_min_exch():
    """
    name of the minimum value exchange
    :return: exchange name
    """
    min_exch = get_columns()[min_last_val()]
    return min_exch


def diff_procent_max_val():
    sum1 = max_last_val() + min_last_val()
    return (100 / sum1) * max_last_val()


def diff_procent_min_val():
    sum2 = max_last_val() + min_last_val()
    return (100 / sum2) * min_last_val()


def diff_val_btc():
    return max_last_val() - min_last_val()


def diff_procent_last():
    return diff_procent_max_val() - diff_procent_min_val()


def last_cmc():
    return get_last_data_row()[3]


def last_bittrex():
    return exch_data_only()[0]


def last_binance():
    return exch_data_only()[1]


def last_poloniex():
    return exch_data_only()[2]


def last_kraken():
    return exch_data_only()[3]


def last_hitbtc():
    return exch_data_only()[4]


def last_bitstamp():
    return exch_data_only()[5]


def last_bitfinex():
    return exch_data_only()[6]


def last_coinbase():
    return exch_data_only()[7]


btc_data_table()
# store new records in the exchange data base
insert_btc_data(current_utc_time(), current_local_time(), coin_market_cap(), bittrex(), binance(), poloniex(),
                kraken(), hitbtc(), bitstamp(), bitfinex(), coinbase_pro())

btc_diff_table()
# store new records in the difference data base
insert_diff_data(current_utc_time(), current_local_time(), diff_procent_last(), last_max_exch(),
                 max_last_val(), last_min_exch(), min_last_val())


# print("\nLocal time in Texas is:")
# print("{}\n".format(datetime.datetime.now().strftime("%A %x %X")))

# for i in view_btc_data():
#     print(i)
#
# for j in view_diff_data():
#     print(j)

# last_cmc()



