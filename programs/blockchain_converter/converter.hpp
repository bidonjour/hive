#pragma once

#include <memory>
#include <map>
#include <string>

#include <fc/crypto/elliptic.hpp>

#include <hive/protocol/operations.hpp>
#include <hive/protocol/block.hpp>

namespace hive {

  using namespace protocol;

  namespace converter {

    class derived_keys_map
    {
    public:

      typedef std::map< public_key_type, fc::ecc::private_key > keys_map_type;
      typedef keys_map_type::const_iterator                     const_iterator;

      derived_keys_map( const std::string& private_key_wif );

      derived_keys_map( const fc::ecc::private_key& _private_key );

      /// Generates public key from the private key mapped to the public key from the original block_log
      public_key_type get_public( const public_key_type& original );

      /// Inserts key to the container if public key from the original block log was not found in the map.
      /// Returns const reference to the generated derived private key.
      const fc::ecc::private_key& get_private( const public_key_type& original );

      /// Retrieves private key from the map. Throws std::out_of_range if given public key was not found.
      const fc::ecc::private_key& at( const public_key_type& original )const;

      const_iterator begin()const;

      const_iterator end()const;

      void save_wallet_file( const std::string& password, std::string wallet_filename = "" )const;

    private:

      keys_map_type keys;

      std::string   private_key_wif;
    };

    class blockchain_converter
    {
    private:
      fc::ecc::private_key _private_key;
      chain_id_type        chain_id;
      derived_keys_map     keys;

    public:
      /// All converted blocks will be signed using keys derived from the given private key
      blockchain_converter( const fc::ecc::private_key& _private_key, const chain_id_type& chain_id = HIVE_CHAIN_ID );

      /// Sets signed_block previous member to the given value and re-signs content of the block using derived keys. Returns current block id.
      block_id_type convert_signed_block( signed_block& _signed_block, const block_id_type& previous_block_id );

      void convert_signed_header( signed_block_header& _signed_header );

      const fc::ecc::private_key& convert_signature_from_header( const signature_type& _signature, const signed_block_header& _signed_header );

      /// Tries to guess canon type using given signature. If not found it is defaulted to fc::ecc::non_canonical
      fc::ecc::canonical_signature_type get_canon_type( const signature_type& _signature )const;

      typename authority::key_authority_map convert_authorities( const typename authority::key_authority_map& auths );

      derived_keys_map& get_keys();
      const derived_keys_map& get_keys()const;
    };

    class convert_operations_visitor
    {
    private:
      blockchain_converter& converter;

    public:
      typedef operation result_type;

      convert_operations_visitor( blockchain_converter& converter );

      const account_create_operation& operator()( account_create_operation& op )const;

      const account_create_with_delegation_operation& operator()( account_create_with_delegation_operation& op )const;

      const account_update_operation& operator()( account_update_operation& op )const;

      const account_update2_operation& operator()( account_update2_operation& op )const;

      const create_claimed_account_operation& operator()( create_claimed_account_operation& op )const;

      const witness_update_operation& operator()( witness_update_operation& op )const;

      const witness_set_properties_operation& operator()( witness_set_properties_operation& op )const;

      const custom_binary_operation& operator()( custom_binary_operation& op )const;

      const pow2_operation& operator()( pow2_operation& op )const;

      const report_over_production_operation& operator()( report_over_production_operation& op )const;

      const request_account_recovery_operation& operator()( request_account_recovery_operation& op )const;

      const recover_account_operation& operator()( recover_account_operation& op )const;

      // No signatures modification ops
      template< typename T >
      const T& operator()( const T& op )const
      {
        FC_ASSERT( !op.is_virtual(), "block log should not contain virtual operations" );
        return op;
      }
    };

  }
}
