Conversion to time series format
================================

For a lot of applications it is favorable to convert the image based format into
a format which is optimized for fast time series retrieval. This is what we
often need for e.g. validation studies. This can be done by stacking the images
into a netCDF file and choosing the correct chunk sizes or a lot of other
methods. We have chosen to do it in the following way:

- Store only the reduced gaußian grid points since that saves space.
- Further reduction the amount of stored data by saving only land points if selected.
- Store the time series in netCDF4 in the Climate and Forecast convention
  `Orthogonal multidimensional array representation
  <http://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html#_orthogonal_multidimensional_array_representation>`_
- Store the time series in 5x5 degree cells. This means there will be 2566 cell
  files (1001 with reduction to land points) and a file called ``grid.nc``
  which contains the information about which grid point is stored in which file.
  This allows us to read a whole 5x5 degree area into memory and iterate over the time series quickly.

  .. image:: 5x5_cell_partitioning_cci.png
     :target: 5x5_cell_partitioning_cci.png

This conversion can be performed using the ``ccism_reshuffle`` command line
program. An example would be:

.. code-block:: shell

   ccism_reshuffle /cci_images /timeseries/data 2000-01-01 2001-01-02 --parameters sm sm_uncertainty --land_points True

Which would take ESA CCI SM data stored in ``/cci_images`` over land from January 1st
2000 to January 2nd 2001 and store the parameters for soil moisture and its uncertainty as time
series in the folder ``/timeseries/data``.

**Note**: If a ``RuntimeError: NetCDF: Bad chunk sizes.`` appears during reshuffling, consider downgrading the
netcdf4 C-library via:

.. code-block:: shell

  conda install -c conda-forge libnetcdf==4.3.3.1 --yes

Conversion to time series is performed by the `repurpose package
<https://github.com/TUW-GEO/repurpose>`_ in the background. For custom settings
or other options see the `repurpose documentation
<http://repurpose.readthedocs.io/en/latest/>`_ and the code in
``esa_cci_sm.reshuffle``.

Reading converted time series data
----------------------------------

For reading the data the ``ccism_reshuffle`` command produces the class
``CCITs`` can be used:

.. code-block:: python

    from esa_cci_sm.interface import CCITs
    ds = CCITs(ts_path)
    # read_ts takes either lon, lat coordinates or a grid point indices.
    # and returns a pandas.DataFrame with all reshuffled variables.
	# e.g. timeseries for lon=45°, lat=15°:
    ts = ds.read_ts(45, 15)
