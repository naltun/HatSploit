"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from pex.proto.tcp import TCPTools

from hatsploit.lib.module import Module


class HatSploitModule(Module, TCPTools):
    details = {
        'Category': "auxiliary",
        'Name': "ADB Installation Checker",
        'Module': "auxiliary/android/checker/check_adb_installation",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer',
        ],
        'Description': "Check if remote Android device has ADB installation.",
        'Platform': "android",
        'Rank': "low",
    }

    options = {
        'HOST': {
            'Description': "Remote host.",
            'Value': None,
            'Type': "ip",
            'Required': True,
        }
    }

    def run(self):
        remote_host = self.parse_options(self.options)

        self.print_process(f"Checking {remote_host}...")
        if self.check_tcp_port(remote_host, 5555):
            self.print_success("Target device may has ADB installation!")
        else:
            self.print_warning("Looks like target device has no ADB installation.")
