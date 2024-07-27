from packages.base import *
from packages.utils import *

class stats:
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
    amplifyMultiplier = 1
    quickenIncrease = 0
    defMultiplier = 1
    resMultiplier = 1
    customMultiplier = 1
    
    def display(this):
        print(f"Atk = {this.atk_}\nHp = {this.hp_}\nDef = {this.def_}\nER = {this.energyRecharge}\nEM = {this.elementalMastery}\nDmg Bonus = {this.dmgBonus}\nCrit Rate = {this.critRate}\nCrit Damage = {this.critDmg}\nDmg Non Crit = {this.dmgNoCrit}\nDmg Average = {this.dmgAvg}\nDmg Crit = {this.dmgCrit}")
    
    def convert(this, base:complete, custom:complete): 
        convertToAtk = override_exp(base.convertToAtk, custom.convertToAtk)
        convertToHp = override_exp(base.convertToHp, custom.convertToHp)
        convertToDef = override_exp(base.convertToDef, custom.convertToDef)
        convertToER = override_exp(base.convertToER, custom.convertToER)
        convertToEM = override_exp(base.convertToEM, custom.convertToEM)
        
        convertToDmgFlat = override_exp(base.convertToDmgFlat, custom.convertToDmgFlat)
        convertToDmgBonus = override_exp(base.convertToDmgBonus, custom.convertToDmgBonus)
        convertToCritRate = override_exp(base.convertToCritRate, custom.convertToCritRate)
        convertToCritDmg = override_exp(base.convertToCritDmg, custom.convertToCritDmg)
        
        this.atk_ += (convertToAtk(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
        this.hp_ += (convertToHp(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
        this.def_ += (convertToDef(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
        this.energyRecharge += (convertToER(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
        this.elementalMastery += (convertToEM(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
        
        this.dmgFlat += (convertToDmgFlat(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
        this.dmgBonus += (convertToDmgBonus(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
        this.critRate += (convertToCritRate(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
        this.critDmg += (convertToCritDmg(this.atk_, this.hp_, this.def_, this.energyRecharge, this.elementalMastery, 0))
    
    def calculate(this, base:complete, custom:complete, buff:partial):
        this.atk_ = override(base.atkBase, custom.atkBase)*(100 + base.atkPercent + custom.atkPercent + buff.atkPercent)/100 + base.atkFlat + custom.atkFlat + buff.atkFlat
        this.hp_ = override(base.hpBase, custom.hpBase)*(100 + base.hpPercent + custom.hpPercent + buff.hpPercent)/100 + base.hpFlat + custom.hpFlat + buff.hpFlat
        this.def_ = override(base.defBase, custom.defBase)*(100 + base.defPercent + custom.defPercent + buff.defPercent)/100 + base.defFlat + custom.defFlat + buff.defFlat
        
        this.energyRecharge = base.energyRecharge + custom.energyRecharge + buff.energyRecharge
        this.elementalMastery = base.elementalMastery + custom.elementalMastery + buff.elementalMastery
        
        this.dmgFlat = base.dmgFlat + custom.dmgFlat + buff.dmgFlat
        
        this.dmgBonus = base.dmgBonusElemental + base.dmgBonusOther + custom.dmgBonusElemental + custom.dmgBonusOther + buff.dmgBonusElemental + buff.dmgBonusOther
        this.critRate = validate(base.critRate + custom.critRate + buff.critRate)
        this.critDmg = base.critDmg + custom.critDmg + buff.critDmg
        
        this.amplifyMultiplier = amplify(base, custom, this.elementalMastery)
        this.quickenIncrease = quicken(base, custom, this.elementalMastery, this.dmgBonus)
        
        this.convert(base, custom)
        
        motionValue = override_exp(base.motionValue, custom.motionValue)
        dmg_ = motionValue(this.atk_, this.hp_, this.def_, this.elementalMastery, this.energyRecharge, this.amplifyMultiplier)
        
        lv = override(base.level, custom.level)
        lvEnemy = override(base.levelEnemy, custom.levelEnemy)
        defIgnore = base.defIgnore + custom.defIgnore + buff.defIgnore
        defShred = base.defShred + custom.defShred + buff.defShred
        
        resBase = override(base.resBase, custom.resBase)
        resShred = base.resShred + custom.resShred + buff.resShred
        
        this.customMultiplier = override(base.customMultiplier, custom.customMultiplier)
        
        if base.calculationMode == 0:
            this.defMultiplier = def_genshin(lv, lvEnemy, defShred, defIgnore)
            this.resMultiplier = res_genshin(resBase, resShred)
        elif base.calculationMode == 1:
            this.defMultiplier = def_hsr(lv, lvEnemy, defIgnore, defShred)
            this.resMultiplier = res_hsr(resBase, resShred)
        else:
            this.defMultiplier = def_genshin(lv, lvEnemy, defIgnore, defShred)
            this.resMultiplier = res_genshin(resBase, resShred)
        
        this.dmgNoCrit = damage(dmg_, this.dmgFlat, this.quickenIncrease, this.dmgBonus, this.defMultiplier, this.resMultiplier, this.customMultiplier)/100
        this.dmgCrit = this.dmgNoCrit*(100 + this.critDmg)/100
        this.dmgAvg = (this.critRate*this.dmgCrit + (1 - this.critRate/100)*this.dmgNoCrit)/100
        
        this.display()