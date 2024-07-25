import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker

lv = np.linspace(0, 100, 11)
lv[0] = 1
dm = [17.165605, 34.143343, 80.584775, 136.29291, 207.382042, 323.601597, 492.88489, 765.640231, 1077.443668, 1446.853458, 2030.071808]
ReactionBase = CubicSpline(lv, dm, bc_type='natural')

def overload(a, b, missing:int=-1):
    if(b == missing): return b
    else: return a

class complete:
    label = ""
    def __init__(
        this, 
        level, calculationMode,
        elementalMastery, energyRecharge, 
        atkBase, atkPercent, atkFlat,
        hpBase, hpPercent, hpFlat,
        defBase, defPercent, defFlat,
        motionValue, dmgFlat, 
        dmgBonusElemental, dmgBonusOther,
        critRate, critDmg,
        quickenType, quickenDmgBonus, catalyzeCount,
        amplifyType, amplifyDmgBonus,
        customMultiplier,
        levelEnemy, resistanceBase, resistanceReduction,
        defShred, defIgnore,
        convertToAtk, convertToHp, convertToDef, convertToER, convertToEM, 
        convertToDmgFlat, convertToDmgBonus, convertToCritRate, convertToCritDmg, buffStatus
        ):
        
        this.level = level
        this.calculationMode = calculationMode
        this.elementalMastery = elementalMastery
        this.energyRecharge = energyRecharge
    # Atk
        this.atkBase = atkBase
        this.atkPercent = atkPercent
        this.atkFlat = atkFlat
    # Hp
        this.hpBase = hpBase
        this.hpPercent = hpPercent
        this.hpFlat = hpFlat
    # Def
        this.defBase = defBase
        this.defPercent = defPercent
        this.defFlat = defFlat
    # Dmg
        this.motionValue = motionValue
        this.dmgFlat = dmgFlat
    # Dmg Bonus
        this.dmgBonusElemental = dmgBonusElemental
        this.dmgBonusOther = dmgBonusOther
    # Crit
        this.critRate = critRate
        this.critDmg = critDmg
    # Reaction Multipliers
        this.quickenType = quickenType
        this.quickenDmgBonus = quickenDmgBonus
        this.catalyzeCount = catalyzeCount
        this.amplifyType = amplifyType
        this.amplifyDmgBonus = amplifyDmgBonus
        this.customMultiplier = customMultiplier
    # Enemy Stats
        this.levelEnemy = levelEnemy
        this.resistanceBase = resistanceBase
        this.resistanceReduction = resistanceReduction
        this.defShred = defShred
        this.defIgnore = defIgnore
    # Conversion
        this.convertToAtk = convertToAtk
        this.convertToHp = convertToHp
        this.convertToDef = convertToDef
        this.convertToER = convertToER
        this.convertToEM = convertToEM
        this.convertToDmgFlat = convertToDmgFlat
        this.convertToDmgBonus = convertToDmgBonus
        this.convertToCritRate = convertToCritRate
        this.convertToCritDmg = convertToCritDmg
    # Buff
        this.buffStatus = buffStatus

class partial:
    def __init__(
        this,
        elementalMastery, energyRecharge, 
        atkPercent, atkFlat,
        hpPercent, hpFlat,
        defPercent, defFlat,
        dmgFlat, 
        dmgBonusElemental, dmgBonusOther,
        critRate, critDmg,
        defShred, defIgnore,
        resistanceReduction,
        ):
        this.elementalMastery = elementalMastery
        this.energyRecharge = energyRecharge
    # Atk
        this.atkPercent = atkPercent
        this.atkFlat = atkFlat
    # Hp
        this.hpPercent = hpPercent
        this.hpFlat = hpFlat
    # Def
        this.defPercent = defPercent
        this.defFlat = defFlat
    # Dmg Bonus
        this.dmgFlat = dmgFlat
        this.dmgBonusElemental = dmgBonusElemental
        this.dmgBonusOther = dmgBonusOther
    # Crit
        this.critRate = critRate
        this.critDmg = critDmg
    # Enemy Stats
        this.defShred = defShred
        this.defIgnore = defIgnore
        this.resistanceReduction = resistanceReduction
        
class stats:
    atk_ = 0
    hp_ = 0
    def_ = 0
    dmg_ = 0
    elementalMastery = 0
    energyRecharge = 0
    dmgBonus = 0
    critRate = 0
    critDmg = 0
    dmgNoCrit = 0
    dmgAvg = 0
    dmgCrit = 0
    amplifyMultiplier = 0
    quickenIncrease = 0
    defMultiplier = 1
    resistanceMultiplier = 1
    
    def convert(this):
        this.atk_ += (this.convertToAtk(this.hp_, this.def_, this.energyRecharge, this.elementalMastery)/100)
        this.hp_ += (this.convertToHp(this.atk_, this.def_, this.energyRecharge, this.elementalMastery)/100)
        this.def_ += (this.convertToDef(this.atk_, this.hp_, this.energyRecharge, this.elementalMastery)/100)
        this.energyRecharge += (this.convertToER(this.atk_, this.hp_, this.def_, this.elementalMastery)/100)
        this.elementalMastery += (this.convertToEM(this.atk_, this.hp_, this.def_, this.energyRecharge)/100)
        
        this.dmgFlat += (this.convertToDmgFlat(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery)/100)
        this.dmgBonus += (this.convertToDmgBonus(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery)/100)
        this.critRate += (this.convertToCritRate(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery)/100)
        this.critDmg += (this.convertToCritDmg(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery)/100)
    
    def calculate(this, base:complete, custom:complete, buff:partial):
        this.atk_ = overload(base.atkBase, custom.atkBase)*(100 + base.atkPercent + custom.atkPercent)/100 + base.atkFlat + base.atkFlat
        this.hp_ = overload(base.hpBase, custom.hpBase)*(100 + base.hpPercent + custom.hpPercent)/100 + base.hpFlat + base.hpFlat
        this.def_ = overload(base.defBase, custom.defBase)*(100 + base.defPercent + custom.defPercent)/100 + base.defFlat + base.defFlat
        
        this.energyRecharge = base.energyRecharge + custom.energyRecharge
        this.elementalMastery = base.elementalMastery + custom.elementalMastery
        
        this.dmgFlat = base.dmgFlat + custom.dmgFlat
        
        this.dmgBonus = base.dmgBonusElemental + base.dmgBonusOther + custom.dmgBonusElemental + custom.dmgBonusOther
        this.critRate = base.critRate + custom.critDmg
        this.critDmg = base.critDmg + custom.critDmg
        
        this.amplifyMultiplier = overload()