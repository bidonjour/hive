import pytest

from test_tools import exceptions


ACCOUNTS = [f'account-{i}' for i in range(3)]

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.find_rc_accounts with incorrect argument type (putting array as 
argument). I think, in this situation program should throw an exception.  (# BUG1) 
"""


@pytest.mark.parametrize(
    'rc_accounts', [
        [''],
        ['non-exist-acc'],
        [ACCOUNTS[0]],
        ACCOUNTS,
    ]
)
def tests_with_correct_value(node, wallet, rc_accounts):
    # TODO Add pattern test
    wallet.create_accounts(len(ACCOUNTS))
    response = node.api.wallet_bridge.find_rc_accounts(rc_accounts)



@pytest.mark.parametrize(
    'rc_accounts', [
        # ['example-array'],  # BUG1
        100,
        True,
        'incorrect_string_argument'
    ]
)
def tests_with_incorrect_type_of_argument(node, rc_accounts):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.find_rc_accounts(rc_accounts)
