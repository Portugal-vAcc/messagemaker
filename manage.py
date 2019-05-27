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
import os
import click
import subprocess
import shutil
from pathlib import Path

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

@cli.command()
@click.argument('dest_folder')
@click.option('--nuke', default=False, is_flag=True, help='clear only dest_folder, do not actually package audio files')
def package(dest_folder, nuke):
    try:
        shutil.rmtree(dest_folder)
    except FileNotFoundError:
        pass
    if nuke:
        return

    os.makedirs(dest_folder)
    with open(f'{dest_folder}/atisfile.txt', 'w') as atisfile:
        for file in os.listdir('audio'):
            audio = Path(file)
            if audio.suffix != '.wav':
                continue

            # this is only required since GNG does not accept some characters for filenames..
            special_chars = ['.', ',']
            safe_filename = audio.stem
            for special_char in special_chars:
                safe_filename = safe_filename.replace(special_char, '')
            subprocess.call(['sox',
                '--norm', f'audio/{file}',
                '-b', '16',     # sample size, 16bits
                '-c', '1',      # audio channels, mono
                '-r', '7350',   # bitrate, 7350Mhz
                f'{dest_folder}/{safe_filename}{audio.suffix}'
            ])
            atisfile.write(f'RECORD:{audio.stem}:{safe_filename}{audio.suffix}\n')

if __name__ == '__main__':
    cli()
