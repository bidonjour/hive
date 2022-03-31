import pytest

from test_tools import exceptions

ACCOUNTS = [f'account-{i}' for i in range(10)]

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_account_history with incorrect value ( putting negative value to
   from_ argument). I think, in this situation program should throw an exception.  (# BUG1) 
   More information about get_account_history is in this place: 
        https://developers.hive.io/apidefinitions/#account_history_api.get_account_history

2. Problem with running wallet_bridge_api.get_account_history with incorrect argument type 
   (putting bool as limit ). I think, in this situation program should throw an exception.  (# BUG2) 
"""


@pytest.mark.parametrize(
    'account, from_, limit', [
        # ACCOUNT
        (ACCOUNTS[0], -1, 1000),
        ('non-exist-acc', -1, 1000),
        ('', -1, 1000),

        # FROM
        (ACCOUNTS[0], 4294967295, 1000),   # maximal value of uint32
        (ACCOUNTS[0], 2, 1),
        (ACCOUNTS[0], -1, 1000),

        # #LIMIT
        (ACCOUNTS[0], -1, 0),
        (ACCOUNTS[0], -1, 1000),
    ]
)
def tests_with_correct_value(node, wallet, account, from_, limit):
    # TODO Add pattern test
    wallet.create_accounts(len(ACCOUNTS))

    node.wait_number_of_blocks(21)  # wait 21 block to appear transactions in 'get account history'
    response = node.api.wallet_bridge.get_account_history(account, from_, limit)


@pytest.mark.parametrize(
    'account, from_, limit', [
        # FROM
        (ACCOUNTS[5], 4294967296, 1000),    # maximal value of uint32 + 1
        # (ACCOUNTS[5], -2, 1000),  # BUG1

        # LIMIT
        (ACCOUNTS[5], -1, -1),
        (ACCOUNTS[5], 1, 0),
        (ACCOUNTS[5], -1, 1001),
    ]
)
def tests_with_incorrect_value(node, account, from_, limit):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_account_history(account, from_, limit)


@pytest.mark.parametrize(
    'account, from_, limit', [
        # ACCOUNT
        (100, -1, 1000),
        (True, -1, 1000),
        (['example_array'], -1, 1000),

        # FROM
        (ACCOUNTS[5], 'example-string-argument', 1000),
        (ACCOUNTS[5], True, 1000),
        (ACCOUNTS[5], [-1], 1000),

        # LIMIT
        (ACCOUNTS[5], -1, 'example-string-argument'),
        # (ACCOUNTS[5], -1, True),  # BUG2
        (ACCOUNTS[5], -1, [1000]),
    ]
)
def tests_with_incorrect_type_of_argument(node, wallet, account, from_, limit):
    wallet.create_accounts(len(ACCOUNTS))

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_account_history(account, from_, limit)
