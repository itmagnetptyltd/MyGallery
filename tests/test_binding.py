"""Criterion 5 — the application is not reachable from another device.

The refusal is a property of the bind address, not of a firewall the client
has to configure, so it is testable here.
"""

import socket

import pytest
from tests.conftest import lan_ipv4


# @covers REQ-GAL-011@v1
def test_a_started_server_reports_a_loopback_bound_address(running_server):
    assert running_server.host == "127.0.0.1"


# @covers REQ-GAL-011@v1
@pytest.mark.skipif(
    lan_ipv4() is None,
    reason="this machine has no non-loopback IPv4 interface to connect from",
)
def test_a_started_server_refuses_a_connection_to_the_machine_network_address(running_server):
    with pytest.raises(OSError):
        socket.create_connection((lan_ipv4(), running_server.port), timeout=3).close()
