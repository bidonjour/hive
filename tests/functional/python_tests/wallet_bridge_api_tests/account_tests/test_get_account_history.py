import pytest

from test_tools import exceptions

import local_tools

ACCOUNTS = [f'account-{i}' for i in range(10)]

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_account_history with incorrect value ( putting negative value to
   from_ argument). I think, in this situation program should throw an exception.  (# BUG1) 
   More information about get_account_history is in this place: 
        https://developers.hive.io/apidefinitions/#account_history_api.get_account_history

2. Problem with running wallet_bridge_api.get_account_history with incorrect argument type 
   (putting bool as limit ). I think, in this situation program should throw an exception.  (# BUG2) 
   
3. Problem with calling wallet_bridge_api.find_proposals with arguments in quotes
     Sent: {"jsonrpc": "2.0", "id": 1, "method": "wallet_bridge_api.get_account_history", "params": [["account-0", "4294967295", "1000"]]}
     Received: 'message': "Assert Exception:arguments.get_array()[1].is_numeric(): from (numeric type) is required as second argument"
     (# BUG3)
"""

CORRECT_VALUES = [
        # ACCOUNT
        (ACCOUNTS[0], -1, 1000),
        ('non-exist-acc', -1, 1000),
        ('', -1, 1000),

        # FROM
        (ACCOUNTS[0], 4294967295, 1000),   # maximal value of uint32
        (ACCOUNTS[0], 2, 1),
        (ACCOUNTS[0], -1, 1000),
        # (ACCOUNTS[0], True, 1000),  # bool is treat like numeric (0:1)   # BUG3

        # LIMIT
        (ACCOUNTS[0], -1, 0),
        (ACCOUNTS[0], -1, 1000),
        (ACCOUNTS[0], -1, True),   # bool is treat like numeric (0:1)
]

@pytest.mark.parametrize(
    'account, from_, limit', CORRECT_VALUES
)
def tests_with_correct_value(node, wallet, account, from_, limit):
    # TODO Add pattern test
    wallet.create_accounts(len(ACCOUNTS))

    node.wait_number_of_blocks(21)  # wait 21 block to appear transactions in 'get account history'
    response = node.api.wallet_bridge.get_account_history(account, from_, limit)


#BUG3  (NOW IS REPAIR IN OTHER MERGE REQUEST. ABLE TO WORK AFTER REBASE)
# @pytest.mark.parametrize(
#     'account, from_, limit', CORRECT_VALUES
# )
# def tests_with_correct_value_in_quote(node, wallet, account, from_, limit):
#     wallet.create_accounts(len(ACCOUNTS))
#
#     from_ = local_tools.add_quotes_to_bool_or_numeric(from_)
#     limit = local_tools.add_quotes_to_bool_or_numeric(limit)
#
#     node.wait_number_of_blocks(21)  # wait 21 block to appear transactions in 'get account history'
#     response = node.api.wallet_bridge.get_account_history(account, from_, limit)


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
