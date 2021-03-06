"""
Message Maker

Copyright (C) 2018 - 2019  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of messagemaker.

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
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from ddt import ddt, data, unpack
from avweather.metar import parse

from src.atis import *

@ddt
class TestLpptAtis(unittest.TestCase):

    def setUp(self):
        self.metar = parse('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0942')
        self.letter = 'A'

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 SCT027 11/06 Q1016',
        '[LPPT ATIS] [A] 1800'),
        ('METAR LPPT 190530Z 22009KT 9999 -RA FEW012 SCT015 BKN033 12/10 Q1014',
        '[LPPT ATIS] [A] 0530')
    )
    @unpack
    def test_intro(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(intro(metar, self.letter), expected)

    @data(
        ('03', '[EXP ILS APCH] [RWY IN USE 03]'),
        ('21', '[EXP ILS APCH] [RWY IN USE 21]'),
    )
    @unpack
    def test_approach(self, rwy, expected):
        self.assertEqual(approach(self.metar, rwy), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0942', '[TL] 75'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0943', '[TL] 70'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0959', '[TL] 70'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0960', '[TL] 65'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0976', '[TL] 65'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0978', '[TL] 60'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0994', '[TL] 60'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q0996', '[TL] 55'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1013', '[TL] 55'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1014', '[TL] 50'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1031', '[TL] 50'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1032', '[TL] 45'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1050', '[TL] 45'),
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1051', '[TL] 40'),
    )
    @unpack
    def test_transitionlevel(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(
            transition_level(metar),
            expected)

    @data(
        (
            ('121.750',),
            '121.750'
        ),
        (
            ('118.100',),
            '118.100'
        ),
        (
            ('121.750', '118.950'),
            '118.950'
        ),
    )
    @unpack
    def test_clrfreq(self, onlinefreqs, expected):
        f, _ = freq(self.metar, onlinefreqs, 'clr_freq')
        self.assertEqual(
            expected,
            f,
            str(onlinefreqs))

    @data(
        (
            ('119.100', '118.100'),
            '119.100'
        ),
        (
            ('125.550', '119.100', '118.100'),
            '119.100'
        ),
    )
    @unpack
    def test_depfreq(self, online_freqs, expected):
        f, _ = freq(self.metar, online_freqs, 'dep_freq')
        self.assertIn(
            expected,
            f,
            str(online_freqs))

    @data(
        (
            ('118.100', '118.950'),
            None
        ),
        (
            ('118.100', '121.750'),
            '[FOR DEP CLEARANCE CONTACT GND 121.750]'
        ),
        (
            ('119.100', '118.100', '118.950'),
            '[AFTER DEP CONTACT 119.1] [FOR DEP CLEARANCE CONTACT DEL 118.950]'
        ),
        (
            ('119.100', '118.950'),
            '[FOR DEP CLEARANCE CONTACT DEL 118.950]'
        ),
        (
            ('119.100', '121.750'),
            '[FOR DEP CLEARANCE CONTACT GND 121.750]'
        ),
        (
            ('125.550', '118.950'),
            '[FOR DEP CLEARANCE CONTACT DEL 118.950]'
        ),
        (
            ('125.550', '121.750'),
            '[FOR DEP CLEARANCE CONTACT GND 121.750]'
        ),
        (
            ('119.100',),
            '[ON THE GROUND CONTACT APP 119.1]'
        ),
        (
            (),
            None
        )
    )
    @unpack
    def test_freqinfo(self, online_freqs, expected):
        print('metar', self.metar)
        part = freqinfo(self.metar, online_freqs)
        self.assertEqual(
            expected,
            part,
            str(online_freqs))

    @data(
        ('03', '[AFTER LANDING VACATE VIA HN]'),
        ('21', '[AFTER LANDING VACATE VIA HS] [MEDIUM AND LGT AIRCRAFT EXP POSITION U FOR DEP \
TKOF AVBL DIST 2410 M IF UNABLE ADVISE BEFORE TAX]'),
        ('35', '')
    )
    @unpack
    def test_arrdepinfo(self, rwy, expected):
        self.assertEqual(
            arrdep_info(self.metar, rwy),
            expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 11/06 Q1016',
        '[WND] 350 [DEG] 15 [KT]'),
        ('METAR LPPT 191800Z 35015KT 350V010 9999 11/06 Q1016',
        '[WND] 350 [DEG] 15 [KT] [VRB BTN] 350 [AND] 010 [DEG]'),
        ('METAR LPPT 191800Z 35015G20KT 9999 11/06 Q1016',
        '[WND] 350 [DEG] 15 [KT] [MAX] 20 [KT]'),
        ('METAR LPPT 191800Z 35015G20KT 350V010 9999 11/06 Q1016',
        '[WND] 350 [DEG] 15 [KT] [MAX] 20 [KT] [VRB BTN] 350 [AND] 010 [DEG]'),
        ('METAR LPPT 191800Z 00000KT 9999 11/06 Q1016',
        '[WND] [CALM]'),
        ('METAR LPPT 191800Z VRB04KT 9999 11/06 Q1016',
        '[WND] [VRB] 4 [KT]'),
        ('METAR LPPT 191800Z VRB04G10KT 9999 11/06 Q1016',
        '[WND] [VRB] 4 [KT] [MAX] 10 [KT]'),
    )
    @unpack
    def test_wind(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(wind(metar), expected)

    @data(
        ('METAR LPPT 191800Z 36010KT 9999 11/06 Q1016',
        '[VIS] 10[KM]'),
        ('METAR LPPT 191800Z 36010KT 9000 11/06 Q1016',
        '[VIS] 9[KM]'),
        ('METAR LPPT 191800Z 36010KT 8000 11/06 Q1016',
        '[VIS] 8[KM]'),
        ('METAR LPPT 191800Z 36010KT 5000 11/06 Q1016',
        '[VIS] 5[KM]'),
        ('METAR LPPT 191800Z 36010KT 4500 11/06 Q1016',
        '[VIS] {4500}[MTS]'),
        ('METAR LPPT 191800Z 36010KT 4000 11/06 Q1016',
        '[VIS] {4000}[MTS]'),
        ('METAR LPPT 191800Z 36010KT 1000 11/06 Q1016',
        '[VIS] {1000}[MTS]'),
        ('METAR LPPT 191800Z 36010KT 0600 11/06 Q1016',
        '[VIS] {600}[MTS]'),
        ('METAR LPPT 191800Z 36010KT 0550 11/06 Q1016',
        '[VIS] 550[MTS]'),
        ('METAR LPPT 191800Z 36010KT 0250 11/06 Q1016',
        '[VIS] 250[MTS]'),
    )
    @unpack
    def test_vis(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(vis(metar), expected)

    @data(
        ('METAR LPPT 291530Z 31006KT 280V350 1200 R21/1900N +RADZ BKN004 FEW018CB 15/15 Q1017',
        '[RVR TDZ] {1900}[MTS]'),
    )
    @unpack
    def test_rvr(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(rvr(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 0100 RA 11/06 Q1016',
        '[MOD] [RA]'),
        ('METAR LPPT 191800Z 35015KT 0100 -RA 11/06 Q1016',
        '[FBL] [RA]'),
        ('METAR LPPT 191800Z 35015KT 0100 +RA 11/06 Q1016',
        '[HVY] [RA]'),
        ('METAR LPPT 191800Z 35015KT 0200 SHRA 11/06 Q1016',
        '[MOD] [SHRA]'),
        ('METAR LPPT 191800Z 35015KT 0300 -SHRA 11/06 Q1016',
        '[FBL] [SHRA]'),
        ('METAR LPPT 191800Z 35015KT 0300 +SHRA 11/06 Q1016',
        '[HVY] [SHRA]'),
        ('METAR LPPT 050820Z 12006KT 0400 FG VV002 04/03 Q1005',
        ''),
        ('METAR LPPT 050820Z 12006KT 0400 PRFG VV002 04/03 Q1005',
        ''),
        ('METAR LPPT 050820Z 12006KT 0400 RADZ FG VV002 04/03 Q1005',
        '[MOD] [RADZ]'),
        ('METAR LPPT 050820Z 12006KT 0400 -DZ PRFG VV002 04/03 Q1005',
        '[FBL] [DZ]'),
        ('METAR LPPT 050820Z 12006KT 0400 -DZ BCFG VV002 04/03 Q1005',
        '[FBL] [DZ]'),
        ('METAR LPPT 191800Z 35015KT 0300 BR 11/06 Q1016',
        ''),
    )
    @unpack
    def test_weather(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(weather(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 FEW003 11/06 Q1016',
        '[CLD] [FEW] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 SCT003 11/06 Q1016',
        '[CLD] [SCT] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 BKN003 11/06 Q1016',
        '[CLD] [BKN] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 OVC003 11/06 Q1016',
        '[CLD] [OVC] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 FEW030 11/06 Q1016',
        '[CLD] [FEW] {3000} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 FEW100 11/06 Q1016',
        '[CLD] [FEW] {10000} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 FEW040TCU 11/06 Q1016',
        '[CLD] [FEW] [TCU] {4000} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 FEW020CB 11/06 Q1016',
        '[CLD] [FEW] [CB] {2000} [FT]'),
    )
    @unpack
    def test_clouds(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(clouds(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016 RERA',
        '[RE][RA]'),
    )
    @unpack
    @unittest.expectedFailure
    def test_recentWeather(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(precip(metar), expected, 'issue #TODO')

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 11/06 Q1016',
        ''),
        ('METAR LPPT 191800Z 35015KT 9999 FEW003 11/06 Q1016',
        '[CLD] [FEW] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 SCT003 11/06 Q1016',
        '[CLD] [SCT] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 BKN003 11/06 Q1016',
        '[CLD] [BKN] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 OVC003 11/06 Q1016',
        '[CLD] [OVC] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 FEW030 11/06 Q1016',
        '[CLD] [FEW] {3000} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 FEW100 11/06 Q1016',
        '[CLD] [FEW] {10000} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 FEW040TCU 11/06 Q1016',
        '[CLD] [FEW] [TCU] {4000} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 FEW020CB 11/06 Q1016',
        '[CLD] [FEW] [CB] {2000} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 VV001 11/06 Q1016',
        '[VV] {100} [FT]'),
        ('METAR LPPT 191800Z 35015KT 9999 VV000 11/06 Q1016',
        '[VV] {0} [FT]'),
    )
    @unpack
    def test_sky(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(sky(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 FEW000 11/06 Q1016',
        '[CLD] [FEW] {0} [FT]')
    )
    @unpack
    def test_sky_gndlevel(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(sky(metar), expected, 'see: issue#15')

    @data(
        ('METAR LPPT 191800Z 35015KT CAVOK 10/05 Q1016', '[TEMP] 10'),
        ('METAR LPPT 191800Z 35015KT CAVOK 05/05 Q1016', '[TEMP] 5'),
        ('METAR LPPT 191800Z 35015KT CAVOK M10/05 Q1016', '[TEMP] -10'),
        ('METAR LPPT 191800Z 35015KT CAVOK M05/05 Q1016', '[TEMP] -5'),
        ('METAR LPPT 191800Z 35015KT CAVOK M00/05 Q1016', '[TEMP] 0'),
    )
    @unpack
    def test_temperature(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(temperature(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT CAVOK 10/10 Q1016', '[DP] 10'),
        ('METAR LPPT 191800Z 35015KT CAVOK 10/05 Q1016', '[DP] 5'),
        ('METAR LPPT 191800Z 35015KT CAVOK 10/M10 Q1016', '[DP] -10'),
        ('METAR LPPT 191800Z 35015KT CAVOK 10/M05 Q1016', '[DP] -5'),
        ('METAR LPPT 191800Z 35015KT CAVOK 10/M00 Q1016', '[DP] 0'),
    )
    @unpack
    def test_dewpoint(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(dewpoint(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT CAVOK 10/10 Q1016', '[QNH] 1016'),
        ('METAR LPPT 191800Z 35015KT CAVOK 10/10 Q0996', '[QNH] 996'),
    )
    @unpack
    def test_qnh(self, metar, expected):
        metar = parse(metar)
        self.assertEqual(qnh(metar), expected)
