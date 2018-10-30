Reading ESA CCI SM images
-------------------------

Reading of the ESA CCI SM raw netcdf files can be done in two ways.

Reading by file name
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from datetime import datetime
    from esa_cci_sm.interface import CCI_SM_025Img
    import numpy.testing as nptest

    # read several parameters
    parameter = ['sm', 'sm_uncertainty']
    # the class is initialized with the exact filename.
    image_path = os.path.join(os.path.dirname(__file__), 'tests', 'esa_cci_sm-test-data',
                              'esa_cci_sm_dailyImages', 'v04.2', 'combined', '2016')
    image_file = 'ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20160607000000-fv04.2.nc'
    img = CCI_SM_025Img(os.path.join(image_path, image_file), parameter=parameter)

    # reading returns an image object which contains a data dictionary
    # with one array per parameter. The returned data is a global 0.25 degree
    # image/array.
    image = img.read()


Reading by date
~~~~~~~~~~~~~~~

All the ESA CCI SM data in a directory structure can be accessed by date.
The filename is automatically built from the given date.

.. code-block:: python

    from esa_cci_sm.interface import CCI_SM_025Ds

    parameter = 'sm'
    img = CCI_SM_025Ds(data_path=os.path.join(os.path.dirname(__file__),
                                                    'tests', 'esa_cci_sm-test-data', 'esa_cci_sm_dailyImages',
                                                    'v04.2', 'combined'),
                              parameter=parameter)

    image = img.read(datetime(2016, 6, 7, 0))


For reading all image between two dates the
:py:meth:`c3s_sm.interface.CCI_SM_025Ds.iter_images` iterator can be
used.
