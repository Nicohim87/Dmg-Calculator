class partial:
    # For other purposes which complements Complete class
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
    # Primary type of data which is stored
    def __init__(
        this, 
        level = 0, calculationMode = 0,
        elementalMastery = 0, energyRecharge = 0, 
        atkBase = 0, atkPercent = 0, atkFlat = 0,
        hpBase = 0, hpPercent = 0, hpFlat = 0,
        defBase = 0, defPercent = 0, defFlat = 0,
        motionValue = 0, dmgFlat = 0, 
        dmgBonusElemental = 0, dmgBonusOther = 0,
        critRate = 0, critDmg = 0,
        quickenType = 0, quickenDmgBonus = 0, quickenCount = 0,
        amplifyType = 0, amplifyDmgBonus = 0,
        customMultiplier = 0,
        levelEnemy = 0, resBase = 0, resShred = 0,
        defShred = 0, defIgnore = 0,
        convertToAtk = 0, convertToHp = 0, convertToDef = 0, convertToER = 0, convertToEM = 0, 
        convertToDmgFlat = 0, convertToDmgBonus = 0, convertToCritRate = 0, convertToCritDmg = 0, buffStatus = 0
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

    def __str__(this):
        return ""