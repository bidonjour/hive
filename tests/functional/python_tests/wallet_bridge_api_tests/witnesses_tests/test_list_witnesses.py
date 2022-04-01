import pytest

from test_tools import exceptions

import local_tools

WITNESSES_NAMES = [f'witness-{i}' for i in range(21)]

# TODO BUG LIST!
'''
1. Problem with run command wallet_bridge_api.list_witnesses() with incorrect type of argument
   (putting bool as limit argument). I think, in this situation program should throw an exception. (# BUG1)
   
2. Problem with calling wallet_bridge_api.find_proposals with arguments in quotes
     Sent: {"jsonrpc": "2.0", "id": 1, "method": "wallet_bridge_api.list_witnesses", "params": [["account-0", "100"]]"}
     Received: 'message': "Assert Exception:arguments.get_array()[1].is_numeric(): Witnesses limit is required as second argument"
     (# BUG2)
'''

CORRECT_VALUES = [
        # WITNESS ACCOUNT
        (WITNESSES_NAMES[0], 100),
        (WITNESSES_NAMES[-1], 100),
        ('non-exist-acc', 100),

        # LIMIT
        (WITNESSES_NAMES[0], 0),
        (WITNESSES_NAMES[0], 1000),
        (WITNESSES_NAMES[0], True),   # bool is treat like numeric (0:1)
]


@pytest.mark.parametrize(
    'witness_account, limit', CORRECT_VALUES
)
def tests_with_correct_value(world, witness_account, limit):
    # TODO Add pattern test
    node = local_tools.prepare_node_with_witnesses(world, WITNESSES_NAMES)
    response = node.api.wallet_bridge.list_witnesses(witness_account, limit)

#BUG2  (NOW IS REPAIR IN OTHER MERGE REQUEST. ABLE TO WORK AFTER REBASE)
# @pytest.mark.parametrize(
#     'witness_account, limit', CORRECT_VALUES
# )
# def tests_with_correct_value_in_quotes(world, witness_account, limit):
#     # TODO Add pattern test
#     node = local_tools.prepare_node_with_witnesses(world, WITNESSES_NAMES)
#     limit = local_tools.add_quotes_to_bool_or_numeric(limit)
#     response = node.api.wallet_bridge.list_witnesses(witness_account, limit)


@pytest.mark.parametrize(
    'witness_account, limit', [
        # LIMIT
        (WITNESSES_NAMES[0], -1),
        (WITNESSES_NAMES[0], 1001),
    ]
)
def tests_with_incorrect_value(world, witness_account, limit):
    node = local_tools.prepare_node_with_witnesses(world, WITNESSES_NAMES)
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.list_witnesses(witness_account, limit)


@pytest.mark.parametrize(
    'witness_account, limit', [
        # WITNESS ACCOUNT
        (100, 100),
        (True, 100),

        # LIMIT
        (WITNESSES_NAMES[0], 'incorrect_string_argument'),
        # (WITNESSES_NAMES[0], True),  # BUG1
    ]
)
def tests_with_incorrect_type_of_arguments(world, witness_account, limit):
    node = local_tools.prepare_node_with_witnesses(world, WITNESSES_NAMES)
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.list_witnesses(witness_account, limit)
