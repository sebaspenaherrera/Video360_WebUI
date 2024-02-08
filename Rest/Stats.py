import pandas as pd
import numpy as np
from .models import *


class Stats:
    # ATTRIBUTES
    data = []

    # METHODS
    def check_length(self):
        # If there are more samples than the limit, then take the last n_samples form the list, discarding others
        if len(self.data) > self.n_samples:
            self.data = self.data[-self.n_samples:]

    def append_stats(self, data: dict | SampleStats):
        # Append new item in the list, if there are more items than the limit, discard the oldest ones
        if data is list:
            for sample in data:
                self.data.append(sample)
                self.check_length()
        else:
            self.data.append(data)
            self.check_length()

    def get_item(self, index: int = 0):
        # Try to get the item at the index. If not, return None
        try:
            item = self.data.pop(index)
        except IndexError:
            print("ERROR: CANNOT DELETE THAT SAMPLE FROM THE MEMORY")
            item = None

        return item

    def get_items(self, start: int = 0, end: int = 1, cpe: bool = True):

        # Try to get the items between the bounds start and end. If exception is triggered, return None
        try:
            items = self.data[start:end]
            # Delete the items from the list
            self.data = self.data[end:]
            if not cpe:
                # if not CPE is wanted, return None for CPE fields in self.data
                for sample in items:
                    sample['CPE'] = {key: None for key in CPEStats.__annotations__.keys()}

        except IndexError:
            print("ERROR: CANNOT DELETE THAT SLICE FROM THE MEMORY")
            items = None

        # If the list is empty, return None
        if not self.data:
            return None
        else:
            return items

    def reset_stats(self):
        # Clear the whole list
        self.data.clear()

    def get_samples_available(self):
        # Get the current number of available samples in buffer
        return len(self.data)

    def to_string(self):
        return str(self.data)

    @staticmethod
    def get_keys():
        # Get the names of the fields from the SampleStats model
        return list(SampleStats.model_fields.keys())

    @staticmethod
    def generate_sample_dataframe(data):
        # Create a one-sample dataframe with the input data
        aux_data = pd.DataFrame.from_dict(data, columns=Stats.get_keys())
        return aux_data.to

    def __init__(self, n_samples: int = 20):
        self.n_samples = n_samples
        self.data = []
