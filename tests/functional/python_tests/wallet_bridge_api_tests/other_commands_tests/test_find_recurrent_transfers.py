import pytest

from test_tools import exceptions

import local_tools

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.find_recurrent_transfers with additional argument.  Method return exception:
   "Assert Exception:args.get_array()[0].is_string(): Account name is required as first argument"   (# BUG1) 
"""


@pytest.mark.parametrize(
    'reward_fund_name', [
        'alice',
        'bob',
    ]
)
def tests_with_correct_value(node, wallet, reward_fund_name):
    # TODO Add pattern test
    local_tools.prepare_node_with_recurrent_transfer(wallet)

    response = node.api.wallet_bridge.find_recurrent_transfers(reward_fund_name)


@pytest.mark.parametrize(
    'reward_fund_name', [
        'non_exist_account',
        '',
    ]
)
def tests_with_incorrect_value(node, reward_fund_name):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.find_recurrent_transfers(reward_fund_name)


@pytest.mark.parametrize(
    'reward_fund_name', [
        ['alice'],
        100,
        True
    ]
)
def tests_with_incorrect_type_of_argument(node, wallet, reward_fund_name):
    local_tools.prepare_node_with_recurrent_transfer(wallet)

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.find_recurrent_transfers(reward_fund_name)


# def test_with_additional_argument(node, wallet):
#     local_tools.prepare_node_with_recurrent_transfer(wallet)
#
#     node.api.wallet_bridge.find_recurrent_transfers('alice', 'additional_argument')   # BUG1
