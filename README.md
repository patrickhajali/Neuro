
I came across LFP recordings and explored what it's like working with neuro data.

More about what I did [here](https://www.patrickhajali.com/neuro). 

#### What I added ontop of [Open-Ephys](https://github.com/open-ephys/open-ephys-python-tools)

An ```LFPSession``` is designed to be created once to load the desired Open-Ephys session.

To extract samples, use the ```load_data``` method which returns an ```LFPRecording```. Each instance of an ```LFPRecording``` stores the selected samples, sample range, channel range, and corresponding Events. This ensures that the samples, selected channels, indices, and related Events are always grouped. 
