"""
Message Maker

Copyright (C) 2018 - 2019  Pedro Rodrigues <prodrigues1990@gmail.com>
                           Bernardo Reis

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
import json
import requests
from itertools import chain

from . import settings

def get_online_stations(metar):
    airport = settings.AIRPORTS[metar.location]
    freqs = tuple(chain(airport['clr_freq'], airport['dep_freq']))
    freqs = { '{:0<7}'.format(freq) for freq, _ in freqs }

    where = ','.join((f'{{"frequency":"{freq}"}}' for freq in freqs))
    url = f'https://vatsim-api.herokuapp.com/clients?where={{"$or":[{where}]}}'

    response = requests.get(url)
    if response.status_code != 200:
        return ()

    stations = json.loads(response.text)['_items']

    return (
        station['frequency'] for station in stations
        for callsign in airport['callsigns']
        if callsign in station['callsign']
    )