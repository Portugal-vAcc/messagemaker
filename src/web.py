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
import logging
import requests
from avweather.metar import parse
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

from . import endpoint
from . import atis
from . import metar_sources

app = Flask(__name__)
Bootstrap(app)

@app.route('/metar')
def metar():
    if 'icao' not in request.args:
        return render_template('metar.html')

    _metar = metar_sources.download(request.args['icao'])

    return render_template('metar.html', metar=_metar)

@app.route('/')
def main():
    # make sure all required args are present and correct
    missing_or_wrong = endpoint.verify_args(request.args)
    if len(missing_or_wrong) > 0:
        missing_or_wrong = ', '.join(missing_or_wrong)
        return f'missing or wrong argument {missing_or_wrong}'

    # get all args to their correct types
    args   = endpoint.parse_args(request.args)
    metar  = endpoint.get_metar(args)
    rwy    = endpoint.get_rwy(args)
    letter = endpoint.get_letter(args)

    parts = []

    # basic terminal information
    parts += [atis.intro(metar, letter)]
    parts += [atis.approach(metar, rwy)]
    parts += [atis.transition_level(metar)]

    # controller selected options
    for option in ['xpndr_startup', 'hiro', 'rwy_35_clsd']:
        if endpoint.has_option_set(args, option):
            parts += atis.get_airport_option(metar, option)

    # online frequencies to contact
    if endpoint.has_option_set(args, 'show_freqs'):
        resp = requests.get('http://cluster.data.vatsim.net/vatsim-data.json')
        data = resp.json()

        parts += [atis.get_clr_freq(metar, data)]
        parts += [atis.get_dep_freq(metar, data)]

    # landing and takeoff instructions
    parts += [atis.arrdep_info(metar, rwy)]

    # weather report
    parts += [atis.wind(metar)]
    parts += [atis.weather(metar)]
    parts += [atis.sky(metar)]
    parts += [atis.temperature(metar)]
    parts += [atis.dewpoint(metar)]
    parts += [atis.qnh(metar)]

    # general arrival and departure information
    parts += atis.get_airport_option(metar, 'general_info')

    # acknowledge information
    parts += [atis.ack(metar, letter)]

    return ' '.join([part for part in parts if part is not None])

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f'args: {request.args}')
    logging.error('out of service', exc_info=True)

    return '[ATIS OUT OF SERVICE]'
