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
from messagemaker import app
import settings

@ddt
class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.airport = settings.AIRPORTS['LPPT']
        self.transition = settings.TRANSITION
        self.letter = 'A'
        self.rwy = '03'

        self.client = app.test_client()

    def get(self, metar, rwy, **kwargs):
        if 'letter' not in kwargs:
            kwargs['letter'] = 'A'
        url = f'/?metar={metar}&rwy={rwy}'

        for k, v in kwargs.items():
            url = url + f'&{k}={v}'
        resp = self.client.get(url)
        return resp.get_data(as_text=True)

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 SCT027 11/06 Q1016', '03')
    )
    @unpack
    def test_message_doesnotfail(self, metar, rwy):
        self.assertNotEqual(
            self.get(metar, rwy),
            '')

    @unittest.expectedFailure
    def test_message_containsprecipt(self):
        atis = self.get(
            'METAR LPPT 010200Z 35010KT 9999 RA SCT027 11/12 Q101',
            self.rwy)
        self.assertIn('RA', atis)

    @data(
        'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016 WS ALL RWYS',
        'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016 WS R03',
        'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016 WS R21',
    )
    def test_message_windshear_doesnotfail(self, metar):
        self.assertNotEqual(
            self.get(
                metar,
                self.rwy),
            '',
            'Python Metar module bug, see issue #13')

    def test_message_hiro(self):
        msg = self.get(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                hiro=True)
        self.assertIn('HIGH INTENSITY RWY OPS', msg)

        msg = self.get(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy)
        self.assertNotIn('HIGH INTENSITY RWY OPS', msg)

    def test_message_xpndrstartup(self):
        msg = self.get(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                xpndr_startup=True)
        self.assertIn('EXP XPNDR ONLY AT STARTUP', msg)

        msg = self.get(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy)
        self.assertNotIn('EXP XPNDR ONLY AT STARTUP', msg)

    def test_message_rwy_35_clsd(self):
        msg = self.get(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy,
                rwy_35_clsd=True)
        self.assertIn('RWY 35 CLSD FOR TKOF AND LDG AVBL TO TAXI', msg)

        msg = self.get(
                'METAR LPPT 191800Z 35015KT CAVOK 11/06 Q1016',
                self.rwy)
        self.assertNotIn('RWY 35 CLSD FOR TKOF AND LDG AVBL TO TAXI', msg)

        msg = self.get(
                'METAR LPFR 191800Z 35015KT CAVOK 11/06 Q1016',
                '10')
        self.assertNotIn('RWY 35 CLSD FOR TKOF AND LDG AVBL TO TAXI', msg)
