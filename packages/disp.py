import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, gridspec
import seaborn as sns
from packages.utils import deltaPerc, countTotal
from packages.base import complete

def diff(data:list[complete]):
    total = countTotal(data)
    corr = np.zeros([total, total])
    tick = []
    for i in range(total):
        for j in range(total):
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
    
def plot(data:list[complete], origin):
    total = countTotal(data)
    stats = ({
        'label':[],
        'Atk': [],
        'Hp': [],
        'Def': [],
        'EM': [],
        'ER': [],
        'Dmg Bonus': [],
        'Crit Rate': [],
        'Crit Damage': [],
        'Def Multiplier': [],
        'Res Multiplier': [],
        'Custom Multiplier': []
    })
    
    for i in range(total):
        stats['label'].append(data[i].label)
        stats['Atk'].append(data[i].atk_)
        stats['Hp'].append(data[i].hp_)
        stats['Def'].append(data[i].def_)
        stats['EM'].append(data[i].elementalMastery)
        stats['ER'].append(data[i].energyRecharge)
        stats['Dmg Bonus'].append(data[i].dmgBonus)
        stats['Crit Rate'].append(data[i].critRate)
        stats['Crit Damage'].append(data[i].critDmg)
        stats['Def Multiplier'].append(data[i].defMultiplier)
        stats['Res Multiplier'].append(data[i].resMultiplier)
        stats['Custom Multiplier'].append(data[i].customMultiplier)
        
    stats = pd.DataFrame(stats)
    
    df = {
        'label': [],
        'percentage': [],
        'type': []
    }
    for i in range (total):
            
        df['percentage'].extend([
            deltaPerc(data[origin-1].dmgCrit, data[i].dmgCrit)+100,
            deltaPerc(data[origin-1].dmgNoCrit, data[i].dmgNoCrit)+100,
            deltaPerc(data[origin-1].dmgAvg, data[i].dmgAvg)+100
        ])
        df['type'].extend(["Crit", "Non-Crit", "Average"])
        df['label'].extend([data[i].label]*3)

    df = pd.DataFrame(df)
    
    fig = plt.figure(figsize=(16,7))
    
    gs = gridspec.GridSpec(6,4, width_ratios=[1,1,.05,2])
    gs.update(wspace=0.1, hspace=1)
    
    cols = stats.columns
    col = 0
    row = 0
    ax = [None]*(len(cols))
    
    for i in range(1, len(cols)):
        ax[i] = fig.add_subplot(gs[row,col])
        if(i % 6 == 0 and i != 0):
            row = 0
            col += 1
        else:
            row += 1
        sns.barplot(stats, x = cols[i], hue=cols[0], ax = ax[i], legend=False)
        if(cols[i] == "Crit Rate"):
            ax[i].set_xlim(0,100)
        elif(cols[i] == "Def Multiplier"):
            ax[i].set_xlim(0,1)    
        ax[i].set_title(cols[i], pad=5)
        ax[i].set_yticklabels([])
        ax[i].set_yticks([])
        ax[i].set_xlabel('')
    
    ax0 = fig.add_subplot(gs[:,3])
    sns.barplot(df, x="type", y="percentage", hue="label", ax=ax0, legend=True)
    ax0.set_ylabel("")
    ax0.set_xlabel("")
    ax0.tick_params(axis='both', labelsize="medium")
    ax0.set_title(f"Performance compared to {data[origin-1].label}", pad=5, loc = 'center', fontsize='x-large')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter())
    
    handles, labels = ax0.get_legend_handles_labels()
    ax0.get_legend().remove()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,1), ncol=len(labels), fontsize='x-large')
        
    plt.show()