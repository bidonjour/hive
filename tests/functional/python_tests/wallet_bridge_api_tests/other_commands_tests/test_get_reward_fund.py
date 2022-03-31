import pytest

from test_tools import exceptions


def test_with_correct_value(node):
    # TODO Add pattern test
    response = node.api.wallet_bridge.get_reward_fund('post')


@pytest.mark.parametrize(
    'reward_fund_name', [
        'command',
        'post0',
        'post1',
        'post2',
        '',
    ]
)
def tests_with_incorrect_value(node, reward_fund_name):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_reward_fund(reward_fund_name)


@pytest.mark.parametrize(
    'reward_fund_name', [
        ['post'],
        100,
        True,
    ]
)
def tests_with_incorrect_type_of_argument(node, reward_fund_name):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_reward_fund(reward_fund_name)
