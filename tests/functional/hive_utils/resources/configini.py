#!/usr/bin/python3

# Easier way to generate configs

class config:
	def __init__(self):
		self.log_appender = '{"appender":"stderr","stream":"std_error"} {"appender":"p2p","file":"logs/p2p/p2p.log"}'
		self.log_logger = '{"name":"default","level":"all","appender":"stderr"} {"name":"p2p","level":"all","appender":"p2p"}'
		self.backtrace = 'yes'
		self.plugin = 'witness database_api account_by_key_api network_broadcast_api condenser_api block_api transaction_status_api debug_node_api'
		self.history_disable_pruning = '0'
		self.account_history_rocksdb_path = '"blockchain/account-history-rocksdb-storage"'
		self.block_data_export_file = 'NONE'
		self.block_log_info_print_interval_seconds = '86400'
		self.block_log_info_print_irreversible = '1'
		self.block_log_info_print_file = 'ILOG'
		self.shared_file_dir = '"blockchain"'
		self.shared_file_size = '8G'
		self.shared_file_full_threshold = '0'
		self.shared_file_scale_rate = '0'
		self.follow_max_feed_size = '500'
		self.follow_start_feeds = '0'
		self.market_history_bucket_size = '[15,60,300,3600,86400]'
		self.market_history_buckets_per_size = '5760'
		self.p2p_seed_node = '127.0.0.1:2001'
		self.rc_skip_reject_not_enough_rc = '0'
		self.rc_compute_historical_rc = '0'
		self.statsd_batchsize = '1'
		self.tags_start_promoted = '0'
		self.tags_skip_startup_update = '0'
		self.transaction_status_block_depth = '64000'
		self.transaction_status_track_after_block = '0'
		self.webserver_http_endpoint = '127.0.0.1:8090'
		self.webserver_ws_endpoint = '127.0.0.1:8090'
		self.webserver_thread_pool_size = '32'
		self.enable_stale_production = '0'
		self.required_participation = '0'
		self.witness = '"initminer"'
		self.private_key = '5JNHfZYKGaomSFvd4NUdQ9qMcEAC43kujbfjueTHpVapX1Kzq2n'
		self.witness_skip_enforce_bandwidth = '1'
		self.snapshot_root_dir = '"/tmp/snapshots"'

	def generate(self, path_to_file : str):
		conf = self.__dict__
		with open(path_to_file, 'w') as file:
			for key, value in conf.items():
				if value is not None:
					file.write("{} = {}\n".format(key.replace("_", "-"), value))

	def load(self, path_to_file : str):
		keys = self.__dict__.keys()
		for key in keys:
			key = key.replace("_", "-")

		def proc_line(line : str):
			values = line.split("=")
			return values[0].strip(), values[1].strip()

		def match_property(self, line : str):
			if line.startswith('#'):
				return
			key, value = proc_line(line)
			if key in keys:
				setattr(self, key.replace('-', '_'), value)

		with open(path_to_file, 'r') as file:
			for line in file:
				match_property(line)
