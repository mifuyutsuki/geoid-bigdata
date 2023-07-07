from setuptools import setup
from geoid import __version__

with open('README.md', encoding='UTF-8') as f:
  readme = f.read()

install_requires = [
  'selenium>=4.10',
  'beautifulsoup4',
  'lxml',
  'requests',
  'unidecode'
]

#: Author and links pending publication

setup(
  name='geoid-bigdata',
  version=__version__,
  description='Maps data scraper-parser for Indonesia places',
  long_description=readme,
  long_description_content_type='text/markdown',


  classifiers=[  
    "Programming Language :: Python :: 3.11"
  ],
  keywords='maps, scraper, indonesia',
  package_dir={'': 'geoid'},
  python_requires='>=3.11, <4',
  install_requires=install_requires
)