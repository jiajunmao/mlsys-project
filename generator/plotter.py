import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

color_palette = [
    'royalblue',
    'orange',
    'mediumseagreen',
    'mediumorchid',
    'orangered'
]

# The input data_frame must have column 'relative' and 'url', where relative in the request's integer second from the start
def plot_frequency(ax, data_frame: pd.DataFrame, plot_url: str, mission_seconds: int, color: str, rolling_window_seconds: int = 240):
    # Filter by the URL that we want to plot
    plot_pdf = data_frame[data_frame['url'] == plot_url]
    # Get how many requests to this URL in a relative time window
    plot_pdf = plot_pdf.groupby(['relative']).size()
    plot_pdf = plot_pdf.to_frame().reset_index().rename(columns={0:'count'})
    # Fill in the missing time window
    plot_pdf.index = plot_pdf['relative']
    plot_pdf = plot_pdf.reindex(np.arange(0, mission_seconds)).fillna(0).astype(int).drop(columns=['relative']).reset_index()
    # Calculate the rolling average of the frequency
    plot_pdf['count_rolling'] = plot_pdf.rolling(window=rolling_window_seconds)['count'].mean().fillna(0)


    ax.plot(plot_pdf['relative'], plot_pdf['count'], label="Freq [{}]".format(plot_url), alpha=0.1, color=color)
    ax.plot(plot_pdf['relative'], plot_pdf['count_rolling'], label="Freq (4m rolling) [{}]".format(plot_url), color=color)
    ax.legend(loc='upper right')

def plot_frequencies(data_frame: pd.DataFrame, plot_urls: List[str], mission_seconds: int, rolling_window_seconds: int = 240, color_palette: List[str] = color_palette):
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(18, 8)
    fig.set_dpi(600)
    
    index = 0
    for plot_url in plot_urls:
        plot_frequency(
            ax, 
            data_frame, 
            plot_url, 
            mission_seconds, 
            color_palette[index],
            rolling_window_seconds
        )
        
        index += 1
        
    plt.xlabel("Mission Time (sec)")
    plt.ylabel("Frequency")
    plt.ylim(0, 3)
    plt.xlim(0, mission_seconds)
    plt.title("Frequency of Access")