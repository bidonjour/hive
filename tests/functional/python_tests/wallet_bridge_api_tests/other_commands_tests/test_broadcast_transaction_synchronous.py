import pytest

from test_tools import exceptions


def test_with_correct_value(node, wallet):
    transaction = wallet.api.create_account('initminer', 'alice', '{}', broadcast=False)
    node.api.wallet_bridge.broadcast_transaction_synchronous(transaction)

    assert 'alice' in wallet.list_accounts()


@pytest.mark.parametrize(
    'transaction_name', [
        ['non-exist-transaction'],
        'non-exist-transaction',
        100,
        True
    ]
)
def tests_with_incorrect_type_of_argument(node, transaction_name):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.broadcast_transaction_synchronous(transaction_name)


def test_with_additional_argument(node, wallet):
    transaction = wallet.api.create_account('initminer', 'alice', '{}', broadcast=False)
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.broadcast_transaction_synchronous(transaction, 'additional_argument')
