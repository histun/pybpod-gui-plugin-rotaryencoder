.. module:: pybpodapi
   :synopsis: top-level module

*************************************************
Getting started
*************************************************

Requirements
===================

This library requires the next Python 3 packages to be installed.

- pyserial>=3.1.1
- python-dateutil
- numpy
- sip
- pyqt5
- matplotlib
- https://github.com/UmSenhorQualquer/pysettings.git
- https://UmSenhorQualquer@bitbucket.org/fchampalimaud/logging-bootstrap.git
- https://github.com/UmSenhorQualquer/pyforms.git



Installation
===================

Execute the next command to install the library.

.. code:: bash

	pip3 install git+https://UmSenhorQualquer@bitbucket.org/fchampalimaud/rotary-encoder-module.git --upgrade


.. note::

	In the case you do not have the git software installed in your system, you can use follow the next procedure.


Alternative installation
--------------------------

Download the files in the `link <https://bitbucket.org/fchampalimaud/rotary-encoder-module/branch/master>`_ and uncompress it.  
After enter in the project directory using the terminal and run the next command.


.. code:: bash
	
	pip3 install -r requirements.txt --upgrade
	pip3 install . --upgrade



Use the module in the `pybpod-api <https://bitbucket.org/fchampalimaud/pybpod-api>`_ library
==============================================================================================

This module can be connected and disconnected from the Pybpod-api library. For this go to your user_settings.py file and add the next configuration.

.. code:: python

	PYBPOD_API_MODULES = [
		'bpod_rotaryencoder_module'
	]

.. note::

	The configuration above is configured by default on the pybpod-api library. You only need to do it, if you have overwriten the **PYBPOD_API_MODULES** variable in your user_settings.py.


Examples
========

Use the rotary encoder module with the pybpod-api
----------------------------------------------------

.. code:: python

	
	#...

	bpod = Bpod()

	for m in bpod.modules:
		print( m.name, type(m) )

	rotary_encoder = bpod.modules[0]
	rotary_encoder.set_position_zero()

	bpod.stop()




Access the rotary encoder module directly from the USB port
-------------------------------------------------------------

.. code:: python

	from bpod_rotaryencoder_module.module_api import RotaryEncoderModule

	m = RotaryEncoderModule('/dev/ttyACM1')

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
	
	print('set', m.set_position(179))
	m.set_zero_position()

	m.enable_thresholds([True, False, True, True, False, False, True, True])
	print(m.current_position())
	
	m.close()


Configure the using the GUI
------------------------------

.. code:: python

	import pyforms
	from bpod_rotaryencoder_module.module_gui import RotaryEncoderModuleGUI


	pyforms.start_app( RotaryEncoderModuleGUI, geometry=(0,0,600,500) )


.. image:: /_static/rotary-encoder-module.png
   :scale: 100 %
