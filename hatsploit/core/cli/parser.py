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

from hatsploit.lib.options import Options


class Parser:
    def parse_options(self, options, option=None):
        if not option:
            values = []
            for option_name in options:
                if option_name.upper() not in Options().handler_options['Module']:
                    if option_name.upper() not in Options().handler_options['Payload']:
                        values.append(str(options[option_name]['Value']))
            if len(values) == 1:
                return values[0]
            return values
        return str(options[option]['Value'])

    @staticmethod
    def parse_ports_range(ports_range):
        start = int(ports_range.split('-')[0].strip())
        end = int(ports_range.split('-')[1].strip())

        return start, end
