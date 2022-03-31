import pytest

from test_tools import exceptions

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_ops_in_block with incorrect argument (putting negative value as block 
   number). I think, in this situation program should throw an exception.  (# BUG1) 

2. Problem with running wallet_bridge_api.get_ops_in_block with incorrect argument type (putting bool as block 
   number). I think, in this situation program should throw an exception.  (# BUG2)  
"""

@pytest.mark.parametrize(
    'block_number, virtual_operation', [
        #  BLOCK NUMBER
        (0, True),
        (18446744073709551615, True),
    ]
)
def test_with_correct_value(node, block_number, virtual_operation):
    # TODO Add pattern test
    node.wait_number_of_blocks(21)  # Waiting for next witness schedule
    response = node.api.wallet_bridge.get_ops_in_block(block_number, virtual_operation)


@pytest.mark.parametrize(
    'block_number, virtual_operation', [
        #  BLOCK NUMBER
        # (-1, True),  # BUG1
        (18446744073709551616, True),
    ]
)
def tests_with_incorrect_value(node, block_number, virtual_operation):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_ops_in_block(block_number, virtual_operation)


@pytest.mark.parametrize(
    'block_number, virtual_operation', [
        #  BLOCK NUMBER
        ('incorrect_string_argument', True),
        # (True, True),  # BUG2
        ([0], True),

        #  VIRTUAL OPERATION
        (0, 'incorrect_string_argument'),
        (0, 0),
        (0, [True]),
    ]
)
def tests_with_incorrect_type_of_arguments(node, block_number, virtual_operation):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_ops_in_block(block_number, virtual_operation)
