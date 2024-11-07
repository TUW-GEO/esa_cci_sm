============
esa_cci_sm
============

|ci| |cov| |pip| |doc|

.. |ci| image:: https://github.com/TUW-GEO/esa_cci_sm/actions/workflows/ci.yml/badge.svg?branch=master
   :target: https://github.com/TUW-GEO/esa_cci_sm/actions

.. |cov| image:: https://coveralls.io/repos/TUW-GEO/esa_cci_sm/badge.png?branch=master
  :target: https://coveralls.io/r/TUW-GEO/esa_cci_sm?branch=master

.. |pip| image:: https://badge.fury.io/py/esa_cci_sm.svg
    :target: http://badge.fury.io/py/esa_cci_sm

.. |doc| image:: https://readthedocs.org/projects/esa_cci_sm/badge/?version=latest
   :target: http://esa_cci_sm.readthedocs.org/


Tools to convert `ESA CCI SM <https://climate.esa.int/en/projects/soil-moisture/>`_ image files into a time series format.

Installation
------------

This python package and all required dependencies can be installed from
`pypi <https://pypi.org/project/esa-cci-sm/>`_
via `pip <https://pip.pypa.io/en/stable/getting-started/>`_

.. code-block:: shell

    pip install esa_cci_sm

On macOS if you get ImportError: Pykdtree failed to import its C extension,
then it might be necessary to install the `pykdtree` package from conda-forge

.. code-block:: shell

    conda install -c conda-forge pykdtree

Data download
-------------

Download ESA CCI SM data files either from the public
`CEDA data store via https <https://catalogue.ceda.ac.uk/uuid/779f116d0477439db1874592add5848c/>`_
or the CEDA FTP server using, e.g. `FileZilla <https://filezilla-project.org/>`_
or `wget <https://www.gnu.org/software/wget/>`_

**Host**: ``anon-ftp.ceda.ac.uk`` no password or user required
**Directory**: ``/neodc/esacci/soil_moisture``)

E.g the following command will download v9.1 COMBINED data for the year 2023

.. code-block:: shell

    wget ftp://anon-ftp.ceda.ac.uk/neodc/esacci/soil_moisture/data/daily_files/COMBINED/v09.1/2023/*.nc

Time series creation
--------------------

After installing this package via pip, you have access to the command line tool to convert ESA CCI SM image files
to CF conform time series. We use an Orthogonal multidimensional array representation
as implemented in the `pynetCF <https://github.com/TUW-GEO/pynetcf>`_ python library.

Note that we assume that the downloaded images are stored in yearly subfolders
like

.. code-block::

    /tmp/img/
    ├── 1978/
    │   ├── ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-19781101000000-fv09.1.nc
    │   ├── ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-19781102000000-fv09.1.nc
    │   ├── ...
    ...
    ├── 2023/
    │   ├── ...
    │   ├── ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20231231000000-fv09.1.nc

The following command would then take the daily images from 1991
to 2023 in the path ``/tmp/img`` and convert data for grid cells over land into times series.
Time series are then stored in ``/tmp/ts``.

.. code-block:: shell

    ccism_reshuffle /tmp/img /tmp/ts 1991-01-01 2023-12-31 --land_points True

Afterwards, in python, the data can be read as pandas DataFrames.

.. code-block:: python

    >> from esa_cci_sm.interface import CCITs
    >> ds = CCITs("/tmp/ts", ioclass_kws={'read_bulk': True})
    >> ds.read(15, 45)  # lon, lat
                      sm  sm_uncertainty  flag  ...  mode  sensor            t0
    1991-01-01  0.424880        0.094507     0  ...     1       2   7670.175000
    1991-01-02       NaN             NaN    24  ...     2       2           NaN
    1991-01-03       NaN             NaN     8  ...     0       2           NaN
    ...              ...             ...   ...  ...   ...     ...           ...
    2023-12-29  0.495448        0.039983     0  ...     3   21536  19720.051575
    2023-12-30  0.426107        0.055060     0  ...     3   16416  19721.147066
    2023-12-31  0.390103        0.030294     0  ...     3   21600  19722.117129


Supported Products
==================

At the moment this package supports ESA CCI soil moisture data versions
3 to 9 in netCDF format (reading and time series creation)
with a spatial sampling of 0.25 degrees.

Contribute
==========

We are happy if you want to contribute. Please raise an issue explaining what
is missing or if you find a bug. We will also gladly accept pull requests
against our master branch for new features or bug fixes.

Setup
-----
Setup of a complete development environment with `conda
<http://conda.pydata.org/miniconda.html>`_ can be performed using the following
commands:

.. code-block:: shell

  git clone git@github.com:TUW-GEO/esa_cci_sm.git --recursive esa_cci_sm
  cd ./esa_cci_sm
  conda create -n esa_cci_sm python=3.12
  conda activate esa_cci_sm
  pip install -e .[testing]

To checkout our testdata files, you need to have
`Git LFS <https://git-lfs.github.com/>`_ installed on your machine.

Guidelines
----------

If you want to contribute please follow these steps:

- Fork the esa_cci_sm repository to your account
- Clone the repository, make sure you use ``git clone ... --recursive`` to also get
  the test data repository.
- make a new feature branch from the esa_cci_sm master branch
- Add your feature
- Please include tests for your contributions in one of the test directories.
  We use pytest so a simple function called test_my_feature is enough
- submit a pull request to our master branch
