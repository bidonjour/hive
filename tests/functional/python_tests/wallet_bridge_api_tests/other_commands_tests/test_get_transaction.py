import pytest

from test_tools import exceptions

import local_tools

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_transaction with additional argument.  Method return exception:
   "Assert Exception:args.get_array()[0].is_string(): Transaction id is required as second argument"   (# BUG1) 
"""


def test_with_correct_value(node, wallet):
    # TODO Add pattern test
    transaction_id = wallet.api.create_account('initminer', 'alice', '{}')['transaction_id']
    node.wait_number_of_blocks(21)
    response = node.api.wallet_bridge.get_transaction(transaction_id)


def test_with_correct_value_in_quotes(node, wallet):
    transaction_id = wallet.api.create_account('initminer', 'alice', '{}')['transaction_id']
    node.wait_number_of_blocks(21)
    transaction_id = local_tools.add_quotes_to_bool_or_numeric(transaction_id)

    response = node.api.wallet_bridge.get_transaction(transaction_id)


def test_with_incorrect_value(node):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_transaction('0000000000000000000000000000000000000000')  # non exist transaction id


@pytest.mark.parametrize(
    'transaction_id', [
        'incorrect_string_argument',
        100,
        True,
    ]
)
def tests_with_incorrect_type_of_argument(node, transaction_id):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_transaction(transaction_id)


def test_with_additional_argument(node, wallet):
    transaction_id = wallet.api.create_account('initminer', 'alice', '{}')['transaction_id']
    node.wait_number_of_blocks(21)

    # node.api.wallet_bridge.get_transaction(transaction_id, 'additional_argument')  # BUG1
