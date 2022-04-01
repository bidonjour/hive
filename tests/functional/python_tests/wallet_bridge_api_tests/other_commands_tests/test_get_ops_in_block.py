import pytest

from test_tools import exceptions

import local_tools

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_ops_in_block with incorrect argument (putting negative value as block 
   number). I think, in this situation program should throw an exception.  (# BUG1) 

2. Problem with running wallet_bridge_api.get_ops_in_block with incorrect argument type (putting bool as block 
   number). I think, in this situation program should throw an exception.  (# BUG2)  
   
3. Problem with calling wallet_bridge_api.find_proposals with arguments in quotes
     Sent: {"jsonrpc": "2.0", "id": 1, "method": "wallet_bridge_api.get_ops_in_block", "params": [["0", "0"]]}
     Received: 'message': "Assert Exception:arguments.get_array()[0].is_numeric(): block number is required as first argument"
     (# BUG3)
"""

CORRECT_VALUES = [
        #  BLOCK NUMBER
        (0, True),
        (18446744073709551615, True),
        (True, True)   # bool is treat like numeric (0:1)
    ]


@pytest.mark.parametrize(
    'block_number, virtual_operation', CORRECT_VALUES
)
def test_with_correct_value(node, block_number, virtual_operation):
    # TODO Add pattern test
    node.wait_number_of_blocks(21)  # Waiting for next witness schedule
    response = node.api.wallet_bridge.get_ops_in_block(block_number, virtual_operation)


#BUG3  (NOW IS REPAIR IN OTHER MERGE REQUEST. ABLE TO WORK AFTER REBASE)
# @pytest.mark.parametrize(
#     'block_number, virtual_operation', CORRECT_VALUES
# )
# def test_with_correct_value_in_quotes(node, block_number, virtual_operation):
#     node.wait_number_of_blocks(21)  # Waiting for next witness schedule
#
#     block_number = local_tools.add_quotes_to_bool_or_numeric(block_number)
#     virtual_operation = local_tools.add_quotes_to_bool_or_numeric(block_number)
#
#     response = node.api.wallet_bridge.get_ops_in_block(block_number, virtual_operation)


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
