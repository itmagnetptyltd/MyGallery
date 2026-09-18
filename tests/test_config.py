"""Configuration — the loopback bind and the port the instructions promise."""


# @covers REQ-GAL-011@v1
def test_the_server_is_configured_to_listen_on_loopback_only():
    from mygallery import config

    assert config.HOST == "127.0.0.1"


# @covers REQ-GAL-011@v1
def test_the_configured_port_matches_the_port_in_the_start_instructions(documented_port):
    from mygallery import config

    assert config.PORT == documented_port
