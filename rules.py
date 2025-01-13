trading_rules = {
    "minimum_gain": 5, # 5% minimum gain before we close postition
    "maximum_loss": 4, # 4% maximum loss for the position
    'max_position_allocation': 0.05, # 5% of the portfolio value
    'minimum_positional_nominal': 1000, # 1000 euro minimum position size
    'minimum_buy_diff': 200, # minimum amount that our market value must be below our set allocation before rebalance
    'minimum_sell_diff': 200, # minimum amount that our market value can be higher than our set allocation before we rebalance
}