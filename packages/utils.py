import numpy as np
from scipy.interpolate import CubicSpline
from packages.helper import Inherit, Atk, Hp, Def, Er, Em, Amp
from packages.base import complete
from sympy import lambdify

lv = np.linspace(0, 100, 11)
lv[0] = 1
dm = [17.165605, 34.143343, 80.584775, 136.29291, 207.382042, 323.601597, 492.88489, 765.640231, 1077.443668, 1446.853458, 2030.071808]
ReactionBase = CubicSpline(lv, dm, bc_type='natural')

def override(a, b, missing = 0):
    if(b == Inherit):    # Inherit
        return a
    elif(b == missing):    # Missing
        return a
    else:                  # Override
        return b
    
def override_exp(exp1, exp2):
    if(exp2 == Inherit):                            # Inherit
        return lambdify((Atk, Hp, Def, Em, Er, Amp), exp1)
    f = lambdify((Atk, Hp, Def, Em, Er, Amp), exp2)
    if f(1,2,3,4,5,6) == f(-6,-5,-4,-3,-2,1):         # Missing
        return lambdify((Atk, Hp, Def, Em, Er, Amp), exp1)
    else:                                             # Override
        return lambdify((Atk, Hp, Def, Em, Er, Amp), exp2)

def validate(value:float, min:float = 0, max:float = 100):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value
    
multiplicative = lambda EM: 278*EM / (EM + 1400)
additive = lambda EM: 500*EM / (EM + 1200)

def amplify(base:complete, custom:complete, EM:float):
    amplifyType = override(base.amplifyType, custom.amplifyType)
    amplifyBonus = base.amplifyDmgBonus + custom.amplifyDmgBonus
    if(amplifyType == 0 or amplifyType == 1):
        return 1
    else:
        return amplifyType * (1 + amplifyBonus + multiplicative(EM))/100 

def quicken(base:complete, custom:complete, EM:float, dmgBonus:float):
    quickenType = override(base.quickenType, custom.quickenType)
    quickenBonus = base.quickenDmgBonus + custom.quickenDmgBonus
    amt = base.quickenCount + custom.quickenCount
    if(quickenType == 0):
        return 0
    else:
        return ReactionBase*quickenType*(1 + dmgBonus + quickenBonus)/100
    
def res_genshin(base, reduction):
    res = (base - reduction)/100
    if res < 0:
        return (1 - 0.5*res)
    elif res > .75:
        return (1 / (4*res + 1))
    else:
        return (1 - res)
    
res_hsr = lambda base, reduction: (100 - base + reduction)/100
    
def_genshin = lambda Lv, Enemy_Lv, defShred, defIgnore: (100 + Lv) / (200 + Lv + Enemy_Lv)*(1 - defShred)*(1 - defIgnore)
def_hsr = lambda Lv, Enemy_Lv, defShred, defIgnore: (20 + Lv) / ((20 + Enemy_Lv)*(100 - defShred - defIgnore)/100 + (20 + Lv))

damage = lambda base, flat, quicken, dmgBonus, defMultiplier, resMultiplier, customMultiplier: ((base + flat)*(1 + dmgBonus/100)+quicken)*defMultiplier*resMultiplier*customMultiplier

deltaPerc = lambda origin, target: (target / origin - 1)*100