import yaqc

edaq = yaqc.Client(38000)
config = eqaq.get_config()




print('Calibrate which channel?')
chno = input()
print(f'Will calibrate {chno}')
edaq.remove_calibration(chno)




calibpoints = config.get('calibpoints', 3)
calibvalues = config.get('calibvalues', [4,7,10])

for i in range (1,calibpoints+1)
    print(f'place probe in pH={calibvalues[i]} buffer, then press enter')
    input()
    edaq.add_calibration_point(chno, i, calibvalues[i])

print('Calibration Complete')