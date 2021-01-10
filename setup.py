# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brew_control_dash']

package_data = \
{'': ['*']}

install_requires = \
['dash>=1.18.1,<2.0.0']

setup_kwargs = {
    'name': 'brew-control-dash',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Erin Arai',
    'author_email': 'erin.arai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
