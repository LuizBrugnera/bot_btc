# Binance Trading Bot

## Overview
This Python script automates trading operations on the Binance platform. It checks the current price of Bitcoin (BTC) against your fiat currency for example the Brazilian Real (BRL) and performs buy and sell operations based on predefined price thresholds.

## Features
- Automatically buys BTC when the price drops to a specified percentage below the last purchase price or the starting price if no purchase has been made yet.
- Sells BTC when the price reaches a specified percentage above the purchase price.
- Saves transaction history and current state to a JSON file to maintain state between executions.
- Uses environment variables for sensitive information like API keys.
- Console messages in Portuguese and English

## Prerequisites
- Python 3
- Binance account
- API Key and Secret from Binance
- `python-binance` library
- `python-dotenv` library for environment variable management

## Setup
1. Clone this repository or download the script.
2. Install the required Python packages:

pip install python-binance
pip install python-dotenv

3. Create a `.env` file in the same directory as the script with the following contents:

API_KEY=your_binance_api_key
API_SECRET=your_binance_api_secret
BUY_PERCENT=percentage_below_current_price_for_buying
SELL_PERCENT=percentage_above_purchase_price_for_selling   
CURRENCY_TYPE=your currency type, for example USD or BRL    
`Opitional` LANGUAGE=en or pt --> English or Portuguese -- by default it comes in English   
`Opitional` REFRESH_TIME=360--> by default it comes in 360 seconds    


Replace `your_binance_api_key`, `your_binance_api_secret`, `percentage_below_current_price_for_buying`, `percentage_above_purchase_price_for_selling`,`your_currency_type`with your actual API credentials and desired percentage thresholds for buying and selling.

## How to Run
1. Navigate to the directory containing the script.
2. Run the script using Python:
python bot_btc.py 

## Operational Logic
- The bot fetches the current BTC price and decides whether to buy or sell based on the set percentage thresholds.
- If the price is below the buy threshold and no BTC is held, it will purchase BTC.
- If the price is above the sell threshold and BTC is held, it will sell the BTC.
- Transaction details are saved in `trading_data.json` to track the bot's activity and maintain its state for future executions.

## Disclaimer
- Use this bot at your own risk. Automated trading can result in significant financial losses.
- Always test the bot in a simulation or with small amounts before running it with substantial capital.
- This script is for educational purposes only and not intended for real trading without thorough testing and customization.