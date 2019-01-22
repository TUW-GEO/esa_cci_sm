============
esa_cci_sm
============


.. image:: https://travis-ci.org/TUW-GEO/esa_cci_sm.svg?branch=master
    :target: https://travis-ci.org/TUW-GEO/esa_cci_sm

.. image:: https://coveralls.io/repos/github/TUW-GEO/esa_cci_sm/badge.svg?branch=master
    :target: https://coveralls.io/github/TUW-GEO/esa_cci_sm?branch=master

.. image:: https://badge.fury.io/py/esa-cci-sm.svg
    :target: https://badge.fury.io/py/esa-cci-sm
    
.. image:: https://readthedocs.org/projects/esa_cci_sm/badge/?version=latest
    :target: http://esa_cci_sm.readthedocs.io/en/latest/?badge=latest

Reading and reshuffling of CCI soil moisture Written in Python.

Installation
============

Installing the package can be done via pip:

.. code-block:: shell

    pip install esa_cci_sm

Setup of a complete development environment with `conda
<http://conda.pydata.org/miniconda.html>`_ can be performed using the following
commands:

.. code-block:: shell

  git clone git@github.com:TUW-GEO/esa_cci_sm.git esa_cci_sm
  cd esa_cci_sm
  conda env create -f environment.yml
  source activate esa_cci_sm

Supported Products
==================

At the moment this package supports ESA CCI soil moisture data version
v02.x and v03.x and v04.x in netCDF format (reading and time series creation)
with a spatial sampling of 0.25 degrees.

Contribute
==========

We are happy if you want to contribute. Please raise an issue explaining what
is missing or if you find a bug. We will also gladly accept pull requests
against our master branch for new features or bug fixes.


Guidelines
----------

If you want to contribute please follow these steps:

- Fork the esa_cci_sm repository to your account
- Clone the repository, make sure you use ``git clone --recursive`` to also get
  the test data repository.
- make a new feature branch from the esa_cci_sm master branch
- Add your feature
- Please include tests for your contributions in one of the test directories.
  We use py.test so a simple function called test_my_feature is enough
- submit a pull request to our master branch

Note
====

This project has been set up using PyScaffold 2.5. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
