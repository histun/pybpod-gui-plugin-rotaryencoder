import time
import sys

sys.path.insert(0, '..')
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule


m = RotaryEncoderModule('COM3')
"""
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
"""
print('--------')

m.enable_logging()

time.sleep(4)

m.disable_logging()

time.sleep(2)

data = m.get_logged_data()

while len(data)>0:
    for r in data:
        print("{0}\t{1}".format(*r))
    data = m.get_logged_data()

m.close()