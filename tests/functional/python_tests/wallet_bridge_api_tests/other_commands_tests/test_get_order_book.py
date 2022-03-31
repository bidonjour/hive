import pytest

from test_tools import exceptions

import local_tools

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_order_book with incorvrect argument type (putting bool as argument).
   I think, in this situation program should throw an exception. (# BUG1) 
"""


@pytest.mark.parametrize(
    'orders_limit', [
        0,
        10,
        500,
    ]
)
def tests_with_correct_value(node, wallet, orders_limit):
    # TODO Add pattern test
    local_tools.prepare_node_with_created_order(wallet)

    response = node.api.wallet_bridge.get_order_book(orders_limit)


@pytest.mark.parametrize(
    'orders_limit', [
        -1,
        501,
    ]
)
def tests_with_incorrect_value(node, orders_limit):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_order_book(orders_limit)


@pytest.mark.parametrize(
    'orders_limit', [
        [0],
        # True,  # BUG1
        'incorrect_string_argument'
    ]
)
def tests_with_incorrect_type_of_argument(node, orders_limit):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_order_book(orders_limit)
