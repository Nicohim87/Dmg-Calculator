import numpy as np
import pandas as pd
from packages.utils import deltaPerc, countTotal, rangify, confidenceInterval95

class difference:
    def __init__(self, data):
        self.total = countTotal(data)
        self.corr = np.zeros([self.total, self.total])
        self.tick = []
    
        # Compare every single data one to another, then store it inside a matrix
        for i in range(self.total):
            for j in range(self.total):
                self.corr[i,j] = deltaPerc(data[i].dmgAvg, data[j].dmgAvg)/100
            self.tick.append(data[i].label)
        


class pltdatamanip:
    def __init__(self, data):
        self.data = data
        self.total = countTotal(data)
        
        self.stats = ({
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
            'Expected Max Error (%)':[]
        })
    
        self.diff = {
            'label': [], # Name
            'output': [], # Output dmg
            'type': [] # Damage type
        }
    
        self.Avg = {
            'label':[],
            'dmg':[]
        }
        
        for i in range(self.total):
            self.stats['label'].append(data[i].label)
            self.stats['Atk'].append(data[i].atk_)
            self.stats['Hp'].append(data[i].hp_)
            self.stats['Def'].append(data[i].def_)
            self.stats['EM'].append(data[i].elementalMastery)
            self.stats['ER (%)'].append(data[i].energyRecharge)
            self.stats['Dmg Bonus (%)'].append(data[i].dmgBonus)
            self.stats['Crit Rate (%)'].append(data[i].critRate)
            self.stats['Crit Damage (%)'].append(data[i].critDmg)
            self.stats['Def Multiplier'].append(data[i].defMultiplier)
            self.stats['Res Multiplier'].append(data[i].resMultiplier)
            self.stats['Custom Multiplier'].append(data[i].customMultiplier)
            self.stats['Expected Max Error (%)'].append(deltaPerc(data[i].dmgAvg, data[i].dmgAvg_err))
        
        for i in range (self.total):
            lb, ub = confidenceInterval95(data[i].dmgNoCrit, data[i].dmgCrit, data[i].critRate)
            self.diff['output'].extend([
                data[i].dmgCrit,
                ub,
                data[i].dmgAvg,
                lb,
                data[i].dmgNoCrit
            ])
            self.diff['type'].extend(["Crit", "95% CI Upper Bound", "Average", "95% CI Lower Bound", "Non-Crit"])
            self.diff['label'].extend([data[i].label]*5)
            
        for i in range(self.total):
            self.Avg['label'].append(data[i].label)
            self.Avg['dmg'].append(data[i].dmgAvg)
            
        self.stats = pd.DataFrame(self.stats)
        self.diff = pd.DataFrame(self.diff)