import pytest

from test_tools import exceptions

import local_tools

# TODO BUG LIST!
"""
1. Problem with running wallet_bridge_api.get_conversion_requests with additional argument.  Method return exception:
   "Assert Exception:args.get_array()[0].is_string(): account name required as first argument"   (# BUG1) 
"""


def test_with_correct_value(node, wallet):
    # TODO Add pattern test
    local_tools.prepare_node_with_set_convert_request(wallet)

    response = node.api.wallet_bridge.get_conversion_requests('alice')


@pytest.mark.parametrize(
    'account_name', [
        'non-exist-acc',
        '',
    ]
)
def tests_with_incorrect_value(node, account_name):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_conversion_requests(account_name)


@pytest.mark.parametrize(
    'account_name', [
        ['alice'],
        100,
        True,
    ]
)
def tests_with_incorrect_type_of_argument(node, wallet, account_name):
    local_tools.prepare_node_with_set_convert_request(wallet)

    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_conversion_requests(account_name)


# def test_with_additional_argument(node, wallet):
#     local_tools.prepare_node_with_set_convert_request(wallet)
#
#     node.api.wallet_bridge.get_conversion_requests('alice', 'additional_argument')  # BUG1
