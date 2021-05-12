# yaqd-edaq

[![PyPI](https://img.shields.io/pypi/v/yaqd-edaq)](https://pypi.org/project/yaqd-edaq)
[![Conda](https://img.shields.io/conda/vn/conda-forge/yaqd-edaq)](https://anaconda.org/conda-forge/yaqd-edaq)
[![yaq](https://img.shields.io/badge/framework-yaq-orange)](https://yaq.fyi/)
[![black](https://img.shields.io/badge/code--style-black-black)](https://black.readthedocs.io/)
[![ver](https://img.shields.io/badge/calver-YYYY.M.MICRO-blue)](https://calver.org/)
[![log](https://img.shields.io/badge/change-log-informational)](https://gitlab.com/yaq/yaqd-edaq/-/blob/master/CHANGELOG.md)

yaq daemons for edaq sensor recording systems

This package contains the following daemon(s):

- https://yaq.fyi/daemons/edaq-isopod

## calibration

Following is an example you might use to apply callibration to the quadmf.

```python
import yaqc

edaq = yaqc.Client(38000)
config = edaq.get_config()


print('Calibrate which channel?')
chno = input()
print(f'Will calibrate {chno}')
edaq.remove_calibration(chno)


calibpoints = config.get('calibpoints', 3)
calibvalues = config.get('calibvalues', [4,7,10])

for i in range (1,calibpoints+1):
    print(f'place probe in pH={calibvalues[i-1]} buffer, then press enter')
    input()
    edaq.add_calibration_point(chno, i, calibvalues[i-1])

print('Calibration Complete')
```
