*************************************
:mod:`USB`
*************************************

.. module:: pybpodapi
   :synopsis: top-level module

.. autoclass:: pybpod_rotaryencoder_module.module_api.RotaryEncoderModule
    :members:
    :private-members:




Usage example
================


.. code:: python

    from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule

    m = RotaryEncoderModule('/dev/ttyACM1')

    m.start_logging()

    m.enable_stream()

    #print the first 100 outputs
    count = 0
    while count<100:
        data = m.read_stream()
        if len(data)==0:
            continue
        else:
            count += 1
            print(data)

    m.disable_stream()

    m.stop_logging()

    m.set_zero_position()

    m.close()
