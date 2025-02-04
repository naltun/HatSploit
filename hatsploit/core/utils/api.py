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

import logging
import sys
from flask import Flask
from flask import cli
from flask import jsonify
from flask import make_response
from flask import request
from io import StringIO
from pex.string import String

from hatsploit.core.base.execute import Execute
from hatsploit.core.cli.fmt import FMT
from hatsploit.lib.config import Config
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.options import Options
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.sessions import Sessions


class APIPool:
    def __init__(self):
        self._stdout = None
        self._string_io = None

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = StringIO()
        return self

    def __exit__(self, tp, value, traceback):
        sys.stdout = self._stdout

    def __str__(self):
        return self._string_io_getvalue()


class API:
    def __init__(self, username, password, host='127.0.0.1', port=8008):
        self.string_tools = String()

        self.fmt = FMT()
        self.execute = Execute()

        self.jobs = Jobs()
        self.options = Options()
        self.modules = Modules()
        self.payloads = Payloads()
        self.sessions = Sessions()
        self.config = Config()

        self.host = host
        self.port = int(port)

        self.username = username
        self.password = password

        self.token = self.string_tools.random_string(32)

    def run(self):
        cli.show_server_banner = lambda *_: None
        rest_api = Flask("HatSploit")

        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

        @rest_api.before_request
        def validate_token():
            if request.path not in ['/login', '/']:
                token = request.form['token']

                if token != self.token:
                    return make_response('', 401)

                current_module = self.modules.get_current_module()
                current_payload = self.payloads.get_current_payload()

                self.jobs.stop_dead()
                self.sessions.close_dead()

                self.options.add_handler_options(current_module, current_payload)

        @rest_api.route('/', methods=['GET', 'POST'])
        def api():
            version = self.config.core_config['details']['version']
            codename = self.config.core_config['details']['codename']

            response = "HatSploit REST API server\n"
            response += f"Version: {version}\n"

            if codename:
                response += f"Codename: {codename}\n"

            return make_response(f"<pre>{response}</pre>", 200)

        @rest_api.route('/login', methods=['POST'])
        def login_api():
            username = request.form['username']
            password = request.form['password']

            if username == self.username and password == self.password:
                return jsonify(token=self.token)
            return make_response('', 401)

        @rest_api.route('/execute', methods=['POST'])
        def commands_api():
            command = request.form['command']
            commands = self.fmt.format_commands(command)

            self.execute.execute_command(commands)

        @rest_api.route('/payloads', methods=['POST'])
        def payloads_api():
            action = None

            if 'action' in request.form:
                action = request.form['action']

            if action == 'list':
                data = {}
                all_payloads = self.payloads.get_payloads()
                number = 0

                for database in sorted(all_payloads):
                    payloads = all_payloads[database]

                    for payload in sorted(payloads):
                        data.update(
                            {
                                number: {
                                    'Category': payloads[payload]['Category'],
                                    'Payload': payloads[payload]['Payload'],
                                    'Rank': payloads[payload]['Rank'],
                                    'Name': payloads[payload]['Name'],
                                    'Platform': payloads[payload]['Platform'],
                                }
                            }
                        )

                        number += 1

                return jsonify(data)
            return make_response('', 200)

        @rest_api.route('/modules', methods=['POST'])
        def modules_api():
            action = None

            if 'action' in request.form:
                action = request.form['action']

            if action == 'list':
                data = {}
                all_modules = self.modules.get_modules()
                number = 0

                for database in sorted(all_modules):
                    modules = all_modules[database]

                    for module in sorted(modules):
                        data.update(
                            {
                                number: {
                                    'Category': modules[module]['Category'],
                                    'Module': modules[module]['Module'],
                                    'Rank': modules[module]['Rank'],
                                    'Name': modules[module]['Name'],
                                    'Platform': modules[module]['Platform'],
                                }
                            }
                        )

                        number += 1

                return jsonify(data)

            if action == 'options':
                data = {}
                current_module = self.modules.get_current_module()

                if current_module:
                    options = current_module.options

                    for option in sorted(options):
                        value, required = (
                            options[option]['Value'],
                            options[option]['Required'],
                        )
                        if required:
                            required = 'yes'
                        else:
                            required = 'no'
                        if not value and value != 0:
                            value = ""
                        data.update(
                            {
                                option: {
                                    'Value': value,
                                    'Required': required,
                                    'Description': options[option]['Description'],
                                }
                            }
                        )

                    if hasattr(current_module, "payload"):
                        current_payload = self.payloads.get_current_payload()

                        if hasattr(current_payload, "options"):
                            options = current_payload.options

                            for option in sorted(options):
                                value, required = (
                                    options[option]['Value'],
                                    options[option]['Required'],
                                )
                                if required:
                                    required = 'yes'
                                else:
                                    required = 'no'
                                if not value and value != 0:
                                    value = ""
                                data.update(
                                    {
                                        option: {
                                            'Value': value,
                                            'Required': required,
                                            'Description': options[option][
                                                'Description'
                                            ],
                                        }
                                    }
                                )

                return jsonify(data)

            if action == 'use':
                self.modules.use_module(request.form['module'])

            if action == 'set':
                self.modules.set_current_module_option(
                    request.form['option'], request.form['value']
                )

            if action == 'run':
                current_module = self.modules.get_current_module()

                if current_module:
                    with APIPool() as pool:
                        self.modules.run_current_module()
                        return make_response(str(pool), 200)

            return make_response('', 200)

        @rest_api.route('/sessions', methods=['POST'])
        def sessions_api():
            action = None

            if 'action' in request.form:
                action = request.form['action']

            if action == 'close':
                session = request.form['session']
                self.sessions.close_session(session)

            elif action == 'list':
                data = {}
                sessions = self.sessions.get_sessions()
                fetch = 'all'

                if 'fetch' in request.form:
                    fetch = request.form['fetch']

                if sessions:
                    for session in sessions:
                        if fetch == 'all':
                            data.update(
                                {
                                    session: {
                                        'Platform': sessions[session]['Platform'],
                                        'Architecture': sessions[session][
                                            'Architecture'
                                        ],
                                        'Type': sessions[session]['Type'],
                                        'Host': sessions[session]['Host'],
                                        'Port': sessions[session]['Port'],
                                    }
                                }
                            )
                        elif fetch == sessions[session]['Platform']:
                            data.update(
                                {
                                    session: {
                                        'Platform': sessions[session]['Platform'],
                                        'Architecture': sessions[session][
                                            'Architecture'
                                        ],
                                        'Type': sessions[session]['Type'],
                                        'Host': sessions[session]['Host'],
                                        'Port': sessions[session]['Port'],
                                    }
                                }
                            )

                return jsonify(data)

            elif action == 'execute':
                session = request.form['session']
                session = self.sessions.get_session(session)

                if session:
                    if request.form['output'].lower() in ['yes', 'y']:
                        output = session.send_command(
                            request.form['command'], output=True
                        )
                        return jsonify(output=output)

                    session.send_command(request.form['command'])

            elif action == 'download':
                if 'local_path' in request.form:
                    local_path = request.form['local_path']
                else:
                    local_path = self.config.path_config['loot_path']

                self.sessions.session_download(
                    request.form['session'], request.form['remote_file'], local_path
                )

            elif action == 'upload':
                self.session.session_upload(
                    request.form['session'],
                    request.form['local_file'],
                    request.form['remote_path'],
                )

            return make_response('', 200)

        rest_api.run(host=self.host, port=self.port)
