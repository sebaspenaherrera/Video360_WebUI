'''
Summary: This module contains the Stats class, which is used to store the samples in memory and manage them.
This class provides methods to append, get, and reset the samples in memory.
Author: Sebastian Penaherrera
Date: 07/10/2023
Status: Under development
'''

import pandas as pd
import numpy as np
from .models import *
from .utils import log_message

class Stats:
    # ATTRIBUTES
    data = []


    # METHODS
    def check_length(self):
        '''
        Check if the number of samples in memory is greater than the limit. If so, discard the oldest samples.
        The limit is defined by the n_samples attribute.

        Returns:
        - None
        '''

        if len(self.data) > self.n_samples:
            self.data = self.data[-self.n_samples:]


    def append_stats(self, data: dict | SampleStats):
        ''' 
        Append a new sample to the list of samples in memory. If the number of samples is greater than the limit, discard the oldest samples.

        Parameters:
        - data: dict | SampleStats. The sample to be appended to the list.

        Returns:
        - None
        '''

        if data is list:
            for sample in data:
                self.data.append(sample)
                self.check_length()
        else:
            self.data.append(data)
            self.check_length()


    def get_item(self, index: int = 0):
        '''
        Return the sample at the specified index. If the index is out of bounds, return None.

        Parameters:
        - index: int. The index of the sample to be returned.

        Returns:
        - The sample at the specified index. If the index is out of bounds, returns None.
        '''
        
        try:
            item = self.data.pop(index)
        except IndexError:
            log_message(message="Sample cannot be fetched. Returning None", level="ERROR")
            item = None

        return item


    def get_items(self, start: int = 0, end: int = 1, cpe: bool = True):
        '''
        Return a list of samples from the start index to the end index. If the list has not enough samples, return None.

        Parameters:
        - start: int. The start index of the samples to be returned.
        - end: int. The end index of the samples to be returned.
        - cpe: bool. If True, return the CPE fields. If False, return None for the CPE fields.

        Returns:
        - A list of samples from the start index to the end index. If the list has not enough samples, return None.
        '''
        
        # If the list has enough samples, take the samples from the list
        if len(self.data) >= (end - start):
            items = self.data[start:end]
            # Delete the items from the list
            self.data = self.data[end::]
            if not cpe:
                # if not CPE is wanted, return None for CPE fields in self.data
                for sample in items:
                    sample['CPE'] = {key: None for key in CPEStats.__annotations__.keys()}
            # Return the samples
            return items
        else:
            # If the list has not enough samples, return None
            log_message(message="Not enough samples in memory", level="ERROR")
            return None


    def reset_stats(self):
        '''
        Clear the list of samples in memory.

        Returns:
        - None
        '''
        
        self.data.clear()


    def get_samples_available(self):
        '''
        Get the current number of available samples in memory.

        Returns:
        - The current number of available samples in memory.
        '''

        return len(self.data)

    def to_string(self):
        '''
        Cast the data attribute to a string.

        Returns:
        - The data attribute casted to a string.
        '''
        
        return str(self.data)


    # STATIC METHODS
    @staticmethod
    def get_keys():
        '''
        Return the names of the fields from the SampleStats model. This method can be used without creating an instance of the Stats class.

        Returns:
        - A list with the names of the fields from the SampleStats model.
        '''
        
        return list(SampleStats.model_fields.keys())


    @staticmethod
    def generate_sample_dataframe(data: dict):
        '''
        Create a one-sample dataframe with the input data.
        
        Parameters: 
        - data: dict. The data to be stored in the dataframe.

        Returns:
        - The dataframe with the input data.
        '''
        
        aux_data = pd.DataFrame.from_dict(data, columns=Stats.get_keys())
        return aux_data.to


    # CONSTRUCTOR
    def __init__(self, n_samples: int = 20):
        self.n_samples = n_samples
        self.data = []
