from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from rules import trading_rules

def get_all_positions_dict(trading_client):
    
    all_positions_list = trading_client.get_all_positions()

    all_positions_dict = {}

    for position in all_positions_list:
        all_positions_dict[position.symbol] = position

    return all_positions_dict


def buy_strategy_1(data_struct, trading_client):
    
    account = trading_client.get_account()

    position_allocation = round(float(account.portfolio_value) * trading_rules['max_position_allocation'], 2)

    all_positions_dict = get_all_positions_dict(trading_client)

    # Ticker already in our portfolio
    if data_struct['symbol'] in all_positions_dict.keys():
        
        market_value = float(all_positions_dict[data_struct['symbol']].market_value)

        if market_value >= position_allocation:
            # if market value meets or exceeds the max position allocation, don't buy any more
            return None
        
        elif (position_allocation - market_value) >= trading_rules['minimum_buy_diff']:
            # if market value is less than the max position allocation by at least the minimum buy difference
            market_order_data = MarketOrderRequest(
                symbol=data_struct['symbol'],
                notional=round(position_allocation-market_value, 2),
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )

            market_order = trading_client.submit_order(
                order_data=market_order_data
            )

            return market_order

    # Ticker not in our portfolio, buy the full position allocation
    else:

        market_order_data = MarketOrderRequest(
            symbol=data_struct['symbol'],
            notional=round(position_allocation, 2),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )

        market_order = trading_client.submit_order(
            order_data=market_order_data
        )

        return market_order

    return None 


def sell_strategy_1(trading_client):

    account = trading_client.get_account()

    all_positions = trading_client.get_all_positions()

    position_allocation = round(float(account.portfolio_value) * trading_rules['max_position_allocation'], 2)

    # Review all of our positions and sell when appropriate
    for position in all_positions:

        gain_loss = round(float(position.unrealized_plpc),2)
        market_value = round(float(position.market_value),2)

        # If our current gain or loss is meeting our gain or loss requirements, liquidate position
        if gain_loss >= trading_rules['minimum_gain'] or gain_loss <= (trading_rules['maximum_loss'] *-1):
            # Create a market SELL order
            market_order_data = MarketOrderRequest(
                symbol=position.symbol,
                qty=position.qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY
            )

            market_order = trading_client.submit_order(
            order_data=market_order_data
            )

            return market_order

        # If our market value exceeds our position allocation by at least 200 dollars, sell the difference
        if (market_value - position_allocation) >= trading_rules['minimum_sell_diff']:
            # Create a market SELL order
            market_order_data = MarketOrderRequest(
                symbol=position.symbol,
                notional=round(market_value - position_allocation, 2),
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY
                )

            market_order = trading_client.submit_order(
            order_data=market_order_data
            )
    return None