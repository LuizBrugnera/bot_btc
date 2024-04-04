import time
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import json
import os
import datetime

def save_data(purchased, price, buy_historic, sell_historic, brl_balance_historic):
    data = {
        'purchased': purchased,
        'price': price,
        'brl_balance_historic': brl_balance_historic, 
        'buy_historic': buy_historic,
        'sell_historic': sell_historic
    }
    with open('trading_data.json', 'w') as f:
        json.dump(data, f)

def load_data():
    try:
        with open('trading_data.json', 'r') as f:
            data = json.load(f)
            return data['purchased'], data['price'], data['brl_balance_historic'] ,data['buy_historic'], data['sell_historic']
    except FileNotFoundError:
        return False, None, [], [], []

def check_balance(currency):
    balance = client.get_asset_balance(asset=currency)
    return float(balance['free'])

def get_lot_size(symbol):
    info = client.get_symbol_info(symbol)
    for filt in info['filters']:
        if filt['filterType'] == 'LOT_SIZE':
            return float(filt['minQty']), float(filt['stepSize']), len(str(filt['stepSize']).split('.')[-1])

def buy_bitcoin():
    amount_brl = check_balance(currency_type)  # Verifica o saldo em BRL
    btc_price = float(client.get_symbol_ticker(symbol="BTCBRL")['price'])
    btc_amount = amount_brl / btc_price

    min_qty, step_size, precision = get_lot_size('BTCBRL')

    # Arredonda a quantidade para atender ao requisito de step size
    btc_amount = round(btc_amount, precision)

    btc_amount = max(min_qty, round(btc_amount // step_size * step_size, precision))

    order = client.order_market_buy(symbol='BTCBRL', quantity=btc_amount)
    return order, btc_price

def sell_bitcoin(btc_amount):
    min_qty, step_size, precision = get_lot_size('BTCBRL')

    # Ajusta a quantidade para atender ao requisito de precisão e step size
    btc_amount = max(min_qty, round(btc_amount // step_size * step_size, precision))

    order = client.order_market_sell(symbol='BTCBRL', quantity=btc_amount)
    return order

def formatPercent(percent, type):
    if type == 'SELL':
        return 1 + percent / 100
    elif type == 'BUY':
        return 1 - percent / 100

load_dotenv()

# Acessa as variáveis de ambiente
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
sell_percent = formatPercent(int(os.getenv('SELL_PERCENT')), 'SELL')
buy_percent = formatPercent(int(os.getenv('BUY_PERCENT')), 'BUY')
currency_type = os.getenv('CURRENCY_TYPE')

client = Client(api_key, api_secret)

purchased = False
price = None  
biggest_price = 0
lowest_price = 1000000
buy_historic = []
sell_historic = []
brl_balance_historic = []



if __name__ == '__main__':
    purchased, price, brl_balance_historic, buy_historic, sell_historic = load_data()
    btc_balance = check_balance('BTC')
        
    while True:
        now = datetime.datetime.now()
        
        print('----' * 5 , now.strftime("%H:%M - %d/%m") , '----' * 5)
        symbol = 'BTC' + currency_type
        current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        if(current_price > biggest_price):
            biggest_price = current_price
            
        if(current_price < lowest_price):
            lowest_price = current_price
            
        print("Maior preço:", biggest_price)
        print("Menor preço:", lowest_price)
        print("Preço atual:", current_price)
        
        if(price):
            if not purchased:
                print("Preço de venda:", price)
            else:
                print("Preço de compra:", price)
                
        
        if not purchased:
            print("Aguardando para comprar ( preço de compra esperado -> {} )".format('indefinido' if price is None else "{:.2f}".format(price * buy_percent)))
            if price is None or current_price <= price * buy_percent:
                amount_brl = check_balance(currency_type)
                if amount_brl >= 50:  # Supondo que 50 é o mínimo para comprar
                    result, price_btc = buy_bitcoin()
                    price = price_btc
                    purchased = True
                    buy_historic.append((result, price))
                    save_data(purchased, price, buy_historic, sell_historic, brl_balance_historic)
                    print("Comprado:", result)
        else: 
            print("Aguardando para vender ( preço de venda esperado -> {} )".format(price * sell_percent))
            if current_price >= price * sell_percent:
                btc_balance = check_balance('BTC')
                result = sell_bitcoin(btc_balance)
                purchased = False
                price = current_price
                sell_historic.append((result, current_price))
                brl_balance_historic.append(check_balance(currency_type))
                save_data(purchased, price, buy_historic, sell_historic, brl_balance_historic)
                print("Vendido:", result)

        time.sleep(360)  