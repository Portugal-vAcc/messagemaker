"""
Message Maker

Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmail.com>

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
from string import Template
from messagemaker import *
from bisect import bisect_right
import requests
import json
import traceback
from itertools import chain
from collections import namedtuple
from avweather.metar import parse as metarparse

def message_try(metar,
                rwy,
                letter,
                airports,
                tl_tbl,
                show_freqs = False,
                hiro=False,
                xpndr_startup=False,
                rwy_35_clsd=False):
    response = None
    try:
        response = message(
            metar,
            rwy,
            letter,
            airports,
            tl_tbl,
            show_freqs,
            hiro,
            xpndr_startup,
            rwy_35_clsd)
    except Exception as crap:
        print(traceback.format_exc())

    return '[ATIS OUT OF SERVICE]' if response is None else response

def freq(airport, online_freqs, freq_type):
    parts = airport[freq_type]
    for freq, part in parts:
        if freq in online_freqs:
            return freq, part

    return None, None

def freqinfo(airport, online_freqs):
    dep_freq, dep_msg = freq(airport, online_freqs, 'dep_freq')
    clr_freq, clr_msg = freq(airport, online_freqs, 'clr_freq')
    del_freq, _ = airport['clr_freq'][0]
    parts = []

    twr_online = True if airport['twr'] in online_freqs else False
    if dep_freq is not None:
        if dep_freq != clr_freq and twr_online:
            parts.append(dep_msg)
        parts.append(clr_msg)
        return ' '.join(parts)
    if clr_freq != del_freq and clr_msg is not None:
        parts.append(clr_msg)
        return ' '.join(parts)

def intro(letter, metar):
    template = '[$airport ATIS] [$letter] $time'
    return Template(template).substitute(
        airport=metar.location,
        letter=letter,
        time='%02d%02d' % (metar.time.hour, metar.time.minute))

def approach(rwy, airport):
    template = '[EXP ${approach} APCH] [RWY IN USE ${rwy}]'
    return Template(template).substitute(
        rwy=rwy,
        approach=airport['approaches'][rwy])

def transition_level(airport, tl_tbl, metar):
    template = '[TL] %s'
    transition_alt = airport['transition_altitude']
    index = bisect_right(
        tl_tbl[transition_alt],
        (float(metar.report.pressure),))
    _, transition_level = tl_tbl[transition_alt][index]
    return template % transition_level

def arrdep_info(airport, rwy):
    if rwy not in airport['arrdep_info']:
        return ''
    parts = []
    for rwy_message in airport['arrdep_info'][rwy]:
        parts.append(rwy_message)
    return ' '.join(parts)

def wind(metar):
    report = metar.report.wind
    parts = []
    if report.direction == 'VRB':
        parts.append('[WND] [VRB] %d [KT]' % report.speed)
    else:
        template = '[WND] ${direction} [DEG] ${speed} [KT]'
        part = Template(template).substitute(
            direction='%03d' % report.direction,
            speed='%d' % report.speed)

        # calm winds (to avoid WND 000 DEG 0 KT)
        if report.speed == 0:
            parts.append('[WND] [CALM]')
        else:
            parts.append(part)
    ## gusts
    if report.gust:
        template = '[MAX] ${gusts} [KT]'
        part = Template(template).substitute(
            gusts='%d' % report.gust
        )
        parts.append(part)
    ## variable
    if report.variable_from and report.variable_to:
        template = '[VRB BTN] ${direction_from} [AND] ${direction_to} [DEG]'
        part = Template(template).substitute(
            direction_from='%03d' % report.variable_from,
            direction_to='%03d' % report.variable_to
        )
        parts.append(part)
    return ' '.join(parts)

def weather(metar):
    weather = metar.report.sky.weather
    if not weather:
        return ''

    parts = []

    if weather.precipitation:
        precip = weather.precipitation
        if precip.intensity == '':
            parts.append('[MOD]')
        elif precip.intensity == '-':
            parts.append('[FBL]')
        elif precip.intensity == '+':
            parts.append('[HVY]')
        # handling 'Rain and Drizzle' case
        precip_phenomena = list(precip.phenomena)
        if 'RA' in precip_phenomena and 'DZ' in precip_phenomena:
            precip_phenomena.remove('RA')
            precip_phenomena.remove('DZ')
            precip_phenomena.append('RADZ')
        for phenomena in precip_phenomena:
            parts.append(f'[{phenomena}]')

    for obscur in weather.obscuration:
        parts.append(f'[{obscur}]')

    return ' '.join(parts)

def vis(metar):
    metar = metar.report.sky.visibility

    ## visibility
    # above or at 5km visibility is given in KM:
    #   5KM 6KM 7KM .. 10KM
    # below 5 km visibility is given in meters:
    #   4000M 3000M ..
    # calculate units, see issue #22
    units = 'MTS'
    vis = metar.distance
    if vis >= 5000:
        vis = int(vis / 1000)
        units = 'KM'
    if vis % 100 == 0:
        vis = '{%d}' % vis

    return f'[VIS] {vis}[{units}]'

def clouds(metar):
    return ' '.join(['[CLD]', *[
        f'[{c.amount}] [{c.type}] {{{c.height * 100}}} [FT]'
        if c.type else
        f'[{c.amount}] {{{c.height * 100}}} [FT]'
        for c in metar.report.sky.clouds
    ]])

def sky(metar):
    parts = []
    _metar = metar
    metar = metar.report.sky
    if not metar:
        parts.append('[CAVOK]')
    else:
        ## visibility
        # above or at 5km visibility is given in KM:
        #   5KM 6KM 7KM .. 10KM
        # below 5 km visibility is given in meters:
        #   4000M 3000M ..
        if metar.visibility and metar.visibility.distance < 10000:
            parts.append(vis(_metar))
        ## clouds
        clouds = metar.clouds
        if len(clouds) > 0:
            parts.append('[CLD]')
        for cloud in clouds:
            camount, cheight, ctype = cloud
            parts.append('[%s]' % camount)
            if ctype:
                parts.append('[%s]' % ctype)
            parts.append('{%d} [FT]' % (cheight * 100))
        if metar.verticalvis is not None:
            parts.append(f'[VV] {{{metar.verticalvis * 100}}} [FT]')
    return ' '.join(parts)

def temperature(metar):
    temperature = metar.report.temperature.air
    return f'[TEMP] {temperature}'

def dewpoint(metar):
    dewpoint = metar.report.temperature.dewpoint
    return f'[DP] {dewpoint}'

def qnh(metar):
    pressure = metar.report.pressure
    return f'[QNH] {pressure}'

def remove_windshear(metar):
    cases = ('WS ALL RWYS', 'WS R03', 'WS R21')
    for case in cases:
        windshear_index = metar.find(case)
        if windshear_index > -1:
            return metar[0:windshear_index]
    return metar

def message(metar,
            rwy,
            letter,
            airports,
            tl_tbl,
            show_freqs,
            hiro,
            xpndr_startup,
            rwy_35_clsd):
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

def download_metar(icao):
    return requests.get(
        'https://avwx.rest/api/metar/%s' % icao).json()['Raw-Report']

def getonlinestations(airport):
    """Returns all vatsim frequencies online at
    a given airport"""

    freqs = tuple(chain(airport['clr_freq'], airport['dep_freq']))
    freqs = { '{:0<7}'.format(freq) for freq, _ in freqs }

    where = ','.join(('{"frequency":"%s"}' % freq for freq in freqs))
    url = 'https://vatsim-status-proxy.herokuapp.com/clients?\
where={"$or":[%s]}' % where

    response = requests.get(url)
    if response.status_code != 200:
        return ()

    stations = json.loads(response.text)['_items']

    return (station['frequency'] for station in stations
                for callsign in airport['callsigns']
                    if callsign in station['callsign'])
