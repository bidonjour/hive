import pytest

from test_tools import exceptions

import local_tools


def test_with_correct_value_and_existing_transaction(node, wallet):
    # TODO Add pattern test
    transaction_id = wallet.api.create_account('initminer', 'alice', '{}')['transaction_id']

    response = node.api.wallet_bridge.is_known_transaction(transaction_id)


def test_with_correct_value_and_existing_transaction_in_quotes(node, wallet):
    transaction_id = wallet.api.create_account('initminer', 'alice', '{}')['transaction_id']
    transaction_id = local_tools.add_quotes_to_bool_or_numeric(transaction_id)

    response = node.api.wallet_bridge.is_known_transaction(transaction_id)


@pytest.mark.parametrize(
    'transaction_id', [
        '0000000000000000000000000000000000000000',
        '',
        '0',
    ]
)
def tests_with_correct_value_and_non_existing_transaction(node, transaction_id):
    node.api.wallet_bridge.is_known_transaction(transaction_id)


@pytest.mark.parametrize(
    'transaction_id', [
        ['0000000000000000000000000000000000000000'],
        100,
        True,
    ]
)
def tests_with_incorrect_type_of_argument(node, transaction_id):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.is_known_transaction(transaction_id)
