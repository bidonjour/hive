import pytest

from test_tools import exceptions

import local_tools

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_order_book with incorvrect argument type (putting bool as argument).
   I think, in this situation program should throw an exception. (# BUG1) 
   
2. Problem with calling wallet_bridge_api.find_proposals with arguments in quotes
     Sent: {"jsonrpc": "2.0", "id": 1, "method": "wallet_bridge_api.get_order_book", "params": ["10"]}
     Received: 'message': "Assert Exception:args.get_array()[0].is_numeric(): Orders limit is required as first argument"
     (# BUG2)
"""

CORRECT_VALUES = [
        0,
        10,
        500,
        True,  # bool is treat like numeric (0:1)
    ]


@pytest.mark.parametrize(
    'orders_limit', CORRECT_VALUES
)
def tests_with_correct_value(node, wallet, orders_limit):
    # TODO Add pattern test
    local_tools.prepare_node_with_created_order(wallet)

    response = node.api.wallet_bridge.get_order_book(orders_limit)

#BUG2  (NOW IS REPAIR IN OTHER MERGE REQUEST. ABLE TO WORK AFTER REBASE)
# @pytest.mark.parametrize(
#     'orders_limit', CORRECT_VALUES
# )
# def tests_with_correct_value_in_quotes(node, wallet, orders_limit):
#     local_tools.prepare_node_with_created_order(wallet)
#     orders_limit = local_tools.add_quotes_to_bool_or_numeric(orders_limit)
#
#     response = node.api.wallet_bridge.get_order_book(orders_limit)


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
