import json
import os 
import matplotlib.pyplot as plt
import numpy as np


def load_channel_layout(path):
    with open(path) as f:
        channel_layout = json.load(f)
    return channel_layout

def save_channel_layout(channel_layout, path):
    with open(path, 'w') as f:
        json.dump(channel_layout, f)    


# # Plotting
        

def plot_psd(bins, lfp_power, num_samples, xleft = -0.1, xright = 60):
    plt.figure(figsize=(8, 4))
    plt.plot(bins[:num_samples // 2 ], lfp_power[:num_samples // 2])  # Plot only the positive frequencies
    plt.xlim(left=xleft, right = xright)
    plt.xlabel('frequency [Hz]')
    plt.yticks([])
    ax = plt.gca()  # Get the current axes
    ax.spines['top'].set_visible(False)  # Hide the top spine
    ax.spines['right'].set_visible(False)  # Hide the right spine
    ax.spines['left'].set_visible(False)  # Hide the left spine
    ax.spines['bottom'].set_visible(False)  # Hide the bottom spine

def plot_hilbert(signal, amp, freq, fs, left=0, right=20, bottom=0, top=10):
    fig, (ax0, ax1) = plt.subplots(nrows=2)
    t = np.arange(signal.shape[0]) / (fs)
    ax0.plot(t, signal, label='signal')
    ax0.plot(t, amp, label='envelope')
    ax0.set_xlim(left=left, right=right)
    ax0.set_yticks([])

    ax0.legend()
    ax1.plot(t[1:], freq)
    ax1.set_xlabel("[s]")
    ax1.set_ylabel("[Hz]")
    ax1.set_xlim(left=left, right=right)
    ax1.set_ylim(bottom, top)
    fig.tight_layout()
    plt.show()

def plot_waveforms(data, session, samples = None,  other_data = [], other_data_labels = []):

    if samples is None:
        samples = data.samples

    fig = plt.figure()
    plt.ion()

    y_min = samples.min()
    y_max = samples.max()
    s = np.linspace(data.start_sample_number, data.end_sample_number, samples.shape[0])

    for i in range(samples.shape[1]):
        plt.plot(s, samples[:, i] - i*(y_max-y_min), linewidth=0.85, alpha=0.95)

    if other_data is not None:
        for i in range(len(other_data)):
            plt.plot(s, other_data[i] - (i+samples.shape[1])*(y_max-y_min), linewidth=0.85, alpha=0.95)
        
    
    plt.bar(x=[x[0] for x in data.event_windows], height=-(y_max-y_min)*(samples.shape[1] + len(other_data)) - y_max, 
            width=[x[1]-x[0] for x in data.event_windows], align='edge',bottom=2*y_max,
              alpha=0.35, color='r')

    num_xticks = 10
    tick_spacing = len(s) // num_xticks
    selected_ticks = s[::tick_spacing]
    selected_labels = [f"{sn / session.fs:.1f}" for sn in selected_ticks]  
    plt.xticks(ticks=selected_ticks, labels=selected_labels)
    plt.xlabel('[s]')

    ylabels = [session.channel_names[i] for i in data.selected_channels]  
    for lbl in other_data_labels:
        ylabels.append(lbl)
    if len(other_data_labels) < len(other_data):
        for _ in range(len(other_data) - len(other_data_labels)):
            ylabels.append('')

    plt.yticks(ticks=[-i*(y_max-y_min) for i in range(samples.shape[1] + len(other_data))], labels=ylabels)
    plt.show()

