class partial:
    def __init__(
        this,
        elementalMastery, energyRecharge, 
        atkPercent, atkFlat,
        hpPercent, hpFlat,
        defPercent, defFlat,
        dmgFlat, quickenDmgBonus, amplifyDmgBonus,
        dmgBonusElemental, dmgBonusOther,
        critRate, critDmg,
        defShred, defIgnore,
        resShred,
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
        this.quickenDmgBonus = quickenDmgBonus
        this.amplifyDmgBonus = amplifyDmgBonus
        this.dmgBonusElemental = dmgBonusElemental
        this.dmgBonusOther = dmgBonusOther
    # Crit
        this.critRate = critRate
        this.critDmg = critDmg
    # Enemy Stats
        this.defShred = defShred
        this.defIgnore = defIgnore
        this.resShred = resShred
    def __str__(this):
        return f"Buffs: \n\n\
Atk%: {this.atkPercent}%\nAtk: {this.atkFlat}\n\
Hp%: {this.hpPercent}%\nHp: {this.hpFlat}\n\
Def%: {this.defPercent}%\nDef: {this.defFlat}\n\
Dmg Bonus: {this.dmgBonusElemental + this.dmgBonusOther}%\nDmg Flat: {this.dmgFlat}\n\
Crit Rate: {this.critRate}%\nCrit Dmg: {this.critDmg}%\n\
Quicken Dmg Bonus: {this.quickenDmgBonus}%\nAmplify Dmg Bonus: {this.amplifyDmgBonus}%\n\
Def Shred: {this.defShred}\nDef Ignore:{this.defIgnore}\n\
Res Shred: {this.resShred}%\n\
"

class complete(partial):
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
        quickenType, quickenDmgBonus, quickenCount,
        amplifyType, amplifyDmgBonus,
        customMultiplier,
        levelEnemy, resBase, resShred,
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
        this.quickenCount = quickenCount
        this.amplifyType = amplifyType
        this.amplifyDmgBonus = amplifyDmgBonus
        this.customMultiplier = customMultiplier
    # Enemy Stats
        this.levelEnemy = levelEnemy
        this.resBase = resBase
        this.resShred = resShred
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