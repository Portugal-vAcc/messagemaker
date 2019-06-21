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
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
import logging
import settings
import os

from .message import *

app = Flask(__name__)

@app.route('/')
def main():
    metar = request.args.get('metar')
    rwy = request.args.get('rwy')
    letter = request.args.get('letter')
    if not metar or not rwy or not letter:
        return 'wrong usage'

    show_freqs = False # request.args.get('show_freqs', 'True') == 'True'
    hiro = request.args.get('hiro', 'False') == 'True'
    xpndr_startup = request.args.get('xpndr_startup', 'False') == 'True'
    rwy_35_clsd = request.args.get('rwy_35_clsd', 'False') == 'True'

    airports = settings.AIRPORTS
    tl_tbl = settings.TRANSITION

    try:
        if len(metar) == 4:
            metar = download_metar(metar)

        metar = metarparse(metar)
        airport = airports[metar.location]
        parts = []

        parts.append(intro(letter, metar))
        if ',' in rwy:
            rwy = rwy.split(',')[0]
        parts.append(approach(rwy, airport))
        parts.append(transition_level(airport, tl_tbl, metar))
        if xpndr_startup and 'xpndr_startup' in airport:
            parts.append(airport['xpndr_startup'])
        if hiro and 'hiro' in airport:
            parts.append(airport['hiro'])
        if rwy_35_clsd and 'rwy_35_clsd' in airport:
            parts.append(airport['rwy_35_clsd'])
        if show_freqs:
            part = freqinfo(airport, tuple(getonlinestations(airport)))
            if part is not None:
                parts.append(part)
        parts.append(arrdep_info(airport, rwy))
        parts.append(wind(metar))
        if metar.report.sky:
            parts.append(weather(metar))
        parts.append(sky(metar))
        parts.append(temperature(metar))
        parts.append(dewpoint(metar))
        parts.append(qnh(metar))

        # general arrival and departure information
        for general_info in airport['general_info']:
            parts.append(general_info)

        parts.append('[ACK %s INFO] [%s]' % (metar.location, letter))

        return ' '.join(parts) if parts is not None else None
    except Exception as crap:
        if app.debug:
            raise
        logging.error(f'metar: {metar}')
        logging.error(f'out of service', exc_info=True)
        return '[ATIS OUT OF SERVICE]'
