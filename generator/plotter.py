import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

color_palette = [
    'royalblue',
    'orange',
    'mediumseagreen',
    'mediumorchid',
    'orangered',
    "slategray",
    "lightpink",
    "lightsalmon",
    "olive",
    "aqua"
]

# The input data_frame must have column 'relative' and 'url', where relative in the request's integer second from the start
def plot_frequency(ax, data_frame: pd.DataFrame, plot_url: str, mission_seconds: int, color: str, rolling_window_seconds: int = 240, xclip: Tuple[int, int]=(-1,-1)):
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
    
    if xclip != (-1,-1):
        plot_pdf = plot_pdf.iloc[xclip[0]:xclip[1]]
    
    return plot_pdf

def plot_frequencies(data_frame: pd.DataFrame, plot_urls: List[str], mission_seconds: int, rolling_window_seconds: int = 240, xlim: Tuple[int] = (-1,-1), ylim: Tuple[int] = (0, 10), xclip: Tuple[int, int]=(-1,-1), color_palette: List[str] = color_palette):
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(18, 8)
    fig.set_dpi(600)
    
    index = 0
    freq_pdfs = []
    for plot_url in plot_urls:
        freq = plot_frequency(
            ax, 
            data_frame, 
            plot_url, 
            mission_seconds, 
            color_palette[index % len(color_palette)],
            rolling_window_seconds,
            xclip
        )
        
        freq_pdfs.append(freq)
        
        index += 1
    
    
    plt.xlabel("Mission Time (sec)")
    plt.ylabel("Frequency")
    plt.ylim(ylim)
    plt.xlim((0, mission_seconds) if xlim [0] == -1 else xlim)
    plt.title("Frequency of Access")
    
    return freq_pdfs