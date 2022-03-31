import pytest

from test_tools import exceptions

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.broadcast_transaction with additional argument.  Method return exception:
    "Assert Exception:args.get_array()[0].is_object(): Signed transaction is required as first argument"   (# BUG1) 
"""


def test_with_correct_value(node, wallet):
    transaction = wallet.api.create_account('initminer', 'alice', '{}', broadcast=False)
    node.api.wallet_bridge.broadcast_transaction(transaction)

    assert 'alice' in wallet.list_accounts()


@pytest.mark.parametrize(
    'transaction_name', [
        ['non-exist-transaction'],
        'non-exist-transaction',
        100,
        True
    ]
)
def tests_broadcast_transaction_with_incorrect_type_of_argument(node, transaction_name):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.broadcast_transaction(transaction_name)


# def test_with_additional_argument(node, wallet):
#     transaction = wallet.api.create_account('initminer', 'alice', '{}', broadcast=False)
#
#     node.api.wallet_bridge.broadcast_transaction(transaction, 'additional_argument')   # BUG1
