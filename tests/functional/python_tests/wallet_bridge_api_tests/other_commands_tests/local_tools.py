from test_tools import Asset


def add_quotes_to_bool_or_numeric(argument):
    if argument is type(int) or type(bool):
        return f'{argument}'


def prepare_node_with_set_withdraw_vesting_route(wallet):
    with wallet.in_single_transaction():
        wallet.api.create_account('initminer', 'alice', '{}')
        wallet.api.create_account('initminer', 'bob', '{}')

    wallet.api.transfer_to_vesting('initminer', 'alice', Asset.Test(500))
    wallet.api.set_withdraw_vesting_route('alice', 'bob', 30, True)


def prepare_node_with_set_convert_request(wallet):
    wallet.api.create_account('initminer', 'alice', '{}')
    wallet.api.transfer('initminer', 'alice', Asset.Test(100), 'memo')
    wallet.api.transfer_to_vesting('initminer', 'alice', Asset.Test(100))
    wallet.api.convert_hive_with_collateral('alice', Asset.Test(10))
    wallet.api.convert_hbd('alice', Asset.Tbd(0.1))


def prepare_node_with_set_collateral_convert_request(wallet):
    wallet.api.create_account('initminer', 'alice', '{}')
    wallet.api.transfer('initminer', 'alice', Asset.Test(100), 'memo')
    wallet.api.transfer_to_vesting('initminer', 'alice', Asset.Test(100))
    wallet.api.convert_hive_with_collateral('alice', Asset.Test(10))


def prepare_node_with_created_order(wallet):
    wallet.api.create_account('initminer', 'alice', '{}')
    wallet.api.transfer('initminer', 'alice', Asset.Test(100), 'memo')
    wallet.api.transfer_to_vesting('initminer', 'alice', Asset.Test(100))
    wallet.api.create_order('alice', 1000, Asset.Test(1), Asset.Tbd(1), False, 1000)


def prepare_node_with_updated_account(wallet):
    wallet.api.create_account('initminer', 'alice', '{}')
    wallet.api.transfer_to_vesting('initminer', 'alice', Asset.Test(500))
    key = 'TST8grZpsMPnH7sxbMVZHWEu1D26F3GwLW1fYnZEuwzT4Rtd57AER'
    wallet.api.update_account('alice', '{}', key, key, key, key)


def prepare_node_with_recurrent_transfer(wallet):
    with wallet.in_single_transaction():
        wallet.api.create_account('initminer', 'alice', '{}')
        wallet.api.create_account('initminer', 'bob', '{}')

    wallet.api.transfer_to_vesting('initminer', 'alice', Asset.Test(100))
    wallet.api.transfer('initminer', 'alice', Asset.Test(500), 'memo')
    wallet.api.recurrent_transfer('alice', 'bob', Asset.Test(20), 'memo', 100, 10)
