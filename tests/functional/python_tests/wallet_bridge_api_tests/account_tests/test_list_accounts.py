import pytest

from test_tools import exceptions

import local_tools
ACCOUNTS = [f'account-{i}' for i in range(10)]

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.list_accounts with incorrect argument  type 
   (putting bool as limit argument). I think, in this situation program should throw an exception.  (# BUG1)
2. Problem with calling wallet_bridge_api.find_proposals with arguments in quotes
     Sent: {"jsonrpc": "2.0", "id": 1, "method": "wallet_bridge_api.list_accounts", "params": [["account-0", "True"]]}
     Received: 'message': "Assert Exception:arguments.get_array()[1].is_numeric(): Accounts limit is required as second argument"
     (# BUG2)

"""

CORRECT_VALUES = [
        # LOWERBOUND ACCOUNT
        (ACCOUNTS[0], 100),
        ('non-exist-acc', 100),
        ('', 100),

        # LIMIT
        (ACCOUNTS[0], 0),
        (ACCOUNTS[0], 1000),
        (ACCOUNTS[0], True),  # bool is treat like numeric (0:1)
]


@pytest.mark.parametrize(
    'lowerbound_account, limit', CORRECT_VALUES
)
def tests_with_correct_values(node, wallet, lowerbound_account, limit):
    # TODO Add pattern test
    wallet.create_accounts(len(ACCOUNTS))

    response = node.api.wallet_bridge.list_accounts(lowerbound_account, limit)

#BUG2  (NOW IS REPAIR IN OTHER MERGE REQUEST. ABLE TO WORK AFTER REBASE)
# @pytest.mark.parametrize(
#     'lowerbound_account, limit', CORRECT_VALUES
# )
# def tests_with_correct_values_in_quotes(node, wallet, lowerbound_account, limit):
#     wallet.create_accounts(len(ACCOUNTS))
#
#     limit = local_tools.add_quotes_to_bool_or_numeric(limit)
#     response = node.api.wallet_bridge.list_accounts(lowerbound_account, limit)


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
