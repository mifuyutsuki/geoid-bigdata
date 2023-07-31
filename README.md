# GeoID

Maps data scraper-parser for Indonesia places.

## Table of Contents

* [About](#about)
* [Disclaimer](#disclaimer)
* [Requirements](#requirements)
* [Installation](#installation)
  * [(TBA) PyPI](#tba-pypi)
  * [From source](#from-source)

## About

GeoID is a web scraper for places in Google Maps, designed primarily as a CLI and specifically for locations in Indonesia.

GeoID runs a search/query of places generally given by a 'term' and a 'city', combined to create a query keyword "`term` `city`". For example, given keyword `wisata` and city `kota bandung`, search for `wisata kota bandung`. The set of terms, cities, and keywords are given by a file which can be generated (using `geoid generate`) and customized. The output is a JSON file containing places from the search results.

By default, GeoID does not "scroll down" search results; use argument `-d n` or `--depth n`, where n is the number of "scrolls", to change this setting. Using `--depth 0` makes GeoID scroll down as much as it can (called "infinite scroll" or "infinite depth").

The program pulls data from (1) the Google Maps search results page to obtain places and (2) the kodeposku.com API to obtain location information from obtained coordinates. Due to the dynamic nature of the Google Maps frontend, an automated web browser (in this case Selenium) is used, with which the program can dynamically interact with the web page.

GeoID is created as part of an internship program.

## Disclaimer

GeoID pulls from publicly available data on Google Maps. As an automated web scraper, usage of the program is a legal gray area and may violate Google's Terms of Service. Please use this program with caution.

The program does not and will not automatically bypass CAPTCHA.

## Requirements

* **Python** 3.11 or later
* **Selenium** 4.10 or later
  * Supported browsers: **Chrome** (default), **Firefox**

GeoID also uses the following libraries:

* **BeautifulSoup4**
* **requests**
* **lxml**
* **selenium-stealth**
* **backoff**

While Selenium supports [additional browsers](https://www.selenium.dev/documentation/webdriver/browsers/), GeoID has only been tested on the above. Using **Chrome** is recommended as the program can benefit from `selenium-stealth`.

Using `pip install -r requirements.txt` during installation automatically installs the dependencies for you. Browsers are not included in the automatic installation.

## Installation

Depending on your setup, you may need to substitute `python` below with `python3` (Unix/macOS), `py` (Windows).

### (TBA) PyPI

*To be announced.*

### From source

The following setup uses `git` to clone this repository.

```bash
git clone https://github.com/mifuyutsuki/geoid-bigdata
cd geoid-bigdata
python setup.py install
```

The setup will additionally install any dependencies needed by GeoID.
