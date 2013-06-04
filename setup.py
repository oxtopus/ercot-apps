from setuptools import setup

requirements = map(str.strip, open('requirements.txt').readlines())

setup(
  name = 'ercot.apps',
  description = "ERCOT Scraper Sample Apps",
  classifiers = \
    [
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Topic :: Software Development :: Libraries',
    ],
  keywords = 'ercot',
  author = 'Austin Marshall',
  author_email = 'oxtopus@gmail.com',
  url = 'https://github.com/oxtopus/ercot.apps',
  license = 'MIT',
  namespace_packages = ['ercot'],
  packages = ['ercot', 'ercot.apps'],
  entry_points = \
    {
      'console_scripts': \
        [
          'system_wide_demand = ercot.apps.system_wide_demand:system_wide_demand'
        ]
    },
  requires = requirements,
  install_requires = requirements,
  dependency_links = [
        "https://github.com/oxtopus/ercot/archive/0.0.3.tar.gz#egg=ercot-0.0.3"
    ]
)
