print('Calibrate which channel?')
chno = input()
print('Will calibrate {chno}')

self.ser.write(b"cal c {chno} remove all\n")

calibpoints = config.get('calibpoints', 3)
calibvalues = config.get('calibvalues', [4,7,10])

for i in range (1,calibpoints+1)
    print('place probe in pH={calibvalues(i)} buffer, then press enter')
    input()
    self.ser.write(b"cal c {chno} set {i} {calibvalues(i)}\n")

print('Calibration Complete')