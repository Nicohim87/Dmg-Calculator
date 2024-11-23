import numpy as np
from scipy.interpolate import CubicSpline
from packages.helper import Inherit, Atk, Hp, Def, Er, Em, Amp
from packages.base import complete, partial
from sympy import lambdify

# Calculating base reaction dmg based on level using cubic spline interpolation
lv = np.linspace(0, 100, 11)
lv[0] = 1
dm = [17.165605, 34.143343, 80.584775, 136.29291, 207.382042, 323.601597, 492.88489, 765.640231, 1077.443668, 1446.853458, 2030.071808]
ReactionBase = CubicSpline(lv, dm, bc_type='natural')

def format_num(x, y=0):
    # Number formatting function for display
    return f"{x:,.0f}"

def override(a, b, missing = 0):
    # Overriding for specific stats
    if(b == Inherit):      # Inherit
        return a
    elif(b == missing):    # Missing
        return a
    else:                  # Override
        return b
    
def override_exp(exp1, exp2):
    # Override function for lambda function
    # Not always correct, but mostly fine
    if(exp2 == Inherit):                            # Inherit
        return lambdify((Atk, Hp, Def, Em, Er, Amp), exp1)
    f = lambdify((Atk, Hp, Def, Em, Er, Amp), exp2)
    if f(1,2,3,4,5,6) == f(-6,-5,-4,-3,-2,1):         # Missing
        return lambdify((Atk, Hp, Def, Em, Er, Amp), exp1)
    else:                                             # Override
        return lambdify((Atk, Hp, Def, Em, Er, Amp), exp2)

def countTotal(data:list[complete]):
    # Count the total amount of datas inside the storage
    count = 0
    for i in data:
        if i.label != "":
            count += 1
    return count

def validate(value:float, min:float = 0, max:float = 100):
    # Gives a limit of values like crit rate where it cannot go over 100 or below 0
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value
    
def rangify(arr):
    data = [arr[0]]
    for i in range(1, len(arr)):
        data.append(arr[i]-arr[i-1])
    return data
    
def confidenceInterval95(min_v, max_v, theta, n_samples=100):
    theta /= 100 # Proportion
    Z_score = 1.96
    
    # Confidence Interval Range
    ci_range = Z_score * np.sqrt(theta*(1-theta)/n_samples)
    
    # Minimum and maximum proportion, truncate between 0 and 1
    min_rate = max(0, theta - ci_range)
    max_rate = min(1, theta + ci_range)
    
    return min_v * (1-min_rate) + max_v * min_rate, min_v * (1-max_rate) + max_v * max_rate

# EM Reaction bonus
multiplicative = lambda EM: 278*EM / (EM + 1400)
additive = lambda EM: 500*EM / (EM + 1200)

def amplify(base:complete, custom:complete, buff:partial, stdError:complete, EM:float):
    # Calculating reaction multiplier for Vape and Melt
    amplifyType = override(base.amplifyType, custom.amplifyType)
    amplifyBonus = base.amplifyDmgBonus + custom.amplifyDmgBonus + buff.amplifyDmgBonus + stdError.amplifyDmgBonus
    if(amplifyType == 0 or amplifyType == 1):
        return 1
    else:
        return amplifyType * (1 + amplifyBonus + multiplicative(EM))/100 

def quicken(base:complete, custom:complete, buff:partial, stdError:complete, EM:float, dmgBonus:float):
    # Calculate flat dmg bonus for Quicken (Aggravate and Spread)
    quickenType = override(base.quickenType, custom.quickenType)
    quickenBonus = base.quickenDmgBonus + custom.quickenDmgBonus + buff.quickenDmgBonus + stdError.quickenDmgBonus
    amt = base.quickenCount + custom.quickenCount
    if(quickenType == 0):
        return 0
    else:
        return ReactionBase(override(base.level, custom.level))*additive(EM)*quickenType*(1 + dmgBonus + quickenBonus)/100*amt
    
def res_genshin(base, reduction):
    # Resistance formula for Genshin
    res = (base - reduction)/100
    if res < 0:
        return (1 - 0.5*res)
    elif res > .75:
        return (1 / (4*res + 1))
    else:
        return (1 - res)
    
#Resistance formula for HSR
res_hsr = lambda base, reduction: (100 - base + reduction)/100

# Defense formula for Genshin
def_genshin = lambda Lv, Enemy_Lv, defShred, defIgnore: (100 + Lv) / (200 + Lv + Enemy_Lv)*(1 - defShred)*(1 - defIgnore)
# Defense formula for HSR
def_hsr = lambda Lv, Enemy_Lv, defShred, defIgnore: (20 + Lv) / ((20 + Enemy_Lv)*(100 - defShred - defIgnore)/100 + (20 + Lv))

# Damage calculation before crit, res, and def multiplier
damage = lambda base, flat, quicken, dmgBonus, defMultiplier, resMultiplier, customMultiplier: ((base + flat)*(1 + dmgBonus/100)+quicken)*defMultiplier*resMultiplier*customMultiplier

# Calculate the improvement of variable after certain operation
deltaPerc = lambda origin, target: (target / origin - 1)*100