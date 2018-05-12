# BEHRDownloader
## Tools to download Berkeley High Resolution (BEHR) OMI NO2 Data

### Data availability

The BEHR product is divided into 4 subproducts. The data is available at the 
native resolution of the OMI pixels and on a 0.05 x 0.05 degree grid; both
of the product are further split into ones using the daily NO2 profiles
recommended in Laughner et al. (ACP, p. 15247, 2016) and one retaining the
standard monthly mean profiles.

BEHR data is available from two sources:

  1. Monthly .tar.gz files are archived in the University of California DASH
     repository (http://dash.ucop.edu/) with the following DOIs:

        * Gridded retrieval using daily NO2 profiles: https://doi.org/10.6078/D12D5X
        * Native OMI pixel retrieval using daily NO2 profiles:
        * Gridded retrieval using 2012 monthly mean NO2 profiles:
        * Native OMI pixel retrieval using 2012 monthly mean NO2 profiles:

     This is the preferred repository to download from as it can be cited as is guaranteed
     to be archived.

  2. Individual files may still be downloaded from http://behr.cchem.berkeley.edu/.


### Installation and use

This package currently only relies on standard Python modules, and so should be easy to use.

The easiest method is to run it directly, without installation using the Terminal on Mac/Linux 
or Cygwin (with Python) on Windows, by executing in this directory the command

```
./getbehr.sh 
```

You can also install it so that the program is available from any directory using the standard
Python package install mechanism, that is, running in this directory the command:

```
python setup.py install --user
```

(The `--user` flag is optional but recommended to avoid installing in your system Python directory.)
This will copy the Python script "getbehr.py" to your user Python binary directory:

    * Windows:
    * Macs: ~/Library/Python/<version>/bin
    * Linux: 

You may need to add this directory to your PATH variable. Assuming that the Python version is 3.6, 
you would add the following line to the listed file:

    * Mac: add `export PATH="$PATH:~/Library/Python/3.6/bin"` to your ~/.bash_profile file.
    * Linux: add `export PATH="$PATH:~/" to your ? file

You make then execute `getbehr.py` from any directory.


### Downloading data

All examples will use the simple method of executing `./getbehr.sh` from this directory.
If you have installed the package into your user binary directory, you can substitute
`getbehr.py` for `./getbehr.sh` in any of these examples.

Currently, the only implemented download method is from Dash by command line. This requires
you specify the product, first month, and last month, e.g.:

```
./getbehr.sh dash daily-gridded 2005-01 2005-12
```

would download the gridded product using daily profiles for 2005 to the current directory. This
command has additional options to specify an alternate output directory, and whether to automatically
extract the .tar files and delete the .tar files once that is complete. Run `./getbehr.sh dash --help`
for a full list of options.
