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
import re
import requests

def download(icao):
    url = 'https://brief-ng.ipma.pt/showopmetquery.php'
    data = {'icaos': icao, 'type': 'metar'}

    response = requests.post(url, data)

    match = re.search(
        f'METAR\ .+$',
        response.text,
        re.MULTILINE,
    )

    return match.group() if match else ''