def test_get_feed_history(node):
    # TODO Add pattern test
    response = node.api.wallet_bridge.get_feed_history()
