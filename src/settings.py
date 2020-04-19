"""
Message Maker

Copyright (C) 2018 - 2019  Pedro Rodrigues <prodrigues1990@gmail.com>
                           Bernardo Reis <bernardo.paranhos.reis@gmail.com>
                           Hugo Santos <hugogpsantos@gmail.com>

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

LPPT = {
    'approaches': {
        '03': 'EXP ILS APCH',
        '21': 'EXP ILS APCH',
        '35': 'EXP VOR DME APCH',
        '17': 'EXP VISUAL APCH'
    },
    'arrdep_info': {
        '03': [
            '[AFTER LANDING VACATE VIA HN]'
        ],
        '21': [
            '[AFTER LANDING VACATE VIA HS]',
            '[MEDIUM AND LGT AIRCRAFT EXP POSITION U FOR DEP TKOF AVBL DIST 2410 M IF UNABLE \
ADVISE BEFORE TAX]',
        ]
    },
    'general_info': [
        '[COMPLY WITH SPEED LIMITATIONS UNLESS OTHERWISE ADVISED BY ATC]'
    ],
    'transition_altitude': '4000',
    'clr_freq': (
        # freq, contact message
        ('118.950', '[FOR DEP CLEARANCE CONTACT DEL 118.950]'),
        ('121.750', '[FOR DEP CLEARANCE CONTACT GND 121.750]'),
        ('118.100', '[FOR DEP CLEARANCE CONTACT TWR 118.100]'),
        ('119.100', '[ON THE GROUND CONTACT APP 119.1]'),
        ('136.025', '[ON THE GROUND CONTACT 136.025]'),
        ('125.550', '[ON THE GROUND CONTACT 125.55]'),
    ),
    'dep_freq': (
        ('119.100', '[AFTER DEP CONTACT 119.1]'),
        ('136.025', '[AFTER DEP CONTACT 136.025]'),
        ('125.550', '[AFTER DEP CONTACT 125.55]'),
    ),
    'twr': '118.100',
    'callsigns': (
       'LPPT',
       'LPPC',
    ),
    'hiro': '[HIGH INTENSITY RWY OPS]',
    'xpndr_startup': '[EXP XPNDR ONLY AT STARTUP]',
    'rwy_35_clsd': '[RWY 35 CLSD FOR TKOF AND LDG AVBL TO TAXI]'
}
LPFR = {
    'approaches': {
        '10': 'EXP R-NAV APCH',
        '28': 'EXP ILS APCH'
    },
    'arrdep_info': {
        '10': [],
        '28': []
    },
    'general_info': [],
    'transition_altitude': '4000',
    'clr_freq': (
        # freq, contact message
        ('118.575', ''),
        ('120.750', '[GND CLOSED]'),
        ('119.400', '[ON THE GROUND CONTACT APP 119.4]'),
        ('132.700', '[ON THE GROUND CONTACT 132.7]'),
        ('136.025', '[ON THE GROUND CONTACT 136.025]'),
        ('125.55', '[ON THE GROUND CONTACT 125.55]'),
    ),
    'twr': '120.750',
    'dep_freq': (),
    'callsigns': (
       'LPFR',
       'LPPC',
    ),
}
LPPR = {
    'approaches': {
        '17': 'EXP ILS DME APCH',
        '35': 'R-NAV'
    },
   'arrdep_info': {
        '17': [],
        '35': []
    },
    'general_info': [],
    'transition_altitude': '4000',
    'clr_freq': (
        # freq, contact message
        ('118.925', '[FOR ATC CLEARANCE CONTACT PORTO DEL]'),
        ('118.000', '[PORTO DEL CLOSED]'),
        ('121.100', '[FREQ 118.0 CLOSED CONTACT FREQ 121.1]'),
        ('132.300', '[ON THE GROUND CONTACT 132.3]'),
        ('136.025', '[ON THE GROUND CONTACT 136.025]'),
        ('125.550', '[ON THE GROUND CONTACT 125.55]'),
    ),
    'dep_freq': (),
    'twr': '118.000',
    'callsigns': (
       'LPPR',
       'LPPC',
    ),
}
LPMA = {
    'approaches': {
        '05': 'EXP VOR DME APCH OTHER APPROACHES AVBL O/R',
        '23': 'EXP VOR DME APCH OTHER APPROACHES AVBL O/R'
    },
    'arrdep_info': {
        '05': [],
        '23': []
    },
    'general_info': [],
    'transition_altitude': '5000',
    'clr_freq': (
        # freq, contact message
        ('118.350', '[ON THE GROUND CONTACT TWR 118.350]'),
        ('119.600', '[ON THE GROUND CONTACT APP 119.6]'),
        ('132.250', '[ON THE GROUND CONTACT 132.25]'),
        ('131.325', '[ON THE GROUND CONTACT 131.325]'),
        ('125.550', '[ON THE GROUND CONTACT 125.55]'),
    ),
    'dep_freq': (),
    'twr': '118.350',
    'callsigns': (
       'LPMA',
       'LPPC',
    ),
}
LPPD = {
    'approaches': {
        '12': 'EXP R-NAV APCH',
        '30': 'EXP ILS APCH'
    },
    'arrdep_info': {
        '12': [],
        '30': []
    },
    'general_info': [],
    'transition_altitude': '6000',
    'clr_freq': (
        # freq, contact message
        ('118.300', ''),
        ('119.400', '[ON THE GROUND CONTACT APP 119.4]'),
        ('132.150', '[ON THE GROUND CONTACT 132.150]'),
        ('132.075', '[ON THE GROUND CONTACT 132.075]'),
    ),
    'twr': '118.300',
    'dep_freq': (),
    'callsigns': (
       'LPPD',
       'LPPO',
    ),
}
LPLA = {
    'approaches': {
        '15': 'EXP ILS APCH',
        '33': 'EXP ILS APCH'
    },
    'arrdep_info': {
        '15': ['[IN CASE OF GO AROUND FLY RWY HDG CLIMB TO 3000 FT]',
               '[CAUTION HIGH TERRAIN BOTH SIDES OF RWY]'],
        '33': ['[CAUTION HIGH TERRAIN BOTH SIDES OF RWY]']
    },
    'general_info': [],
    'transition_altitude': '5000',
    'clr_freq': (
        # freq, contact message
        ('121.900', ''),
        ('122.100', '[ON THE GROUND CONTACT TWR 122.100]'),
        ('135.000', '[ON THE GROUND CONTACT APP 135.000]'),
        ('132.150', '[ON THE GROUND CONTACT 132.150]'),
        ('132.075', '[ON THE GROUND CONTACT 132.075]'),
    ),
    'twr': '122.100',
    'dep_freq': (),
    'callsigns': (
       'LPLA',
       'LPPO',
    ),
}

AIRPORTS = {
    'LPPT': LPPT,
    'LPFR': LPFR,
    'LPPR': LPPR,
    'LPMA': LPMA,
    'LPPD': LPPD,
    'LPLA': LPLA,
}

TRANSITION = {
    '4000': [
        (942.1, '75'),
        (959.4, '70'),
        (977.1, '65'),
        (995.0, '60'),
        (1013.2, '55'),
        (1031.6, '50'),
        (1050.3, '45'),
        (9999, '40')
    ],
    '5000': [
        (942.1, '85'),
        (959.4, '80'),
        (977.1, '75'),
        (995.0, '70'),
        (1013.2, '65'),
        (1031.6, '60'),
        (1050.3, '55'),
        (9999, '50')
    ],
    '6000': [
        (942.1, '95'),
        (959.4, '90'),
        (977.1, '85'),
        (995.0, '80'),
        (1013.2, '75'),
        (1031.6, '70'),
        (1050.3, '65'),
        (9999, '60')
    ],
    '8000': [
        (942.1, '115'),
        (959.4, '110'),
        (977.1, '105'),
        (995.0, '100'),
        (1013.2, '95'),
        (1031.6, '90'),
        (1050.3, '85'),
        (9999, '80')
    ]
}
