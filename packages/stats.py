from packages.base import *
from packages.utils import *
from sympy import lambdify

class stats:
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
        this.atk_ = override(base.atkBase, custom.atkBase)*(100 + base.atkPercent + custom.atkPercent + buff.atkPercent)/100 + base.atkFlat + base.atkFlat + buff.atkFlat
        this.hp_ = override(base.hpBase, custom.hpBase)*(100 + base.hpPercent + custom.hpPercent + buff.hpPercent)/100 + base.hpFlat + base.hpFlat + buff.hpFlat
        this.def_ = override(base.defBase, custom.defBase)*(100 + base.defPercent + custom.defPercent + buff.defPercent)/100 + base.defFlat + base.defFlat + buff.defFlat
        
        this.energyRecharge = base.energyRecharge + custom.energyRecharge + buff.energyRecharge
        this.elementalMastery = base.elementalMastery + custom.elementalMastery + buff.elementalMastery
        
        this.dmgFlat = base.dmgFlat + custom.dmgFlat + buff.dmgFlat
        
        this.dmgBonus = base.dmgBonusElemental + base.dmgBonusOther + custom.dmgBonusElemental + custom.dmgBonusOther + buff.dmgBonusElemental + buff.dmgBonusOther
        this.critRate = validate(base.critRate + custom.critRate + buff.critRate)
        this.critDmg = base.critDmg + custom.critDmg + buff.critDmg
        
        this.amplifyMultiplier = amplify(base, custom, this.elementalMastery)
        this.quickenIncrease = quicken(base, custom, this.elementalMastery, this.dmgBonus)
        
        motionValue = override_mv(base.motionValue, custom.motionValue)
        dmg_ = lambdify((Atk, Hp, Def, Em, Er, Amp),motionValue)
        
        defBase = override(base.defBase, custom.defBase)
        defIgnore = base.defIgnore + custom.defIgnore + buff.defIgnore
        defShred = base.defShred + custom.defShred + buff.defShred
        
        resBase = override(base.resBase, custom.resBase)
        resShred = base.resShred + custom.resShred + buff.resShred
        
        this.customMultiplier = override(base.customMultiplier, custom.customMultiplier)
        
        if base.calculationMode == 0:
            this.defMultiplier = def_genshin(defBase, defIgnore, defShred)
            this.resMultiplier = res_genshin(resBase, resShred)
        elif base.calculationMode == 1:
            this.defMultiplier = def_hsr(defBase, defIgnore, defShred)
            this.resMultiplier = res_hsr(resBase, resShred)
        else:
            this.defMultiplier = def_genshin(defBase, defIgnore, defShred)
            this.resMultiplier = res_genshin(resBase, resShred)
        
        this.dmgNoCrit = damage(dmg_, this.dmgFlat, this.quickenIncrease, this.dmgBonus, this.defMultiplier, this.resMultiplier, this.customMultiplier)
        this.dmgCrit = this.dmgNoCrit*(100 + this.critDmg)/100
        this.dmgAvg = this.critRate*this.dmgCrit + (1 - this.critRate)*this.dmgNoCrit