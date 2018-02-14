============
hsaf_cci_042
============


Reading and reshuffling of CCI soil moisture


.. image:: https://travis-ci.org/TUW-GEO/hsaf_cci_042.svg?branch=master
    :target: https://travis-ci.org/TUW-GEO/hsaf_cci_042

Reading and reshuffling of CCI soil moisture Written in Python.

Installation
============

Setup of a complete environment with `conda
<http://conda.pydata.org/miniconda.html>`_ can be performed using the following
commands:

.. code-block:: shell

  conda create -q -n hsaf_cci-environment -c conda-forge numpy netCDF4 pyproj pygrib
  source activate hsaf_cci-environment
  pip install hsaf_env

.. note::

   Reading grib files does not work on Windows as far as we know. It might be
   possible to compile the ECMWF C library but we have not done it yet.

Documentation
=============

.. image:: https://readthedocs.org/projects/hsaf-cci-042/badge/?version=latest
    :target: http://hsaf-cci-042.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Note
====

This project has been set up using PyScaffold 2.5. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
