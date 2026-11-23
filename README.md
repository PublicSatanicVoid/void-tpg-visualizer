# Void TPG Visualizer

Generates KML file with voided zones for Void TPG (Travel Picture Game).

Zones are voided in two ways:

1. Submitting a location voids everywhere within a certain radius of it. This radius expands with each round.

2. Counties are randomly voided each round.

## Usage

Installation with Python virtual environment:

```
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

County boundaries downloaded [from US Census Bureau](https://www2.census.gov/geo/tiger/GENZ2018/kml/cb_2018_us_county_500k.zip)

```
curl -O https://www2.census.gov/geo/tiger/GENZ2018/kml/cb_2018_us_county_500k.zip
unzip cb_2018_us_county_500k.zip
```

Add void circles and counties by editing `main.py`

Then rerun with:
```
./venv/bin/python3 main.py
```

The resulting KML file will be at `out.kml`
