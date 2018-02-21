from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule

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