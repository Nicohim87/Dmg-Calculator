import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns
from packages.stats import stats
from packages.utils import deltaPerc

def diff(data, totalData):
        corr = np.zeros([totalData, totalData])
        tick = []
        for i in range(totalData):
            for j in range(totalData):
                corr[i,j] = deltaPerc(data[i].dmgAvg, data[j].dmgAvg)/100
            tick.append(data[i].label)
            
        plt.figure(figsize=(6,4))
        ax = sns.heatmap(corr, annot=True, xticklabels=tick, yticklabels=tick, square=True, fmt=".2%")
        ax.set_xlabel("To", fontsize = "large")
        ax.set_ylabel("From", fontsize = "large")
        ax.set_title("Percentage of Average Damage Increase", fontsize='large')
        ax.tick_params(axis='both', labelsize="medium")
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize='medium')
        
        plt.show()
    
    
    
def plot(data, totalData, originData):
        df = {
            'label': [],
            'numeric': [],
            'percentage': [],
            'type': []
        }

        for i in range (totalData):
            
            df['percentage'].extend([
                deltaPerc(data[originData-1].dmgCrit, data[i].dmgCrit),
                deltaPerc(data[originData-1].dmgAvg, data[i].dmgAvg),
                deltaPerc(data[originData-1].dmgNoCrit, data[i].dmgNoCrit)
            ])
            df['numeric'].extend([
                data[i].dmgCrit,
                data[i].dmgNoCrit,
                data[i].dmgAvg
            ])
            df['type'].extend(["Crit", "Non-Crit", "Average"])
            df['label'].extend([data[i].label]*3)

        df = pd.DataFrame(df)
        fig, ax = plt.subplots(ncols = 2, nrows = 1, figsize=(20,7))
        
        sns.barplot(df, x="type", y="numeric", hue="label", ax=ax[0])
        ax[0].set_yscale("linear")
        ax[0].set_ylabel("Damage")
        ax[0].set_xlabel("")
        ax[0].legend()
        ax[0].grid(axis='y', which='both')
        ax[0].set_title("Number", pad=20, loc = 'center')
        ax[0].yaxis.set_major_formatter(lambda value, _: f"{int(value):,}")

        sns.barplot(df, x="type", y="percentage", hue="label", ax=ax[1], legend=False)
        ax[1].set_ylabel("% damage increase from origin data")
        ax[1].set_xlabel("")
        ax[1].grid(axis='y', which='both')
        ax[1].set_title(f"Percentage (Origin = Data {originData})", pad=20, loc = 'center')
        ax[1].yaxis.set_major_formatter(ticker.PercentFormatter())

        handles, labels = ax[0].get_legend_handles_labels()
        ax[0].get_legend().remove()
        fig.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout(rect=[0, 0, 1, 1])
        
        plt.show()