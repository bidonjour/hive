import pytest

from test_tools import exceptions


ACCOUNTS = [f'account-{i}' for i in range(10)]

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_accounts with incorrect argument type 
   (putting array as argument). I think, in this situation program should throw an exception.  (# BUG1) 
"""


@pytest.mark.parametrize(
    'account', [
        ACCOUNTS,
        [ACCOUNTS[0]],
        ['non-exist-acc'],
        [''],
    ]
)
def tests_with_correct_value(node, wallet, account):
    # TODO Add pattern test
    wallet.create_accounts(len(ACCOUNTS))

    response = node.api.wallet_bridge.get_accounts(account)


@pytest.mark.parametrize(
    'account_key', [
        # ['example-array'],  # BUG1
        100,
        True,
        'incorrect_string_argument'
    ]
)
def tests_with_incorrect_type_of_argument(node, account_key):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_accounts(account_key)
