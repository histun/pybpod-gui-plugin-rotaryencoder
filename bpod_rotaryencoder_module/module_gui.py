import pyforms, sip
from pyforms import BaseWidget
from pyforms.Controls import ControlText, ControlCheckBox, ControlNumber, ControlButton
from pyforms.Controls import ControlMatplotlib
from bpod_rotaryencoder_module.module import RotaryEncoderModule

from pysettings import conf
if conf.PYFORMS_USE_QT5:
	from PyQt5.QtCore import QTimer, QEventLoop
else:
	from PyQt4.QtCore import QTimer, QEventLoop

class RotaryEncoderModuleGUI(RotaryEncoderModule, BaseWidget):

	TITLE = 'Rotary encoder module'

	def __init__(self):
		BaseWidget.__init__(self, self.TITLE)
		RotaryEncoderModule.__init__(self)

		self._port 			= ControlText('Serial port', '/dev/ttyACM1')
		self._connect_btn   = ControlButton('Connect', checkable=True)

		self._events 		= ControlCheckBox('Enable events')
		self._stream 		= ControlCheckBox('Stream data')
		self._zero_btn 		= ControlButton('Reset position')
		self._reset_threshs = ControlButton('Reset thresholds')
		self._thresh_lower 	= ControlNumber('Lower threshold (deg)', 0, -360, 360)
		self._thresh_upper 	= ControlNumber('Upper threshold (deg)', 0, -360, 360)
		self._graph 		= ControlMatplotlib('Value')
		self._clear_btn 	= ControlButton('Clear')

		self.set_margin(10)

		self.formset = [
			('_port','_connect_btn'),
			('_events', '_stream','_zero_btn',),
			('_thresh_lower', '_thresh_upper', '_reset_threshs'),			
			'=',
			'_graph',
			'_clear_btn'
		]

		self._stream.enabled = False
		self._events.enabled = False
		self._zero_btn.enabled = False
		self._reset_threshs.enabled = False
		self._thresh_lower.enabled = False
		self._thresh_upper.enabled = False

		self._connect_btn.value = self.__toggle_connection_evt
		self._stream.changed_event = self.__stream_changed_evt
		self._events.changed_event = self.__events_changed_evt
		self._thresh_upper.changed_event = self.__thresh_evt
		self._thresh_lower.changed_event = self.__thresh_evt
		self._reset_threshs.value = self.__reset_thresholds_evt
		self._zero_btn.value = self.__zero_btn_evt
		self._graph.on_draw = self.__on_draw_evt
		self._clear_btn.value = self.__clear_btn_evt

		self.history_x = []
		self.history_y = []

		self._timer = QTimer()
		self._timer.timeout.connect(self.__update_graph)

	def __clear_btn_evt(self):
		self.history_x = []
		self.history_y = []
		self._graph.draw()

	def __on_draw_evt(self, figure):
		axes = figure.add_subplot(111)
		axes.clear();
		axes.plot(self.history_x, self.history_y) 

		if len(self.history_x)>=2:
			x_range = [self.history_x[0],self.history_x[-1]]
			axes.plot(x_range,[self._thresh_upper.value, self._thresh_upper.value], linestyle='dotted', color='red')
			axes.plot(x_range,[self._thresh_lower.value, self._thresh_lower.value], linestyle='dotted', color='blue')

		self._graph.repaint()
		#print(self.history_x, self.history_y)

	def __update_graph(self):
		for data in self.read_stream():
			self.history_x.append(data[0])
			self.history_y.append(data[1])

		self._graph.draw()

	def __zero_btn_evt(self): 
		self.set_zero_position()

	def __reset_thresholds_evt(self):
		pass


	def __thresh_evt(self):
		thresholds = [int(self._thresh_lower.value), int(self._thresh_upper.value) ]	
		self.set_thresholds(thresholds)


	def __stream_changed_evt(self):
		if self._stream.value:
			self.enable_stream()
			self._timer.start(100)
		else:
			self.disable_stream()
			self._timer.stop()

	def __events_changed_evt(self):
		if self._stream.value:
			self.enable_evt_transmission()
		else:
			self.disable_evt_transmission()

	def __toggle_connection_evt(self):
		if not self._connect_btn.checked:
			if hasattr(self, 'arcom'):
				self.disable_stream()
				self._timer.stop()
				self.close()
			self._connect_btn.label = 'Connect'
			self._stream.enabled = False
			self._events.enabled = False
			self._zero_btn.enabled = False
			self._reset_threshs.enabled = False
			self._thresh_lower.enabled = False
			self._thresh_upper.enabled = False
		else:
			self.open(self._port.value)
			self._connect_btn.label = 'Connected'
			self._stream.enabled = True
			self._events.enabled = True
			self._zero_btn.enabled = True
			self._reset_threshs.enabled = True
			self._thresh_lower.enabled = True
			self._thresh_upper.enabled = True



if __name__=='__main__':
	pyforms.start_app( RotaryEncoderModuleGUI, geometry=(0,0,600,500) )