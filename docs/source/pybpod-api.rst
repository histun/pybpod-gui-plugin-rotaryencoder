*************************************
:mod:`pybpodapi`
*************************************

.. module:: pybpodapi
   :synopsis: top-level module

.. autoclass:: pybpod_rotaryencoder_module.module.RotaryEncoder
    :members:
    :private-members:
    :show-inheritance:


Usage example
================


.. code:: python

	
	#...

	bpod = Bpod()

	# get the module connected to the first bpod serial port.
	rotary_encoder = bpod.modules[0]

	# call a function of the module
	rotary_encoder.activate_outputstream()

	bpod.stop()
