# Message Maker [![Build Status](https://travis-ci.org/pedro2555/messagemaker.svg?branch=master)](https://travis-ci.org/pedro2555/messagemaker)

Message Maker provides ATIS services for VATSIM at LPPT, LPPR, LPFR, and LPMA airfields.
All ATIS text and recordings are intended to be as close, as is possible on VATSIM, to the real ATIS provided by NAV Portugal at the respective airfields.

Without disconsideration to the above, information deemed as not useful on VATSIM and/or in simulation may not be provided, dispite its publication on the real ATIS for the time or situation.

Message Maker is provided as free software under the terms of the GNU General Public License, version 2 of the license.
Other software used by Message Maker may be provided under different licenses, please refer to any 

## Contributing

Make sure your contributions fall under projecto scope above, and submit either an issue or a pull request.

If your pull request includes code, make sure it includes test cases for, at least, the most basic functionality it provides.

Welcome changes:

 - PEP8. Thats a big failure from the start.



Available at:
https://messagemaker.herokuapp.com/?metar=LPPT&rwy=21&letter=A

https://messagemaker.herokuapp.com/?metar=$metar($atisairport)&rwy=$arrrwy($atisairport)&letter=$atiscode
