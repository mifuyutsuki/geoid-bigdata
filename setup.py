# Copyright (c) 2023 mifuyutsuki

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
setup.py to install GeoID. 
"""


from setuptools import setup, find_packages


version = {}
with open('./geoid/version.py') as f:
  exec(f.read(), version)
version = version['__version__']

with open('README.md', encoding='UTF-8') as f:
  readme = f.read()

install_requires = []
with open('requirements.txt', encoding='UTF-8') as f:
  for line in f:
    install_requires.append(line.strip())


setup(
  name='geoid-bigdata',
  version=version,
  description='Maps data scraper-parser for Indonesia places',
  long_description=readme,
  long_description_content_type='text/markdown',
  url='https://github.com/mifuyutsuki/geoid-bigdata',
  author='mifuyutsuki',
  classifiers=[  
    "Development Status :: 3 - Alpha"
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11"
  ],
  keywords='maps, scraper, indonesia',
  package_dir={'': 'geoid'},
  packages=find_packages(where='geoid'),
  python_requires='>=3.11, <4',
  install_requires=install_requires,
  entry_points={
    "console_scripts": [
      "geoid=cli.cli:start"
    ],
  }
)