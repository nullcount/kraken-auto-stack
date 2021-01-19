#!/usr/bin/env python

import krakenex
import json

k = krakenex.API()
k.load_key('kraken.key')

def getConfig():
    with open('config.json') as f:
        return json.load(f)

c = getConfig()

def getBalance():
    return k.query_private('Balance')['result']


def getTradableBalance(bal):
    tb = {}
    for alt in c['alts']:
        tb[alt] = float(bal[alt])
    return tb


def getPrice(asset, units):
    pair = asset+units
    ticker = k.query_public('Ticker', {'pair': pair})
    last_close_raw = ticker["result"][pair]["c"]
    last_close = last_close_raw[0]
    return float(last_close)

def getAltConfig(ticker):
    for alt in c['alts']:
        if alt == ticker:
            return c['alts'][alt]

def getSellableUnits(tradable):
    # units of each tradable asset can be sold
    sellable = {}
    for alt in tradable:
        a = getAltConfig(alt)
        unitsOfMin = a['minBalance'] / getPrice(alt, a['quote'])
        if tradable[alt] > unitsOfMin:
            sellable[alt] = tradable[alt] - unitsOfMin
    return sellable

def getPair(alt):
  return "%s%s" % (alt, c['alts'][alt]['buy'])

def marketBuy(pair, amt):
    print("BUY %s %s" % (pair, amt))

def worthIt(alt, amt):
    return True

def processTrades():
    bal = getBalance()
    printTable(bal, "Account Balances:")
    tradable = getTradableBalance(bal)
    sellable = getSellableUnits(tradable)
    if sellable:
        printTable(sellable, "Ready to Trade:")
    else:
        print("No alts to trade. Good job!")
    for alt in sellable:
        amt = sellable[alt]
        if worthIt(alt, amt):
	        pair = getPair(alt)
	        marketBuy(pair, amt)

def printTable(vals, desc):
    print()
    print(desc)
    for key in vals:
        print("%s %s" % (key, vals[key]))
    print()

def main():
    processTrades()
    print("Done.")

if __name__ == "__main__":
    main()
