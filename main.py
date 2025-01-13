from dotenv import load_dotenv
import os
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from strategy_1 import buy_strategy_1, sell_strategy_1

load_dotenv() # LOAD OUR ENV VARIABLES FROM OUR .ENV FILE

trading_client = TradingClient(os.getenv('ALPACAKEY'), os.getenv('ALPACASECRET'), paper=True) # SET PAPER = TRUE TO USE FAKE MONEY

# ASYNC HANDLER
async def quote_data_handler(data):
    # QUOTE DATA WILL ARRIVE HERE
    
    data_struct = {
        'symbol' : data.symbol,
        'bid_price' : data.bid_price,
        'bid_size' : data.bid_size,
        'ask_price': data.ask_price,
        'ask_size': data.ask_size
    }
    
    trade_result = buy_strategy_1(data_struct, trading_client)
    trade_result2 = sell_strategy_1(trading_client)

    if trade_result:
        print(trade_result)

    if trade_result:
        print(trade_result2)
    
    print(data_struct)

def main():

    stream_client = StockDataStream(os.getenv('ALPACAKEY'), os.getenv('ALPACASECRET'))
    stream_client.subscribe_quotes(quote_data_handler, 'NVDA')

    stream_client.run()

if __name__ == '__main__':
    main() 