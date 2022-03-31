import pytest

from test_tools import exceptions

ACCOUNTS = [f'account-{i}' for i in range(10)]


@pytest.mark.parametrize(
    'account', [
        ACCOUNTS[0],
        'non-exist-acc',
        '',
    ]
)
def tests_correct_value(node, wallet, account):
    # TODO Add pattern test
    wallet.create_accounts(len(ACCOUNTS))
    response = node.api.wallet_bridge.get_account(account)


@pytest.mark.parametrize(
    'account', [
        ['example_array'],
        100,
        True,
    ]
)
def tests_incorrect_type_of_argument(node, account):
    with pytest.raises(exceptions.CommunicationError):
        node.api.wallet_bridge.get_account(account)
