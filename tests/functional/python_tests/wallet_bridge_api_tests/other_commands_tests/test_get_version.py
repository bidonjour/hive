def test_get_version(node):
    # TODO Add pattern test
    response = node.api.wallet_bridge.get_version()
