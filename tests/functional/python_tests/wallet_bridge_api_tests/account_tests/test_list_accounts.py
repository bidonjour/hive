import pytest

from test_tools import exceptions

ACCOUNTS = [f'account-{i}' for i in range(10)]

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.list_accounts with incorrect argument  type 
   (putting bool as limit argument). I think, in this situation program should throw an exception.  (# BUG1) 
"""


@pytest.mark.parametrize(
    'lowerbound_account, limit', [
        # LOWERBOUND ACCOUNT
        (ACCOUNTS[0], 100),
        ('non-exist-acc', 100),
        ('', 100),

        # LIMIT
        (ACCOUNTS[0], 0),
        (ACCOUNTS[0], 1000),
    ]
)
def tests_with_correct_value(node, wallet, lowerbound_account, limit):
    # TODO Add pattern test
    wallet.create_accounts(len(ACCOUNTS))

    response = node.api.wallet_bridge.list_accounts(lowerbound_account, limit)


@pytest.mark.parametrize(
    'lowerbound_account, limit', [
        # LIMIT
        (ACCOUNTS[0], -1),
        (ACCOUNTS[0], 1001),
    ]
)
def tests_with_incorrect_values(node, wallet, lowerbound_account, limit):
    wallet.create_accounts(len(ACCOUNTS))

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.list_accounts(lowerbound_account, limit)


@pytest.mark.parametrize(
    'lowerbound_account, limit', [
        # LOWERBOUND ACCOUNT
        (True, 100),
        (100, 100),
        (['example-array'], 100),

        # LIMIT
        # (ACCOUNTS[0], True),  # BUG1
        (ACCOUNTS[0], 'incorrect_string_argument'),
        (ACCOUNTS[0], [100]),
    ]
)
def tests_with_incorrect_type_of_argument(node, lowerbound_account, limit):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.list_accounts(lowerbound_account, limit)
