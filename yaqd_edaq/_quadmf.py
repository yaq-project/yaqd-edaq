__all__ = ["QuadMF"]

import asyncio
from typing import Dict, Any

from yaqd_core import Sensor, logging

import serial

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
                self.ser.write(f"set c {i} units config[f'c_{i}_units']\n".encode())
            
        self.channels = {"channel 1": (config.get('c_1_units',None), ()),
                         "channel 2": (config.get('c_2_units',None) ()),
                         "channel 3": (config.get('c_3_units',None) ()),
                         "channel 4": (config.get('c_4_units',None) ()),
                         }


    def _load_state(self, state):
        """Load an initial state from a dictionary (typically read from the state.toml file).

        Must be tolerant of missing fields, including entirely empty initial states.

        Parameters
        ----------
        state: dict
            The saved state to load.
        """
        super()._load_state(state)
        # This is an example to show the symetry between load and get
        # If no persistent state is needed, these unctions can be deleted
        self.value = state.get("value", 0)

    def get_state(self):
        state = super().get_state()
        state["value"] = self.value
        return state



    async def _measure(self):
        import numpy
        return {"channel": 0, "curtis": numpy.pi}



    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        # If there is no state to monitor continuously, delete this function
        while True:
            # Perform any updates to internal state
            self._busy = False
            # There must be at least one `await` in this loop
            # This one waits for something to trigger the "busy" state
            # (Setting `self._busy = True)
            # Otherwise, you can simply `await asyncio.sleep(0.01)`
            await self._busy_sig.wait()
