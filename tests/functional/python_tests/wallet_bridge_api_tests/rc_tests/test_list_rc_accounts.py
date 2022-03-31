import pytest

from test_tools import exceptions


ACCOUNTS = [f'account-{i}' for i in range(3)]

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.list_rc_accounts with incorrect argument type (putting 
bool as limit). I think, in this situation program should throw an exception.  (# BUG1) 
"""


@pytest.mark.parametrize(
    'rc_account, limit', [
        # RC ACCOUNT
        (ACCOUNTS[0], 100),
        (ACCOUNTS[-1], 100),
        ('non-exist-acc', 100),
        ('', 100),

        # LIMIT
        (ACCOUNTS[0], 0),
        (ACCOUNTS[0], 1000),
    ]
)
def tests_with_correct_values(node, wallet, rc_account, limit):
    # TODO Add pattern test
    wallet.create_accounts(len(ACCOUNTS))
    response = node.api.wallet_bridge.list_rc_accounts(rc_account, limit),


@pytest.mark.parametrize(
    'rc_account, limit', [
        # LIMIT
        (ACCOUNTS[0], -1),
        (ACCOUNTS[0], 1001),
    ]
)
def tests_with_incorrect_values(node, wallet, rc_account, limit):
    wallet.create_accounts(len(ACCOUNTS))

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.list_rc_accounts(rc_account, limit)


@pytest.mark.parametrize(
    'rc_account, limit', [
        # WITNESS
        (['example-array'], 100),
        (100, 100),
        (True, 100),

        # LIMIT
        (ACCOUNTS[0], 'incorrect_string_argument'),
        (ACCOUNTS[0], [100]),
        # (ACCOUNTS[0], True),  # BUG1
    ]
)
def tests_with_incorrect_type_of_arguments(node, wallet, rc_account, limit):
    wallet.create_accounts(len(ACCOUNTS))
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.list_rc_accounts(rc_account, limit)
