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
from avweather.metar import parse

OPTIONS = (
   #('name'         , required, coerse, default)
    ('hiro'         , False   , bool  , False),
    ('letter'       , True    , str   , ''),
    ('metar'        , True    , str   , ''),
    ('rwy'          , True    , str   , ''),
    ('rwy_35_clsd'  , False   , bool  , False),
    ('show_freqs'   , False   , bool  , True),
    ('xpndr_startup', False   , bool  , False),
)

def bool(string):
    return string.lower() == 'true'

def verify_args(args):
    return [
        name
        for name, required, _, _ in OPTIONS
        if required and name not in args
    ]

def parse_args(args):
    return {
        name: coerse(args.get(name, default))
        for name, _, coerse, default in OPTIONS
    }

def get_metar(args):
    if len(args['metar']) == 4:
        raw_metar = _download(args['metar'])
    else:
        raw_metar = args['metar']
    
    return parse(raw_metar)

def _download(icao):
    return 'LPPT 110600Z 03003KT 9999 FEW014 12/12 Q1020'

def get_rwy(args):
    # if 2 or more rwys are selected in Euroscope, pick the first one
    return args['rwy'].split(',')[0]

def get_letter(args):
    return args['letter']

def has_option_set(args, option):
    return args.get(option, False)
