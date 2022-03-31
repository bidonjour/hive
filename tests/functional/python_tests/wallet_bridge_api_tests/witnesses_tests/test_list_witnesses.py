import pytest

from test_tools import exceptions

import local_tools

WITNESSES_NAMES = [f'witness-{i}' for i in range(21)]

# TODO BUG LIST!
'''
1. Problem with run command wallet_bridge_api.list_witnesses() with incorrect type of argument
   (putting bool as limit argument). I think, in this situation program should throw an exception. (# BUG1)
'''


@pytest.mark.parametrize(
    'witness_account, limit', [
        # WITNESS ACCOUNT
        (WITNESSES_NAMES[0], 100),
        (WITNESSES_NAMES[-1], 100),
        ('non-exist-acc', 100),

        # LIMIT
        (WITNESSES_NAMES[0], 0),
        (WITNESSES_NAMES[0], 1000),
    ]
)
def tests_with_correct_value(world, witness_account, limit):
    # TODO Add pattern test
    node = local_tools.prepare_node_with_witnesses(world, WITNESSES_NAMES)
    response = node.api.wallet_bridge.list_witnesses(witness_account, limit)


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
