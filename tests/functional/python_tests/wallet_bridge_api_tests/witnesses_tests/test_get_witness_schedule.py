import local_tools

WITNESSES_NAMES = [f'witness-{i}' for i in range(21)]


def tests_with_correct_value(world):
    # TODO Add pattern test
    node = local_tools.prepare_node_with_witnesses(world, WITNESSES_NAMES)
    response = node.api.wallet_bridge.get_witness_schedule()
