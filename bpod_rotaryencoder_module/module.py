from pybpodapi.bpod.com.arcom import ArCOM, ArduinoTypes

class RotaryEncoderModule(object):

	COM_HANDSHAKE 		 = 'C'
	COM_TOGGLEEVTTRANSM  = 'V'
	COM_TOGGLESTREAM 	 = 'S'
	COM_STARTLOGGING 	 = 'L'
	COM_STOPLOGGING 	 = 'F'
	COM_GETLOGDATA 		 = 'R'
	COM_GETCURRENTPOS  	 = 'Q'
	COM_SETZEROPOS 		 = 'Z'
	COM_SETPOS 			 = 'P'
	COM_ENABLETHRESHOLDS = ';'
	COM_SETPREFIX	 	 = 'I'
	COM_SETTHRESHOLDS 	 = 'T'
	COM_SETWRAPPOINT 	 = 'W'


	def __init__(self, serialport=None):
		if serialport: self.open(serialport)

	def open(self, serialport):
		self.arcom = ArCOM().open(serialport, 115200)
		self.arcom.write_char(self.COM_HANDSHAKE)
		if self.arcom.read_uint8() != 217:
			raise Exception('Could not connect =( ')


	def close(self): self.arcom.close()

	def __pos_2_degrees(self, pos): 	return round(((float(pos)/512.0)*180.0)*10.0)/10.0;
	def __degrees_2_pos(self, degrees): return int(round( (float(degrees)/180.0)*512.0, 0) );


	def enable_evt_transmission(self):
		self.arcom.write_array([ord(self.COM_TOGGLEEVTTRANSM), 1])
		return self.arcom.read_uint8()==1


	def disable_evt_transmission(self):
		self.arcom.write_array([ord(self.COM_TOGGLEEVTTRANSM), 0])
		return self.arcom.read_uint8()==1


	def enable_stream(self):  self.arcom.write_array([ord(self.COM_TOGGLESTREAM), 1])
	def disable_stream(self): self.arcom.write_array([ord(self.COM_TOGGLESTREAM), 0])

	def read_stream(self):
		data = []
		available = self.arcom.bytes_available()

		if available>5:
			msg = self.arcom.read_bytes_array(available)
			
			for i in range(0, len(msg), 6):
				data_in_bytes = b''.join(msg)

				position = int.from_bytes( data_in_bytes[i:i+2],   byteorder='little', signed=True)
				evt_time = float(int.from_bytes( data_in_bytes[i+2:i+6], byteorder='little', signed=False))/1000.0
				
				position_degrees = self.__pos_2_degrees(position)
				
				data.append((evt_time, position_degrees))
			
		return data


	def enable_logging(self): 	self.arcom.write_array([ord(self.COM_STARTLOGGING)])
	def disable_logging(self): 	self.arcom.write_array([ord(self.COM_STOPLOGGING)])

	def get_logged_data(self):
		self.arcom.write_array([ord(self.COM_GETLOGDATA)])
		msg    = self.arcom.read_bytes_array(4)
		n_logs = int.from_bytes( b''.join(msg), byteorder='little', signed=False)
		data = []
		for i in range(0, n_logs, 6):
			msg = self.arcom.read_bytes_array(6)
			data_in_bytes = b''.join(msg)
			position = int.from_bytes( data_in_bytes[i:i+2],   byteorder='little', signed=True)
			evt_time = float(int.from_bytes( data_in_bytes[i+2:i+6], byteorder='little', signed=False))/1000.0
			position_degrees = self.__pos_2_degrees(position)				
			data.append((evt_time, position_degrees))
			
		return data



	def current_position(self):
		self.arcom.write_array([ord(self.COM_GETCURRENTPOS)])
		data_in_bytes = b''.join(self.arcom.read_bytes_array(2))
		ticks = int.from_bytes( data_in_bytes, byteorder='little', signed=True)
		return self.__pos_2_degrees(ticks)
		
	def set_zero_position(self):
		self.arcom.write_array([ord(self.COM_SETZEROPOS)])

	def set_prefix(self, prefix):
		self.arcom.write_array([ord(self.COM_SETPREFIX), prefix])
		return self.arcom.read_uint8()==1

	def set_thresholds(self, thresholds):
		data  = ArduinoTypes.get_uint8_array([ord(self.COM_SETTHRESHOLDS), len(thresholds) ])
		data += ArduinoTypes.get_uint16_array([ self.__degrees_2_pos(thresh) for thresh in thresholds])
		self.arcom.write_array(data )
		return self.arcom.read_uint8()==1
		
	def set_position(self, degrees):
		ticks = self.__degrees_2_pos(degrees)
		data  = ArduinoTypes.get_uint8_array([ord(self.COM_SETPOS)])
		data += ticks.to_bytes(2, byteorder='little', signed=True)
		
		self.arcom.write_array(data)
		return self.arcom.read_uint8()==1

	def set_wrappoint(self, wrap_point):
		ticks = self.__degrees_2_pos(wrap_point)
		self.arcom.write_array([ord(self.COM_SETWRAPPOINT)]+ ArduinoTypes.get_uint16_array([ticks]) )
		return self.arcom.read_uint8()==1

	def enable_thresholds(self, thresholds):
		if len(thresholds)!=8: raise Exception('Thresholds array has to be of length 8')
		string = ''.join(map(lambda x: str(int(x)), thresholds))
		bits = int(string, 2)
		self.arcom.write_array([ord(self.COM_ENABLETHRESHOLDS), bits])




if __name__=='__main__':
	import time

	m = RotaryEncoderModule('/dev/ttyACM1')

	#m.start_logging()
	
	#m.stop_logging()

	m.enable_stream()
	
	
	
	count = 0
	while count<100 or True:
		data = m.read_stream()
		if len(data)==0: continue

		print(data)
		count += 1

	m.disable_stream()
	
	print('set', m.set_position(179))
	m.set_zero_position()

	m.enable_thresholds([True, False, True, True, False, False, True, True])
	print(m.current_position())
	print(m.get_logged_data())

	m.close()