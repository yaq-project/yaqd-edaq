__all__ = ["QuadMF"]

import asyncio
from typing import Dict, Any

from yaqd_core import Sensor, logging

import serial  # type: ignore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QuadMF(Sensor):
    _kind = "quadmf"
    traits = ["uses-serial", "uses-uart"]
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Perform any unique initializationset
        self.ser = serial.Serial(config["serialport"], 115_200)
        self.ser.timeout = 1
        for i in range(1, 5):
            mode = config[f"c_{i}_mode"]
            self.ser.write(f"set c {i} function {mode}\n".encode())
            if mode == "pH&ISE":
                self.ser.write(f"set c {i} units {config[f'c_{i}_units']}\n".encode())
        self.channel_names = [f"channel {n}" for n in range(1, 5)]
        self.channel_units = {f"channel {n}": config.get(f"c_{n}_units", None) for n in range(1, 5)}

    def blink(self):

        self.ser.write(b"blink\n")

    def remove_calibration(self, chno):
        self.ser.write(f"cal c {chno} remove all\n".encode())

    def add_calibration_point(self, chno, pointno, knownval):
        self.ser.write(f"cal c {chno} set {pointno} {knownval}\n".encode())

    def raw_write(self, string):
        self.ser.reset_input_buffer()
        self.ser.write(string.encode())
        while True:
            line = self.ser.readline()
            if line == b"":
                break
            logger.info(line)

    async def _measure(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.write(b"r\n")
        raw = self.ser.readline()
        raw = self.ser.readline()
        raw = raw.split()
        vals = []
        for r in raw:
            try:
                vals.append(float(r))
            except ValueError:
                vals.append(float("nan"))
        return {f"channel {i}": float(vals[i * 2]) for i in range(1, 5)}
