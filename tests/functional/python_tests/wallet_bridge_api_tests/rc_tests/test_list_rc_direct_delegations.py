import pytest

from test_tools import Asset, exceptions

import local_tools

ACCOUNTS = [f'account-{i}' for i in range(3)]

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.list_rc_direct_delegations with incorrect argument 
    type (putting bool as limit). I think, in this situation program should throw an exception.  (# BUG1) 

2. Problem with calling wallet_bridge_api.find_proposals with arguments in quotes
     Sent: {"jsonrpc": "2.0", "id": 1, "method": "wallet_bridge_api.list_rc_direct_delegations", "params": [[["account-0", "account-1"], "1000"]]"}
     Received: 'message': "Assert Exception:arguments.get_array()[1].is_numeric(): Limit is required as second argument"
     (# BUG2)
"""


CORRECT_VALUES = [
        # FROM, TO
        (ACCOUNTS[0], ACCOUNTS[1], 100),
        (ACCOUNTS[0], '', 100),

        # LIMIT
        (ACCOUNTS[0], ACCOUNTS[1], 0),
        (ACCOUNTS[0], ACCOUNTS[1], 1000),
        (ACCOUNTS[0], ACCOUNTS[1], True),   # bool is treat like numeric (0:1)
]


@pytest.mark.parametrize(
    'from_, to, limit', CORRECT_VALUES
)
def test_list_rc_direct_delegations_with_correct_value(node, wallet, from_, to, limit):
    wallet.create_accounts(len(ACCOUNTS))
    wallet.api.transfer_to_vesting('initminer', ACCOUNTS[0], Asset.Test(0.1))
    wallet.api.delegate_rc(ACCOUNTS[0], [ACCOUNTS[1]], 5)

    response = node.api.wallet_bridge.list_rc_direct_delegations([from_, to], limit),


#BUG2  (NOW IS REPAIR IN OTHER MERGE REQUEST. ABLE TO WORK AFTER REBASE)
# @pytest.mark.parametrize(
#     'from_, to, limit', CORRECT_VALUES
# )
# def test_list_rc_direct_delegations_with_correct_value_in_quotes(node, wallet, from_, to, limit):
#     wallet.create_accounts(len(ACCOUNTS))
#     wallet.api.transfer_to_vesting('initminer', ACCOUNTS[0], Asset.Test(0.1))
#     wallet.api.delegate_rc(ACCOUNTS[0], [ACCOUNTS[1]], 5)
#     limit = local_tools.add_quotes_to_bool_or_numeric(limit)
#
#     response = node.api.wallet_bridge.list_rc_direct_delegations([from_, to], limit),


@pytest.mark.parametrize(
    'from_, to, limit', [
        # LIMIT
        (ACCOUNTS[0], ACCOUNTS[1], -1),
        (ACCOUNTS[0], '', 1001),
    ]
)
def test_list_rc_direct_delegations_with_incorrect_value(node, wallet, from_, to, limit):
    wallet.create_accounts(len(ACCOUNTS))
    wallet.api.transfer_to_vesting('initminer', ACCOUNTS[0], Asset.Test(0.1))
    wallet.api.delegate_rc(ACCOUNTS[0], [ACCOUNTS[1]], 5)

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.list_rc_direct_delegations([from_, to], limit)


@pytest.mark.parametrize(
    'from_, to, limit', [
        # FROM_
        (100, ACCOUNTS[1], 100),
        (True, ACCOUNTS[1], 100),

        # TO
        (ACCOUNTS[0], 100, 100),
        (ACCOUNTS[0], True, 100),

        # LIMIT
        (ACCOUNTS[0], ACCOUNTS[1], 'incorrect_string_argument'),
        # (ACCOUNTS[0], ACCOUNTS[1], True),  # BUG1
    ]
)
def test_list_rc_direct_delegations_with_incorrect_type_of_arguments(node, wallet, from_, to, limit):
    wallet.create_accounts(len(ACCOUNTS))
    wallet.api.transfer_to_vesting('initminer', ACCOUNTS[0], Asset.Test(0.1))
    wallet.api.delegate_rc(ACCOUNTS[0], [ACCOUNTS[1]], 5)

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.list_rc_direct_delegations([from_, to], limit)
