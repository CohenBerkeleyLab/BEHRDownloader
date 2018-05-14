#!/usr/bin/env python
from __future__ import print_function
import argparse
import datetime as dt
import os
import requests
import shutil
import tarfile

import pdb

dash_root = "https://dash.ucop.edu"
request_params = {"accept": "application/json"}
default_block_size_bytes = 4096

behr_dois = {'daily-gridded': 'doi:10.6078/D12D5X',
             'monthly-gridded': 'doi:10.6078/D1RQ3G',
             'daily-native': 'doi:10.6078/D1WH41',
             'monthly-native': 'doi:10.6078/D1N086'}

def replace_ascii_html(s):
    html_table = {':': '%3A',
                  '/': '%2F'}
    for k, v in html_table.items():
        s = s.replace(k, v)

    return s


def get_dash_files_from_doi(doi):
    doi = replace_ascii_html(doi)
    # First, we get a list of all versions associated with this DOI
    versions = requests.get("{}/api/datasets/{}/versions".format(dash_root, doi), params=request_params)

    # Find the most recent version
    newest_version = -1
    newest_idx = -1
    for idx, a_version in enumerate(versions.json()['_embedded']['stash:versions']):
        if a_version['versionNumber'] > newest_version:
            newest_version = a_version['versionNumber']
            newest_idx = idx

    if newest_idx < 0:
        raise RuntimeError('Failed to find the newest version')

    # Assuming that the list of versions is in chronological order, we want the most recent one
    # In that version is the URL to request the files
    file_url = versions.json()['_embedded']['stash:versions'][newest_idx]['_links']['stash:files']['href']

    # Now we can retrieve a list of the available files
    file_list = requests.get("{}{}".format(dash_root, file_url), params=request_params).json()['_embedded'][
        'stash:files']

    # Extract the file name and link into a more easily comprehendable dict
    return {f['path']: dash_root + f['_links']['stash:download']['href'] for f in file_list}


def download_file(url, out_name, block_size=default_block_size_bytes):

    # Requesting the URL as a stream will not try to download the entire file at once
    dl_obj = requests.get(url, stream=True)
    dl_obj.raise_for_status()

    with open(out_name, 'wb') as outfile:
        for block in dl_obj.iter_content(block_size):
            outfile.write(block)


def extract_tar_file(filename, delete_tar=False, verbose=0, logging_fxn=print):
    extract_path = os.path.dirname(filename)
    with tarfile.open(filename, 'r:gz') as tarobj:
        tarobj.extractall(path=extract_path)
    if delete_tar:
        if verbose > 0:
            logging_fxn('Deleting {}'.format(filename))
        os.remove(filename)


def iter_months(start, end):
    curr_date = start.replace(day=1)
    while curr_date <= end:
        yield curr_date
        curr_date += dt.timedelta(days=32)
        curr_date = curr_date.replace(day=1)


def iter_files_for_dates(filenames, start, end):
    for date in iter_months(start, end):
        date_string = date.strftime('%Y%m')
        for f in filenames.keys():
            if date_string in f:
                yield f, filenames[f]
                break  # break the inner loop, assume that there's only one file per month


def driver(dataset, out_dir, start, end, extract_tar=False, delete_tar=False, logging_fxn=print, verbose=0, **kwargs):
    if not dataset.startswith('doi'):
        try:
            dataset = behr_dois[dataset]
        except KeyError:
            raise ValueError('dataset must be a DOI string beginning with "doi" or one of the following strings: {}'.format(
                ', '.join(behr_dois.keys())
            ))

    if not os.path.isdir(out_dir):
        raise ValueError('outdir must be an existing directory')

    file_dict = get_dash_files_from_doi(dataset)
    for fname, url in iter_files_for_dates(file_dict, start, end):
        save_name = os.path.join(out_dir, fname)
        if verbose > 0:
            logging_fxn('Saving {} as {}'.format(url, save_name))
        download_file(url, save_name)
        if extract_tar:
            if verbose > 0:
                logging_fxn('Extracting {}'.format(save_name))
            extract_tar_file(save_name, delete_tar=delete_tar, verbose=verbose, logging_fxn=logging_fxn)


def parse_cl_date(date_string):
    return dt.datetime.strptime(date_string, '%Y-%m')


def parse_args(parser=None):
    called_as_subcommand = parser is not None
    description = 'Interface to batch download BEHR files from University of California DASH'
    epilog = 'Example: {} daily-gridded 2005-01 2005-02'.format(os.path.basename(__file__))
    if not called_as_subcommand:
        parser = argparse.ArgumentParser(description=description, epilog=epilog)

    parser.add_argument('dataset', choices=behr_dois.keys(), help='Which dataset to download.')
    parser.add_argument('start', type=parse_cl_date, help='Beginning date to download in yyyy-mm format.')
    parser.add_argument('end', type=parse_cl_date, help='Ending date to download in yyyy-mm format.')
    parser.add_argument('-o', '--out-dir', default='.', help='Directory to save downloads to. Default is the current directory.')
    parser.add_argument('-e', '--extract-tar', action='store_true', help='Extract the tar files after downloading')
    parser.add_argument('-d', '--delete-tar', action='store_true', help='Delete tar file after extracting. Has no effect without --extract-tar.')
    parser.add_argument('-v', '--verbose', action='count', help='Increase logging to console.')
    parser.set_defaults(driver_fxn=driver)

    if not called_as_subcommand:
        return parser.parse_args()


def main(subparser=None):
    args = parse_args(subparser)
    driver(**vars(args))


if __name__ == '__main__':
    main()