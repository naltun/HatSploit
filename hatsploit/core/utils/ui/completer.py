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

import readline

from hatsploit.core.cli.fmt import FMT
from hatsploit.lib.commands import Commands


class Completer:
    fmt = FMT()

    commands = Commands()

    matches = None

    def completer(self, text, state):
        if state == 0:
            options = []

            original_line = readline.get_line_buffer()
            line = original_line.lstrip()

            stripped = len(original_line) - len(line)

            start_index = readline.get_begidx() - stripped
            end_index = readline.get_endidx() - stripped

            if start_index > 0:
                command = self.fmt.format_commands(line)

                if command[0] == "":
                    complete_function = self.default_completer
                else:
                    commands = self.commands.get_commands()

                    other_commands = self.commands.get_modules_commands()
                    other_commands.update(self.commands.get_plugins_commands())

                    if command[0] in commands:
                        if hasattr(commands[command[0]], "complete"):
                            complete_function = commands[command[0]].complete
                        else:
                            if 'Options' in commands[command[0]].details:
                                options = commands[command[0]].details['Options']
                            else:
                                complete_function = self.default_completer

                    elif command[0] in other_commands:
                        if 'Options' in other_commands[command[0]]:
                            options = other_commands[command[0]]['Options']
                        else:
                            complete_function = self.default_completer

                    else:
                        complete_function = self.default_completer
            else:
                complete_function = self.commands.commands_completer

            if options:
                self.matches = self.options_completer(options, text)
            else:
                self.matches = complete_function(text)

        try:
            return self.matches[state]
        except IndexError:
            return None

    def options_completer(self, options, text):
        return [option for option in options if option.startswith(text)]

    def default_completer(self, text):
        return []
