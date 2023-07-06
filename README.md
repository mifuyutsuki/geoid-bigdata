# GeoID

Maps data scraper-parser for Indonesia places. Uses Selenium. CLI available.

## Requirements

* **Python** 3.11 or later
* **Selenium** 4.10 or later
  * Supported webdrivers: **Firefox**, **Chrome**

See also requirements.txt. Installing the program using `pip` (see **Installation**) automatically installs the dependencies for you.

## About

GeoID accepts a query or a list of queries based on a single keyword and a city or a list of cities. For example, given keyword `wisata` and city `kota bandung`, search for `wisata kota bandung`. The output is a JSON file containing the acquired search results. By default, GeoID does not scroll down search results; use `Config.query.depth` or CLI argument `-depth n` to change this setting.

The program pulls data from the Google Maps search results page and the kodeposku.com API to obtain location information from obtained coordinates.

## Installation

### Using PyPI (`pip`)

Linux/MacOS (Unix):

```bash
pip install geoid-bigdata
```

Windows:

```bash
python -m pip install geoid-bigdata
```

### From source

Clone this repository:

```bash
git clone https://github.com/           /geoid-bigdata
```

On the repository path (using `cd` or by launching a new terminal in the path),

```bash
python setup.py install
```
