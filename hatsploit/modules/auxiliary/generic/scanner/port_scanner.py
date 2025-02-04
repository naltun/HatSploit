"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import time
from pex.proto.tcp import TCPTools

from hatsploit.lib.module import Module


class HatSploitModule(Module, TCPTools):
    details = {
        'Category': "auxiliary",
        'Name': "Port Scanner",
        'Module': "auxiliary/generic/scanner/port_scanner",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer',
        ],
        'Description': "Scan host for opened ports.",
        'Platform': "generic",
        'Rank': "low",
    }

    options = {
        'HOST': {
            'Description': "Remote host.",
            'Value': None,
            'Type': "ip",
            'Required': True,
        },
        'RANGE': {
            'Description': "Ports to scan.",
            'Value': "0-65535",
            'Type': "port_range",
            'Required': True,
        },
    }

    def check_port(self, remote_host, port):
        target = remote_host + '/' + str(port)
        if self.check_tcp_port(remote_host, port):
            self.print_success(f"{target} - opened")

    def run(self):
        remote_host, ports_range = self.parse_options(self.options)
        start, end = self.parse_ports_range(ports_range)

        self.print_process(f"Scanning {remote_host}...")
        for port in range(start, end):
            self.check_port(remote_host, port)
