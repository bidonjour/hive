import pytest

from test_tools import exceptions


def test_with_correct_value_and_existing_transaction(node, wallet):
    # TODO Add pattern test
    transaction_id = wallet.api.create_account('initminer', 'alice', '{}')['transaction_id']

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
