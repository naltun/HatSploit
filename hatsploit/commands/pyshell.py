"""
MIT License

Copyright (c) 2020-2022 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import platform

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    details = {
        'Category': "developer",
        'Name': "pyshell",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer',
        ],
        'Description': "Open Python shell.",
        'Usage': "pyshell",
        'MinArgs': 0,
    }

    def run(self, argc, argv):
        self.print_information(f"Python {platform.python_version()} console")
        self.print_empty()

        while True:
            code = self.input_empty("%bold>>> %end")

            if "exit" in code or "quit" in code:
                return
            try:
                exec(' '.join(code))
            except SystemExit:
                return
            except (EOFError, KeyboardInterrupt):
                return
            except Exception as e:
                self.print_error(str(e))
