from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime as dtime, timedelta as tdel
import urllib2

__metaclass__ = type  # Automatically makes Python 2 classes inherit from object to be new-style classes

version_file = 'http://behr.cchem.berkeley.edu/behr/behr_version.txt'
name_fmt_string = 'OMI_BEHR-{}_{}_{}_{}.hdf'

def get_current_behr_version():
    # Only read 32 characters from the file - that should be more than enough for a version string like v3-0Arev1 and
    # prevents flooding the user's computer with unnecessary data
    version_string = urllib2.urlopen(version_file).read(32)
    return version_string

def iter_file_list(region, profile_mode, start_date, end_date):
    start_dt = dtime.strptime(start_date, '%Y-%m-%d')
    end_dt = dtime.strptime(end_date, '%Y-%m-%d')
    version = get_current_behr_version()

    one_day = tdel(days=1)
    curr_dt = start_dt
    while curr_dt <= end_dt:
        file_name = name_fmt_string.format(profile_mode.upper(), region.upper(), version, curr_dt.strftime('%Y%m%d'))
        yield file_name
        curr_dt += one_day

def print_file_list_debug(region, profile_mode, start_date, end_date):
    for f in iter_file_list(region, profile_mode, start_date, end_date):
        print(f)