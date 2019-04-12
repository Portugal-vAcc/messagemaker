"""
Message Maker

Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmail.com>

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
from metar import Metar

from messagemaker.message import *
import settings

@ddt
class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.airport = settings.AIRPORTS['LPPT']
        self.transition = settings.TRANSITION
        self.letter = 'A'
        self.rwy = '03'

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 SCT027 11/06 Q1016', '03')
    )
    @unpack
    def test_message_doesnotfail(self, metar, rwy):
        self.assertNotEqual(
            message(
                metar,
                rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                False,
                False,
                False),
            '')

    @unittest.expectedFailure
    def test_message_containsprecipt(self):
        atis = message(
            'METAR LPPT 010200Z 35010KT 9999 RA SCT027 11/12 Q101',
            self.rwy,
            self.letter,
            settings.AIRPORTS,
            settings.TRANSITION,
            False,
            False,
            False,
            False)
        self.assertIn('RA', atis)

    @data(
        'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016 WS ALL RWYS',
        'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016 WS R03',
        'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016 WS R21',
    )
    def test_message_windshear_doesnotfail(self, metar):
        self.assertNotEqual(
            message(
                metar,
                self.rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                False,
                False,
                False),
            '',
            'Python Metar module bug, see issue #13')

    def test_message_hiro(self):
        msg = message(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                True,
                False,
                False)
        self.assertIn('HIGH INTENSITY RWY OPS', msg)

        msg = message(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                False,
                False,
                False)
        self.assertNotIn('HIGH INTENSITY RWY OPS', msg)

    def test_message_xpndrstartup(self):
        msg = message(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                False,
                True,
                False)
        self.assertIn('EXP XPNDR ONLY AT STARTUP', msg)

        msg = message(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                False,
                False,
                False)
        self.assertNotIn('EXP XPNDR ONLY AT STARTUP', msg)

    def test_message_rwy_35_clsd(self):
        msg = message(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                False,
                False,
                True)
        self.assertIn('RWY 35 CLSD FOR TKOF AND LDG AVBL TO TAXI', msg)

        msg = message(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                False,
                False,
                False)
        self.assertNotIn('RWY 35 CLSD FOR TKOF AND LDG AVBL TO TAXI', msg)

        msg = message(
                'METAR LPFR 191800Z 35015KT CAVOK 11/06 Q1016',
                '10',
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION,
                False,
                False,
                False,
                True)
        self.assertNotIn('RWY 35 CLSD FOR TKOF AND LDG AVBL TO TAXI', msg)
