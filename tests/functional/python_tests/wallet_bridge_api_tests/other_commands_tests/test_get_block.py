import pytest

from test_tools import exceptions

import local_tools

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_block with incorrect argument (putting negative value as 
   argument). I think, in this situation program should throw an exception. (# BUG1) 

2. Problem with running wallet_bridge_api.get_block with incorrect argument type (putting bool as 
   argument). I think, in this situation program should throw an exception. (# BUG2)  
"""

CORRECT_VALUES = [
        0,
        1,
        10,
        18446744073709551615,
    ]


@pytest.mark.parametrize(
    'block_number', CORRECT_VALUES
)
def tests_with_correct_value(node, block_number):
    # TODO Add pattern test
    if block_number < 2:  # This condition makes it possible to get a saturated output stream for blocks 0 and 1.
        node.wait_for_block_with_number(2)
    response = node.api.wallet_bridge.get_block(block_number)


@pytest.mark.parametrize(
    'block_number', CORRECT_VALUES
)
def tests_with_correct_value_in_quotes(node, block_number):
    if block_number < 2:  # This condition makes it possible to get a saturated output stream for blocks 0 and 1.
        node.wait_for_block_with_number(2)

    block_number = local_tools.add_quotes_to_bool_or_numeric(block_number)
    response = node.api.wallet_bridge.get_block(block_number)


@pytest.mark.parametrize(
    'block_number', [
        # -1,  # BUG1
        18446744073709551616,
    ]
)
def tests_with_incorrect_value(node, block_number):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_block(block_number)


@pytest.mark.parametrize(
    'block_number', [
        [0],
        # True,  # BUG2
        'incorrect_string_argument'
    ]
)
def tests_with_incorrect_type_of_argument(node, block_number):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_block(block_number)
