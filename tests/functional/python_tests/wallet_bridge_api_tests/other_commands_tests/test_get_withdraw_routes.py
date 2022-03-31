import pytest

from test_tools import exceptions

import local_tools


@pytest.mark.parametrize(
    'account_name, withdraw_route_type', [
        #  ACCOUNT NAME
        ('alice', 'all'),
        ('bob', 'all'),
        ('non-exist-acc', 'all'),
        ('', 'all'),

        #  WITHDRAW ROUTE TYPE
        ('alice', 'all'),
        ('alice', 'incoming'),
        ('alice', 'outgoing'),
    ]
)
def tests_with_correct_value(node, wallet, account_name, withdraw_route_type):
    # TODO Add pattern test
    local_tools.prepare_node_with_set_convert_request(wallet)
    response = node.api.wallet_bridge.get_withdraw_routes(account_name, withdraw_route_type)


@pytest.mark.parametrize(
    'account_name, withdraw_route_type', [
        #  WITHDRAW ROUTE TYPE
        ('alice', 'non-exist-argument'),
    ]
)
def tests_with_incorrect_value(node, wallet, account_name, withdraw_route_type):
    local_tools.prepare_node_with_set_convert_request(wallet)

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_withdraw_routes(account_name, withdraw_route_type)


@pytest.mark.parametrize(
    'account_name, withdraw_route_type', [
        #  ACCOUNT NAME
        (['alice'], 'all'),
        (100, 'all'),
        (True, 'all'),

        #  WITHDRAW ROUTE TYPE
        ('alice', ['all']),
        ('alice', 100),
        ('alice', True),
    ]
)
def tests_with_incorrect_type_of_arguments(node, wallet, account_name, withdraw_route_type):
    local_tools.prepare_node_with_set_convert_request(wallet)

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_withdraw_routes(account_name, withdraw_route_type)


def tests_with_additional_argument(node, wallet):
    local_tools.prepare_node_with_set_convert_request(wallet)

    node.api.wallet_bridge.get_withdraw_routes('alice', 'all', 'additional_argument')


def tests_with_missing_argument(node, wallet):
    local_tools.prepare_node_with_set_convert_request(wallet)

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_withdraw_routes('alice')
