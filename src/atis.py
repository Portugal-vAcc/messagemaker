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
import requests
import json
import traceback
from string import Template
from bisect import bisect_right
from itertools import chain
from collections import namedtuple
from avweather.metar import parse as metarparse
from avweather._metar_parsers import pwind

from . import settings

def freq(metar, online_freqs, freq_type):
    airport = settings.AIRPORTS[metar.location]
    parts = airport[freq_type]
    for freq, part in parts:
        if freq in online_freqs:
            return freq, part

    return None, None

def freqinfo(metar, online_freqs):
    airport = settings.AIRPORTS[metar.location]
    dep_freq, dep_msg = freq(metar, online_freqs, 'dep_freq')
    clr_freq, clr_msg = freq(metar, online_freqs, 'clr_freq')
    try:
        del_freq, _ = airport['clr_freq'][0]
    except IndexError:
        del_freq = None
    twr_online = airport['twr'] in online_freqs

    parts = []
    if dep_freq is not None:
        if dep_freq != clr_freq and twr_online:
            parts.append(dep_msg)
        parts.append(clr_msg)
        return ' '.join(parts)
    if clr_freq != del_freq and clr_msg is not None:
        parts.append(clr_msg)
        return ' '.join(parts)

def get_freq_info(metar, vatsim_data):
    return ''

def intro(metar, letter):
    time = f'{metar.time.hour:02}{metar.time.minute:02}'
    return f'[{metar.location} ATIS] [{letter}] {time}'

def approach(metar, rwy):
    airport = settings.AIRPORTS[metar.location]
    approach = airport['approaches'][rwy]
    return f'[{approach}] [RWY IN USE {rwy}]'

def transition_level(metar):
    airport = settings.AIRPORTS[metar.location]
    tl_tbl = settings.TRANSITION
    transition_alt = airport['transition_altitude']

    index = bisect_right(
        tl_tbl[transition_alt],
        (float(metar.report.pressure),)
    )
    _, transition_level = tl_tbl[transition_alt][index]

    return f'[TL] {transition_level}'

def arrdep_info(metar, rwy):
    airport = settings.AIRPORTS[metar.location]
    if rwy not in airport['arrdep_info']:
        return ''
    parts = []
    for rwy_message in airport['arrdep_info'][rwy]:
        parts.append(rwy_message)
    return ' '.join(parts)

def wind(metar):
    wind = metar.report.wind
    if (wind.direction == '///' or wind.speed == '//') and 'WIND' in metar.unmatched:
        wind = get_rmk_wind(metar)
    parts = []
    if wind.direction == 'VRB':
        parts.append(f'[WND] [VRB] {wind.speed} [KT]')
    else:
        # calm winds (to avoid WND 000 DEG 0 KT)
        if wind.speed == 0:
            parts.append('[WND] [CALM]')
        elif wind.direction != '///' and wind.speed != '//':
            parts.append(f'[WND] {wind.direction:03} [DEG] {wind.speed} [KT]')

    if wind.gust:
        parts.append(f'[MAX] {wind.gust} [KT]')
    if wind.variable_from and wind.variable_to:
        parts.append(f'[VRB BTN] {wind.variable_from:03} [AND] {wind.variable_to:03} [DEG]')
    return ' '.join(parts)

def get_rmk_wind(metar):
    for part in metar.unmatched.split():
        wind, _ = pwind(part)

        if wind is not None:
            return wind

def weather(metar):
    if not metar.report.sky:
        return None

    weather = metar.report.sky.weather
    if not weather:
        return None

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
        vis = f'{{{vis}}}'

    return f'[VIS] {vis}[{units}]'

def clouds(metar):
    return ' '.join(['[CLD]', *[
        f'[{c.amount}] [{c.type}] {{{c.height * 100}}} [FT]'
        if c.type else
        f'[{c.amount}] {{{c.height * 100}}} [FT]'
        for c in metar.report.sky.clouds
    ]])

def rvr(metar):
    _, rvr = metar.report.sky.rvr[0]
    units = 'MTS'
    rvr = rvr.distance
    if rvr >= 5000:
        rvr = int(rvr / 1000)
        units = 'KM'
    if rvr % 100 == 0:
        rvr = f'{{{rvr}}}'

    return f'[RVR TDZ] {rvr}[{units}]'


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
        if metar.rvr:
            parts.append(rvr(_metar))
        for obscur in metar.weather.obscuration:
            parts.append(f'[{obscur}]')
        ## clouds
        clouds = metar.clouds
        if len(clouds) > 0:
            parts.append('[CLD]')
        for cloud in clouds:
            camount, cheight, ctype = cloud
            parts.append(f'[{camount}]')
            if ctype:
                parts.append(f'[{ctype}]')
            cheight = cheight * 100
            parts.append(f'{{{cheight}}} [FT]')
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

def get_airport_option(metar, option):
    airport = settings.AIRPORTS[metar.location]
    value = airport.get(option) 
    return value if isinstance(value, list) else [value]

def ack(metar, letter):
    return f'[ACK {metar.location} INFO] [{letter}]'