import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, gridspec
import seaborn as sns
from packages.utils import deltaPerc, countTotal, format_num
from packages.base import complete

def diff(data:list[complete]):
    # Calculate difference between datas
    total = countTotal(data)
    corr = np.zeros([total, total])
    tick = []
    
    # Compare every single data one to another, then store it inside a matrix
    for i in range(total):
        for j in range(total):
            corr[i,j] = deltaPerc(data[i].dmgAvg, data[j].dmgAvg)/100
        tick.append(data[i].label)
            
    # Display the matrix using a heatmap
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
    # Plotting the data obtained from calculations
    
    # Total of data
    total = countTotal(data)
    
    # Map to store the stats for each datas
    stats = ({
        'label':[],
        'Atk': [],
        'Hp': [],
        'Def': [],
        'EM': [],
        'ER (%)': [],
        'Dmg Bonus (%)': [],
        'Crit Rate (%)': [],
        'Crit Damage (%)': [],
        'Def Multiplier': [],
        'Res Multiplier': [],
        'Custom Multiplier': [],
        'Max Error (%)':[]
    })
    
    # Inputting the stats data, then convert to DataFrame
    for i in range(total):
        stats['label'].append(data[i].label)
        stats['Atk'].append(data[i].atk_)
        stats['Hp'].append(data[i].hp_)
        stats['Def'].append(data[i].def_)
        stats['EM'].append(data[i].elementalMastery)
        stats['ER (%)'].append(data[i].energyRecharge)
        stats['Dmg Bonus (%)'].append(data[i].dmgBonus)
        stats['Crit Rate (%)'].append(data[i].critRate)
        stats['Crit Damage (%)'].append(data[i].critDmg)
        stats['Def Multiplier'].append(data[i].defMultiplier)
        stats['Res Multiplier'].append(data[i].resMultiplier)
        stats['Custom Multiplier'].append(data[i].customMultiplier)
        stats['Max Error (%)'].append(deltaPerc(data[i].dmgAvg, data[i].dmgAvg_err))
        
    stats = pd.DataFrame(stats)
    
    # Map to store the damage value
    df = {
        'label': [], # Name
        'percentage': [], # Percentage increase from default
        'type': [] # Damage type
    }
    
    # Inputting the damage data, then convert to data frame
    for i in range (total):
            
        df['percentage'].extend([
            deltaPerc(data[origin-1].dmgCrit, data[i].dmgCrit)+100,
            deltaPerc(data[origin-1].dmgNoCrit, data[i].dmgNoCrit)+100,
            deltaPerc(data[origin-1].dmgAvg, data[i].dmgAvg)+100
        ])
        df['type'].extend(["Crit", "Non-Crit", "Average"])
        df['label'].extend([data[i].label]*3)
    
    df = pd.DataFrame(df)
    
    # Map to store the average dmg
    Avg = {
        'label':[],
        'dmg':[]
    }
    
    # Inputting the average dmg data, then convert to data frame
    for i in range(total):
        Avg['label'].append(data[i].label)
        Avg['dmg'].append(data[i].dmgAvg)
    
    Avg = pd.DataFrame(Avg)
    
# Visualization
    
    # Using gridSpec with figsize of 16,9 to generate a cluster of compacted plots
    fig = plt.figure(figsize=(16,9))
    gs = gridspec(7,4, width_ratios=[1,1,.05,2])
    gs.update(wspace=0.1, hspace=1)
    
    # Zeroing and initialization
    cols = stats.columns
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
        sns.barplot(stats, x = cols[i], hue=cols[0], ax = ax[i], legend=False)
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
    
    # Subplot for performance compared to other data (the damage value)
    ax0 = fig.add_subplot(gs[:6,3])
    sns.barplot(df, x="type", y="percentage", hue="label", ax=ax0, legend=True)
    ax0.set_ylabel("")
    ax0.set_xlabel("")
    ax0.tick_params(axis='both', labelsize="medium")
    ax0.set_title(f"Performance compared to {data[origin-1].label}", pad=5, loc = 'center', fontsize='x-large')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter())
    
    # Adding and handling legends for better viewing
    handles, labels = ax0.get_legend_handles_labels()
    ax0.get_legend().remove()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,1), ncol=len(labels), fontsize='x-large')
    
    # Subplot for average dmg
    ax1 = fig.add_subplot(gs[6,:])
    sns.barplot(Avg, x='dmg', hue='label', legend=False, ax=ax1)
    ax1.set_title("Avg Dmg Output", pad=5)
    ax1.set_yticklabels([])
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_num))
    ax1.set_yticks([])
    ax1.set_xlabel('')
        
    # Plot
    plt.show()