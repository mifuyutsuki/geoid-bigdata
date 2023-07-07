# GeoID

Maps data scraper-parser for Indonesia places. Uses Selenium. CLI available.

## About

GeoID accepts a query or a list of queries based on (1) a single keyword and (2) a city or a list of cities in Indonesia. For example, given keyword `wisata` and city `kota bandung`, search for `wisata kota bandung`. The output is a JSON file containing the acquired search results. By default, GeoID does not "scroll down" search results; use `Config.query.depth` or CLI argument `-depth n` to change this setting.

The program pulls data from (1) the Google Maps search results page and (2) the kodeposku.com API to obtain location information from obtained coordinates. Due to the dynamic nature of the Google Maps frontend, Selenium is used to initialize a browser, with which the program can "scroll down" search results to obtain more results.

## Disclaimer

GeoID pulls from publicly available data on Google Maps. As an automated web scraper, usage of the program is a legal gray area and may violate Google's Terms of Service. Please use this program with caution.

The program does not and will not automatically bypass CAPTCHA.

## Requirements

* **Python** 3.11 or later
* **Selenium** 4.10 or later
  * Supported webdrivers: **Firefox** (default), **Chrome**

Other requirements are listed in requirements.txt. Installing the program using `pip` (see [Installation](#installation)) automatically installs the dependencies for you.

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
