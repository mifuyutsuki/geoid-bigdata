from setuptools import setup, find_packages

version = {}
with open('./geoid/version.py') as f:
  exec(f.read(), version)
version = version['__version__']

with open('README.md', encoding='UTF-8') as f:
  readme = f.read()

install_requires = [
  'selenium>=4.10',
  'beautifulsoup4',
  'lxml',
  'requests',
  'unidecode'
]

#: Links pending publication

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