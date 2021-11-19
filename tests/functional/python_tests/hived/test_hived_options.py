from os import remove
from os.path import join
from pathlib import Path
from shutil import rmtree

from test_tools import World

from .conftest import BLOCK_COUNT


def test_dump_config(world : World):
  node = world.create_init_node('init_0')
  old_config = dict()
  for key, value in node.config.__dict__.items(): old_config[key] = value
  node.run()
  node.wait_number_of_blocks(2)
  node.close()
  node.dump_config()
  assert node.config.__dict__ == old_config


def test_exit_before_sync(world : World, block_log : Path):
  net = world.create_network()

  init = net.create_api_node(name='node_1')
  half_way = int(BLOCK_COUNT / 2.0)

  init.run(replay_from=block_log, stop_at_block=half_way, exit_before_synchronization=True)
  assert not init.is_running()

  background_node = net.create_init_node()
  background_node.run(replay_from=block_log, wait_for_live=True)
  background_node.wait_number_of_blocks(2)

  rmtree( join( str(init.directory), 'blockchain' ), ignore_errors=True)
  init.run(replay_from=block_log, exit_before_synchronization=True)
  assert not init.is_running()

  background_node.close()

  snap = init.dump_snapshot(close=True)
  assert not init.is_running()

  remove( join( str(init.directory), 'blockchain', 'shared_memory.bin' ) )
  init.run(load_snapshot_from=snap, exit_before_synchronization=True)
  assert not init.is_running()


def test_bug_exit_after_replay_no_exception(world: World):
  node = world.create_init_node()
  node.run()

  with open(node.directory / 'stderr.txt') as file:
    stderr = file.read()

  warning = "flag `--exit-after-replay` is deprecated, please consider usage of `--exit-before-sync`"
  assert not warning in stderr


def test_bug_exit_after_replay_exception(world: World, block_log: Path):
  net = world.create_network()

  init = net.create_api_node(name='node_1')
  half_way = int(BLOCK_COUNT / 2.0)

  init.run(replay_from=block_log, stop_at_block=half_way, with_arguments=['--exit-after-replay'])

  with open(init.directory / 'stderr.txt') as file:
    stderr = file.read()

  warning = "flag `--exit-after-replay` is deprecated, please consider usage of `--exit-before-sync`"
  assert  warning in stderr


def test_exit_after_replay_behavior(world: World, block_log: Path):
  net = world.create_network()

  init = net.create_api_node(name='node_1')
  half_way = int(BLOCK_COUNT / 2.0)

  init.run(replay_from=block_log, stop_at_block=half_way, with_arguments=['--exit-after-replay'])
  assert not init.is_running()

  background_node = net.create_init_node()
  background_node.run(replay_from=block_log, wait_for_live=True)
  background_node.wait_number_of_blocks(2)

  rmtree( join( str(init.directory), 'blockchain' ), ignore_errors=True)
  init.run(replay_from=block_log, with_arguments=['--exit-after-replay'])
  assert not init.is_running()

  background_node.close()

  snap = init.dump_snapshot(close=True)
  assert not init.is_running()

  remove( join( str(init.directory), 'blockchain', 'shared_memory.bin' ) )
  init.run(load_snapshot_from=snap, with_arguments=['--exit-after-replay'])
  assert not init.is_running()
