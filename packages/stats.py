from packages.base import *
from packages.utils import *

class stats(complete):
    label = ""
    atk_ = 0
    hp_ = 0
    def_ = 0
    dmg_ = 0
    elementalMastery = 0
    energyRecharge = 0
    dmgFlat = 0
    dmgBonus = 0
    critRate = 0
    critDmg = 0
    dmgNoCrit = 0
    dmgAvg = 0
    dmgCrit = 0
    dmgNoCrit_err = 0
    dmgAvg_err = 0
    dmgCrit_err = 0
    amplifyMultiplier = 1
    quickenIncrease = 0
    defMultiplier = 1
    resMultiplier = 1
    customMultiplier = 1
    
    def __init__(this):
        return
    
    def display(this):
        # Display the stats
        print(f"Atk = {this.atk_}\nHp = {this.hp_}\nDef = {this.def_}\nER = {this.energyRecharge}\nEM = {this.elementalMastery}\nDmg Bonus = {this.dmgBonus}\nCrit Rate = {this.critRate}\nCrit Damage = {this.critDmg}\nDmg Non Crit = {this.dmgNoCrit}\nDmg Average = {this.dmgAvg}\nDmg Crit = {this.dmgCrit}")
    
    def convert(this, base:complete, custom:complete): 
        # Conversion and add it to the stats
        convertToAtk = override_exp(base.convertToAtk, custom.convertToAtk)
        convertToHp = override_exp(base.convertToHp, custom.convertToHp)
        convertToDef = override_exp(base.convertToDef, custom.convertToDef)
        convertToER = override_exp(base.convertToER, custom.convertToER)
        convertToEM = override_exp(base.convertToEM, custom.convertToEM)
        
        convertToDmgFlat = override_exp(base.convertToDmgFlat, custom.convertToDmgFlat)
        convertToDmgBonus = override_exp(base.convertToDmgBonus, custom.convertToDmgBonus)
        convertToCritRate = override_exp(base.convertToCritRate, custom.convertToCritRate)
        convertToCritDmg = override_exp(base.convertToCritDmg, custom.convertToCritDmg)
        
        this.atk_ += (convertToAtk(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        this.hp_ += (convertToHp(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        this.def_ += (convertToDef(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        this.energyRecharge += (convertToER(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        this.elementalMastery += (convertToEM(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        
        this.dmgFlat += (convertToDmgFlat(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        this.dmgBonus += (convertToDmgBonus(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        this.critRate += (convertToCritRate(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        this.critDmg += (convertToCritDmg(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, 0))
        
    
    def calculate(this, base:complete, custom:complete, buff:partial, Error:bool = True):
        # Damage calculation 
        buffStatus = override(base.buffStatus, custom.buffStatus,-1)
        if buffStatus == False:
            # If buff is not applied, change every value to zero
            buff = partial(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        
        if Error == False:
            # Do not calculate the error
            stdError = complete()
        else:
            # Calculate the error
            stdError = complete(
                                atkBase=1, atkPercent=0.2, atkFlat=2,
                                hpBase=1, hpPercent=0.2, hpFlat=2,
                                defBase=1, defPercent=0.2, defFlat=2,
                                elementalMastery=1, energyRecharge=0.2,
                                dmgFlat=2, dmgBonusElemental=0.2, dmgBonusOther=0.2,
                                amplifyDmgBonus=0.2, quickenDmgBonus=0.2,
                                critRate=0.2, critDmg=0.2
                                )
        
        # Base stats calculation
        this.atk_ = (override(base.atkBase, custom.atkBase) + stdError.atkBase)*(100 + base.atkPercent + custom.atkPercent + buff.atkPercent + stdError.atkPercent)/100 + base.atkFlat + custom.atkFlat + buff.atkFlat + stdError.atkFlat
        this.hp_ = (override(base.hpBase, custom.hpBase) + stdError.hpBase)*(100 + base.hpPercent + custom.hpPercent + buff.hpPercent + stdError.hpPercent)/100 + base.hpFlat + custom.hpFlat + buff.hpFlat + stdError.hpFlat
        this.def_ = (override(base.defBase, custom.defBase) + stdError.defBase)*(100 + base.defPercent + custom.defPercent + buff.defPercent + stdError.defPercent)/100 + base.defFlat + custom.defFlat + buff.defFlat + stdError.defFlat
        
        this.energyRecharge = base.energyRecharge + custom.energyRecharge + buff.energyRecharge + stdError.energyRecharge
        this.elementalMastery = base.elementalMastery + custom.elementalMastery + buff.elementalMastery + stdError.elementalMastery
        
        this.dmgFlat = base.dmgFlat + custom.dmgFlat + buff.dmgFlat + stdError.dmgFlat
        
        this.dmgBonus = base.dmgBonusElemental + base.dmgBonusOther + custom.dmgBonusElemental + custom.dmgBonusOther + buff.dmgBonusElemental + buff.dmgBonusOther + stdError.dmgBonusElemental + stdError.dmgBonusOther
        this.critRate = validate(base.critRate + custom.critRate + buff.critRate + stdError.critRate) # Crit rate has minimum value of 0 and maximum value of 100
        this.critDmg = base.critDmg + custom.critDmg + buff.critDmg + stdError.critDmg
        
        # Reaction bonus calculation
        this.amplifyMultiplier = amplify(base, custom, buff, stdError, this.elementalMastery)
        this.quickenIncrease = quicken(base, custom, buff, stdError, this.elementalMastery, this.dmgBonus)
        
        # Stat conversion
        this.convert(base, custom)
        
        # Motion value and base damage
        motionValue = override_exp(base.motionValue, custom.motionValue)
        this.dmg_ = motionValue(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, this.amplifyMultiplier)
        
        # Enemy Defense stats calculation
        lv = override(base.level, custom.level)
        lvEnemy = override(base.levelEnemy, custom.levelEnemy)
        defIgnore = base.defIgnore + custom.defIgnore + buff.defIgnore
        defShred = base.defShred + custom.defShred + buff.defShred
        
        # Enemy Resistance stats calculation
        resBase = override(base.resBase, custom.resBase)
        resShred = base.resShred + custom.resShred + buff.resShred
        
        # Custom multiplier for generality
        this.customMultiplier = override(base.customMultiplier, custom.customMultiplier)
        if this.customMultiplier == 0:
            this.customMultiplier = 1
            
        
        # Calculate the def and res multiplier based on game
        # 0 for Genshin Impact
        # 1 for Honkai: Star Rail
        # Else, default at Genshin Impact
        if base.calculationMode == 0:
            this.defMultiplier = def_genshin(lv, lvEnemy, defShred, defIgnore)
            this.resMultiplier = res_genshin(resBase, resShred)
        elif base.calculationMode == 1:
            this.defMultiplier = def_hsr(lv, lvEnemy, defIgnore, defShred)
            this.resMultiplier = res_hsr(resBase, resShred)
        else:
            this.defMultiplier = def_genshin(lv, lvEnemy, defIgnore, defShred)
            this.resMultiplier = res_genshin(resBase, resShred)
        
        # Critical damage calculations
        this.dmgNoCrit = damage(this.dmg_, this.dmgFlat, this.quickenIncrease, this.dmgBonus, this.defMultiplier, this.resMultiplier, this.customMultiplier)/100
        this.dmgCrit = this.dmgNoCrit*(100 + this.critDmg)/100
        this.dmgAvg = (this.critRate/100*this.dmgCrit + (1 - this.critRate/100)*this.dmgNoCrit)
        
        # Error Calculation
        if Error == True :
            # Store the dmg value if calculate with error
            this.dmgNoCrit_err = this.dmgNoCrit
            this.dmgAvg_err = this.dmgAvg
            this.dmgCrit_err = this.dmgCrit
            this.calculate(base, custom, buff, False) # Re iterate without error
        else:
            # Print the dmg calculated if calculate without error
            print(f"Dmg No Crit: {format_num(this.dmgNoCrit)} to {format_num(this.dmgNoCrit_err)}")
            print(f"Dmg Crit: {format_num(this.dmgCrit)} to {format_num(this.dmgCrit_err)}")
            print(f"Dmg Avg: {format_num(this.dmgAvg)} to {format_num(this.dmgAvg_err)}")
            