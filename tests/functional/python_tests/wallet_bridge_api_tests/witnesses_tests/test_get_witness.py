import pytest

from test_tools import exceptions

import local_tools

WITNESSES_NAMES = [f'witness-{i}' for i in range(21)]


@pytest.mark.parametrize(
    'witness_account', [
        WITNESSES_NAMES[0],
        WITNESSES_NAMES[-1],
        'non-exist-acc',
        '',
    ],
)
def tests_with_correct_value(world, witness_account):
    # TODO Add pattern test.
    node = local_tools.prepare_node_with_witnesses(world, WITNESSES_NAMES)
    response = node.api.wallet_bridge.get_witness(witness_account)


@pytest.mark.parametrize(
    'witness_account', [
        100,
        True,
        ['example-array']
    ]
)
def tests_with_incorrect_type_of_argument(node, witness_account):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_witness(witness_account)
