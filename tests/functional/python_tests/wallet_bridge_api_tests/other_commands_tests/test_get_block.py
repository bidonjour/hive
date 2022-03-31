import pytest

from test_tools import exceptions

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_block with incorrect argument (putting negative value as 
   argument). I think, in this situation program should throw an exception. (# BUG1) 

2. Problem with running wallet_bridge_api.get_block with incorrect argument type (putting bool as 
   argument). I think, in this situation program should throw an exception. (# BUG2)  
"""


@pytest.mark.parametrize(
    'block_number', [
        0,
        1,
        10,
        18446744073709551615,
    ]
)
def tests_with_correct_value(node, block_number):
    # TODO Add pattern test
    if block_number < 2:  # This condition makes it possible to get a saturated output stream for blocks 0 and 1.
        node.wait_for_block_with_number(2)
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
