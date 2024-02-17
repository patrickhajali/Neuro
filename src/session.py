
import json
import os
import numpy as np
import open_ephys.analysis

class LFPData:

    def __init__(self, samples, event_windows, start_sample_number, end_sample_number, selected_channels):
        
        self._samples = samples
        self.event_windows = event_windows
        self.start_sample_number = start_sample_number
        self.end_sample_number = end_sample_number
        self.selected_channels = selected_channels


    def set_channels(self, channels):
        self.selected_channels = channels

    @property
    def samples(self):
        return self._samples[:,self.selected_channels]

    
class LFPSession:

    def __init__(self, dir, start_idx=None, end_idx=None, channel_layout_dir=None):
        
        self.dir = dir

        # Load the session
        session = open_ephys.analysis.Session(dir)
        recording = session.recordnodes[0].recordings[0]
        self.continuous = recording.continuous[0] # In this case, there is only one continuous recording 
        self.sample_numbers = self.continuous.sample_numbers
        self.metadata = self.continuous.metadata
        self.events = recording.events # stored as a Pandas dataframe

        # Load params from metadata
        self.num_channels = self.metadata['num_channels']
        self.channel_names = self.metadata['channel_names']
        self.fs = self.metadata['sample_rate']

        # Create a channel map
        self.channel_layout = {}
        self.left_channels = []
        self.right_channels = []
        if channel_layout_dir is not None:
            self.channel_layout = self._load_channel_layout(channel_layout_dir)
            self.left_channels = np.array(self.channel_layout['left'])
            self.right_channels = np.array(self.channel_layout['right'])

    def _load_channel_layout(self, path):
        with open(path) as f:
            channel_layout = json.load(f)
        return channel_layout


    def load_data(self, start_sample_idx=0, end_sample_idx=None, channels = 'all'):
        

        if end_sample_idx is None:
            end_sample_idx = len(self.sample_numbers)-1

        if start_sample_idx < 0 or end_sample_idx > len(self.sample_numbers):
            raise ValueError('start_sample_idx and end_sample_idx must be within the range of the sample numbers')
        

        start_sample_number = self.sample_numbers[start_sample_idx]
        end_sample_number = self.sample_numbers[end_sample_idx]

        samples = self.continuous.get_samples(start_sample_index = start_sample_idx, end_sample_index = end_sample_idx)
        
        event_windows = self._load_events(start_sample_number, end_sample_number)
        selected_channels = np.concatenate([self.left_channels, self.right_channels])
        
        return LFPData(samples[:,selected_channels], event_windows, start_sample_number, end_sample_number, selected_channels)

    def get_channels(self, side='left', min_depth=0, max_depth=15):
    
        if side == 'left':
            return self.left_channels[min_depth:max_depth+1]
        elif side == 'right':
            return self.right_channels[min_depth:max_depth+1]
        else:
            raise ValueError('side must be either "left" or "right"')

    def _load_events(self, start_sample_number=None, end_sample_number=None):

        if start_sample_number is None or end_sample_number is None:
            raise ValueError('start_sample_number and end_sample_number must be defined before loading events')
        
        event_windows = []
        for i in range(0,len(self.events), 2): # first event is always a rise (assuming alternating state is guaranteed)
            if self.events.iloc[i]['state'] == 1: # should always be true 
                start = self.events.iloc[i]['sample_number']
                if start < start_sample_number: 
                    continue
                end = self.events.iloc[i+1]['sample_number']
                if end > end_sample_number: 
                    break 
                event_windows.append((start, end))
        
        return event_windows
        
