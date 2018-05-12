from distutils.core import setup

setup(name="BEHRDownloader",
      version='0.1',
      description="Python utilities to download Berkeley High Resolution (BEHR) OMI NO2 data",
      author="Josh Laughner",
      author_email="jlaughner@berkeley.edu",
      url="http://behr.cchem.berkeley.edu",
      packages=['behrdownloader'],
      scripts=['behrdownloader/getbehr.py']
      )