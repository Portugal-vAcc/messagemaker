"""
Message Maker

Copyright (C) 2018 - 2019  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of Message Maker.

Message Maker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

Message Maker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Message Maker.  If not, see <http://www.gnu.org/licenses/>.
"""
import click
import subprocess

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', '-h', default='0.0.0.0', help='The address the web app will listen in.')
@click.option('--port', '-p', default=5000, help='The TCP port to listen to')
@click.option('--debug', '-d', default=False, is_flag=True, help='Set enviroment mode')
def run(host, port, debug):
    """Runs a development web server."""
    if debug:
        from messagemaker import app
        app.run(host=host, port=port, debug=debug)
    else:
        subprocess.call(['gunicorn', 'messagemaker:app', '--bind', f'{host}:{port}', '--log-file=-'])

@cli.command()
def shell():
    """Runs a shell in the app context."""
    subprocess.call(['flask', 'shell'])

@cli.command()
@click.option('--only', help='Run only the specified test.')
def test(only=None):
    """Runs tests."""
    suite = ['coverage', 'run', '--source=messagemaker', '-m', 'unittest', '-v']
    if only:
        suite.append(only)
    subprocess.call(suite)
    subprocess.call(['coverage', 'report', '--show-missing'])

if __name__ == '__main__':
    cli()
