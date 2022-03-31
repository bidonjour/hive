from test_tools import Account, Asset, logger, Wallet


def prepare_node_with_witnesses(world, witnesses_names):
    node = world.create_init_node()
    for name in witnesses_names:
        witness = Account(name)
        node.config.witness.append(witness.name)
        node.config.private_key.append(witness.private_key)

    node.run()
    wallet = Wallet(attach_to=node)

    with wallet.in_single_transaction():
        for name in witnesses_names:
            wallet.api.create_account('initminer', name, '')

    with wallet.in_single_transaction():
        for name in witnesses_names:
            wallet.api.transfer_to_vesting("initminer", name, Asset.Test(1000))

    with wallet.in_single_transaction():
        for name in witnesses_names:
            wallet.api.update_witness(
                name, "https://" + name,
                Account(name).public_key,
                {"account_creation_fee": Asset.Test(3), "maximum_block_size": 65536, "sbd_interest_rate": 0}
            )

    logger.info('Wait 22 block, to next schedule of witnesses.')
    node.wait_number_of_blocks(22)

    return node
