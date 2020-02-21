__all__ = ["QuadMF"]

import asyncio
from typing import Dict, Any

from yaqd_core import Sensor, logging

import serial  # type: ignore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QuadMF(Sensor):
    _kind = "quadmf"
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Perform any unique initializationset
        self.ser = serial.Serial(config['serialport'], 115200)
        for i in range (1,5):
            mode = config[f'c_{i}_mode']
            self.ser.write(f"set c {i} function {mode}\n".encode())
            if mode == 'pH&ISE':
                self.ser.write(f"set c {i} units {config[f'c_{i}_units']}\n".encode())
            
        self.channels = {"channel 1": (config.get('c_1_units',None), ()),
                         "channel 2": (config.get('c_2_units',None), ()),
                         "channel 3": (config.get('c_3_units',None), ()),
                         "channel 4": (config.get('c_4_units',None), ()),
                         }


    def blink(self):
    
        self.ser.write(b"blink\n")
        
    def remove_calibration(self, chno):
        self.ser.write(f"cal c {chno} remove all\n".encode())
        
    def add_calibration_point(self, chno, pointno, knownval)
        self.ser.write(f"cal c {chno} set {pointno} {knownval}\n".encode())
  
    async def _measure(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.write(b'r\n')
        raw = self.ser.readline()
        raw = self.ser.readline()
        raw = raw.split()
        vals = []
        for r in raw:
            try:
                vals.append(float(r))
            except ValueError:
                vals.append(float("nan"))
        return {f"channel {i}": float(vals[i*2]) for i in range(1,5)}