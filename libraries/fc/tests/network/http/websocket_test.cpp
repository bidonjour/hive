#include <boost/test/unit_test.hpp>

#include <fc/network/http/websocket.hpp>

#include <iostream>

BOOST_AUTO_TEST_SUITE(fc_network)

BOOST_AUTO_TEST_CASE(websocket_test)
{
  try
  {
    fc::http::websocket_client client;
    fc::http::websocket_connection_ptr s_conn, c_conn;

    {
      fc::http::websocket_server server;

      server.on_connection( [&]( const fc::http::connection_ptr& c ){
        s_conn = std::static_pointer_cast< fc::http::websocket_connection >( c );
        s_conn->on_message_handler( [&](const std::string& s){
          s_conn->send_message("echo: " + s);
        } );
      } );

      server.listen( 8090 );
      server.start_accept();

      std::string echo;
      c_conn = std::static_pointer_cast< fc::http::websocket_connection >( client.connect( "ws://localhost:8090" ) );
      c_conn->on_message_handler( [&](const std::string& s){
        echo = s;
      } );

      c_conn->send_message( "hello world" );
      fc::usleep( fc::seconds(1) );
      BOOST_CHECK_EQUAL("echo: hello world", echo);

      c_conn->send_message( "again" );
      fc::usleep( fc::seconds(1) );
      BOOST_CHECK_EQUAL("echo: again", echo);

      s_conn->close(0, "test");
      fc::usleep( fc::seconds(1) );
      BOOST_REQUIRE_THROW( c_conn->send_message( "again" ), fc::assert_exception );

      c_conn = std::static_pointer_cast< fc::http::websocket_connection >( client.connect( "ws://localhost:8090" ) );
      c_conn->on_message_handler( [&](const std::string& s){
        echo = s;
      } );

      c_conn->send_message( "hello world" );
      fc::usleep( fc::seconds(1) );
      BOOST_CHECK_EQUAL("echo: hello world", echo);
    }

    BOOST_REQUIRE_THROW( c_conn->send_message( "again" ), fc::assert_exception );

    BOOST_REQUIRE_THROW( client.connect( "ws://localhost:8090" ), fc::exception );

  } FC_CAPTURE_LOG_AND_RETHROW(());
}

BOOST_AUTO_TEST_SUITE_END()
