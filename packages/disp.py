import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker, gridspec
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from packages.base import complete
import packages.datamanip as dm
from packages.utils import format_num

def diff(data:list[complete]):
    difference = dm.difference(data)
            
    # Display the matrix using a heatmap
    plt.figure(figsize=(6,4))

    ax = sns.heatmap(difference.corr, annot=True, xticklabels=difference.tick, yticklabels=difference.tick, square=True, fmt=".2%")
    ax.set_xlabel("To", fontsize = "large")
    ax.set_ylabel("From", fontsize = "large")
    ax.set_title("Percentage of Average Damage Increase", fontsize='large')
    ax.tick_params(axis='both', labelsize="medium")
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize='medium')
        
    plt.show()
    
    
def plot(data:list[complete]):
    transformed = dm.pltdatamanip(data)
    
    # Using gridSpec with figsize of 16,9 to generate a cluster of compacted plots
    fig = plt.figure(figsize=(16,9))
    gs = gridspec.GridSpec(7,4, width_ratios=[1,1,.05,2])
    gs.update(wspace=0.1, hspace=1)
    
    # Zeroing and initialization
    cols = transformed.stats.columns
    col = 0
    row = 0
    ax = [None]*(len(cols))
    
    # Plotting for each type of stats
    for i in range(1, len(cols)):
        # Figuring out the plot location
        ax[i] = fig.add_subplot(gs[row,col])
        
        # Incrementing the plot location
        if(i % 6 == 0 and i != 0):
            row = 0
            col += 1
        else:
            row += 1
            
        # Plotting
        sns.barplot(transformed.stats, x = cols[i], hue=cols[0], ax = ax[i], legend=False)
        if(cols[i] == "Crit Rate (%)"):
            # Crit rate has a minimum value of 0 and maximum value of 100
            # Below 0% and above 100%, crit rate does not have any meanings
            ax[i].set_xlim(0,100)
        elif(cols[i] == "Def Multiplier"):
            # Because def multiplier always has a minimum value of 0 and maximum value of 1
            # Negative or higher than 1 def multiplier implies that there is level 0 and negative level, which contradicts with the definiton of level
            ax[i].set_xlim(0,1)    
        ax[i].set_title(cols[i], pad=5)
        ax[i].set_yticklabels([])
        ax[i].set_yticks([])
        ax[i].set_xlabel('')
    
    # Subplot for Damage Output Range
    palette = {
        "Non-Crit":'white', 
        "95% CI Lower Bound":'#FFFFB0', 
        "Average":'#FFFF00', 
        "95% CI Upper Bound":'#80FF00', 
        "Crit":'#D0FFB0'
    }
    
    ax0 = fig.add_subplot(gs[:6,3])
    sns.barplot(transformed.diff, x="label", y="output", hue="type", ax=ax0, legend=True, dodge=False, palette=palette)
    ax0.set_ylabel("")
    ax0.set_xlabel("")
    ax0.tick_params(axis='both', labelsize="medium")
    ax0.set_title(f"Average Damage Output Range for 100 Tries", pad=5, loc = 'center', fontsize='x-large')
    handles, labels = ax0.get_legend_handles_labels()  # Get existing legend
    custom_labels = [
        'Upper Outlier', 
        '95% CI Upper Range', 
        '95% CI Lower Range', 
        'Bottom Outlier', 
        ''
    ]
    ax0.legend(handles, custom_labels, title='', loc='lower right')
    
    
    # Subplot for average dmg
    ax1 = fig.add_subplot(gs[6,:])
    sns.barplot(transformed.Avg, x='dmg', hue='label', legend=True, ax=ax1)
    ax1.set_title("Avg Dmg Output", pad=5)
    ax1.set_yticklabels([])
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_num))
    ax1.set_yticks([])
    ax1.set_xlabel('')
    
    # Adding and handling legends for better viewing
    handles, labels = ax1.get_legend_handles_labels()
    ax1.get_legend().remove()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,1), ncol=len(labels), fontsize='x-large')
        
    # Plot
    plt.show()