import asyncio
import serial  # type: ignore
from typing import Dict, Any, List

from yaqd_core import UsesUart, UsesSerial, HasMeasureTrigger, IsSensor, IsDaemon


class EdaqIsoPod(UsesUart, UsesSerial, HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "edaq-quadmf"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._ser = serial.Serial(
            self._config["serial_port"], baudrate=self._config["baud_rate"], timeout=1
        )
        for channel_name, channel_config in self._config["channels"].items():
            index = channel_config["index"]
            mode = channel_config["mode"]
            units = channel_config["units"]
            self._ser.write(f"set c {index} function {mode}\n".encode())
            if mode == "pH&ISE":
                self._ser.write(f"set c {i} units {units}\n".encode())
        self._channel_names = list(self._config["channels"].keys())
        self.channel_units = {
            name: self._config["channels"][name]["units"] for name in self._channel_names
        }

    def add_calibration_point(self, chno, pointno, knownval):
        self._ser.write(f"cal c {chno} set {pointno} {knownval}\n".encode())

    def blink(self) -> None:
        self._ser.write(b"blink\n")

    def direct_serial_write(self, message: bytes):
        self._ser.write(message)

    def remove_calibration(self, chno):
        self._ser.write(f"cal c {chno} remove all\n".encode())

    async def _measure(self) -> Dict[str, float]:
        self._ser.reset_input_buffer()
        self._ser.reset_output_buffer()
        self._ser.write(b"r\n")
        raw = self._ser.readline()
        raw = self._ser.readline()
        raw = raw.split()
        vals = []
        for r in raw:
            try:
                vals.append(float(r))
            except ValueError:
                vals.append(float("nan"))
        return {f"channel {i}": float(vals[i * 2]) for i in range(1, 5)}
