# Message Maker [![Build Status](https://travis-ci.org/pedro2555/messagemaker.svg?branch=master)](https://travis-ci.org/pedro2555/messagemaker)

Message Maker provides ATIS services for VATSIM at LPPT, LPPR, LPFR, and LPMA airfields.
All ATIS text and recordings are intended to be as close, as is possible on VATSIM, to the real ATIS provided by NAV Portugal at the respective airfields.

Without disconsideration to the above, information deemed as not useful on VATSIM and/or in simulation may not be provided, despite its publication on the real ATIS for the time or situation.

Message Maker is provided as free software under the terms of the GNU General Public License, version 2 of the license.
Other software used by Message Maker may be provided under different licenses, please refer to any 

## Running the application

Use the provided management script `manage.py`. Run `python manage.py` for a list of available options.

Make sure to use python 3.7 or above, install the requirements with

```pip install -r requirements.txt```

### Run the tests

```python manage.py test```

### Run the app

```python manage.py run```

If running a development serve use

```python manage.py run --debug```

## Usage options

All optional information available to display on the ATIS message is controlable via a corresponding URL parameter.

Some options are airport specific and are ignored where they do not apply.

### Show Frequencies

**default** True

This option is on by default but you can similarly disable it by forcing it to off:

`&show_freqs=False`

Displays information of frequencies to contact on ground and/or after departure, when they differ from the ones published on the charts.

### Transponder on startup

```
&xpndr_startup=True

EXP XPNDR ONLY AT STARTUP
```

### Runway 35 closed

```
&rwy_35_clsd=True

RWY 35 CLSD FOR TKOF AND LDG AVBL TO TAXI
```

### High intensity runway operations

```
&hiro=True

HIGH INTENSITY RWY OPS
```


## Euroscope Installation

1. Get the [latest audio package.zip](https://github.com/pedro2555/messagemaker/releases/latest), extract to `Documents/Euroscope/messagemaker/`.

![Screenshot_4](https://user-images.githubusercontent.com/1645623/54699336-b93bf480-4b28-11e9-9673-5a3600ccb96a.jpg)

![image](https://user-images.githubusercontent.com/1645623/38401424-92d36974-394d-11e8-9bb0-c5e2535b1de8.png)

2. On the `Voice ATIS Setup Dialog` in Euroscope, select the `atisfiles.txt` included with the audio package

![image](https://user-images.githubusercontent.com/1645623/38401444-b149ae54-394d-11e8-9b5a-e95d8944f86e.png)

3. On the same dialog, replace your current `ATIS Maker URL` with:

    `https://messagemaker.herokuapp.com/?metar=$metar($atisairport)&rwy=$arrrwy($atisairport)&letter=$atiscode`

## Contributing

Make sure your contributions fall under projecto scope above, and submit either an issue or a pull request.

If your pull request includes code, make sure it includes test cases for, at least, the most basic functionality it provides.

Welcome changes:

 - PEP8. Thats a big failure from the start.
