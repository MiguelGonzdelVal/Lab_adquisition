import pandas as pd
import time
import numpy as np
class Device(object):
    def __init__(self, device_ID):
        """Generate a parent class for all devices

        Args:
            device_ID (int): ID of the device so it can be cathegorized
        """        
        self.device_ID=device_ID
        self.current_data=None
    def get_data(self):
        """A function that returns the current data.

        Returns:
            list: list of all the data asked by the user
        """        
        return self.current_data
