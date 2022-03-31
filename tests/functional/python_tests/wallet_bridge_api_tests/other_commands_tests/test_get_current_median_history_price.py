def test_get_current_median_history_price(node):
    # TODO Add pattern test
    response = node.api.wallet_bridge.get_current_median_history_price()
