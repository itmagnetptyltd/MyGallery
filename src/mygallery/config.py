"""Where the application listens.

HOST is loopback deliberately: REQ-GAL-011 requires that a connection from
another device on the network is refused, and binding to 127.0.0.1 is what
makes that true without the client configuring a firewall. Do not change it
to 0.0.0.0.
"""

HOST = "127.0.0.1"
PORT = 8765
