from flask import Flask, render_template, url_for
import btc_exc as be
import os

os.system('python btc_exc.py')

app = Flask(__name__)

def average():
    return '{:,.2f} US$'.format(be.get_data_average())


def minval():
    return'{:,.2f} US$'.format(be.min_last_val())


def maxval():
    return '{:,.2f} US$'.format(be.max_last_val())


def difvalu():
    return '{:,.2f} US$'.format(be.diff_val_btc())

def minex():
    return be.last_min_exch().title()


def maxex():
    return be.last_max_exch().title()


def difpro():
    return '{:,.2f} %'.format(be.diff_procent_last())


def val_bittrex():
    return '{:,.2f} US$'.format(be.last_bittrex())


def val_binance():
    return '{:,.2f} US$'.format(be.last_binance())


def val_poloniex():
    return '{:,.2f} US$'.format(be.last_poloniex())


def val_kraken():
    return '{:,.2f} US$'.format(be.last_kraken())


def val_hitbtc():
    return '{:,.2f} US$'.format(be.last_hitbtc())


def val_bitstamp():
    return '{:,.2f} US$'.format(be.last_bitstamp())


def val_bitfinex():
    return '{:,.2f} US$'.format(be.last_bitfinex())


def val_coinbase():
    return '{:,.2f} US$'.format(be.last_coinbase())


@app.route('/')
def index():
    return render_template('index.html',
                           btcinf=be.usd_btc_info(),
                           loctime=be.local_in_string(),
                           averval=average(),
                           minexna=minex(),
                           minexval=minval(),
                           maxexna=maxex(),
                           maxexval=maxval(),
                           diffproce=difpro(),
                           diffusd=difvalu(),
                           bitst=val_bitstamp(),
                           bitfi=val_bitfinex(),
                           bina=val_binance(),
                           bittre=val_bittrex(),
                           coinb=val_coinbase(),
                           hitb=val_hitbtc(),
                           krak=val_kraken(),
                           polo=val_poloniex()
                           )


if __name__ == '__main__':
    app.run(debug=True)
