import pytest

from test_tools import exceptions

import local_tools


@pytest.mark.parametrize(
    'account_name', [
        '',
        'non-exist-acc',
        'alice',
    ]
)
def tests_with_correct_value(node, wallet, account_name):
    # TODO Add pattern test
    local_tools.prepare_node_with_updated_account(wallet)

    response = node.api.wallet_bridge.get_owner_history(account_name)


@pytest.mark.parametrize(
    'account_name', [
        ['alice'],
        100,
        True
    ]
)
def tests_with_incorrect_type_of_argument(node, wallet, account_name):
    local_tools.prepare_node_with_updated_account(wallet)

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_owner_history(account_name)
