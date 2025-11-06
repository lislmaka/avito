import math

def formula_morma(value):
    return 1/(1 + math.pow(math.e, 1/value))

def formula_morma2(value, mmin, mmax):
    return (value - mmin) / (mmax - mmin)

l = [1981, 1978, 2000, 2011, 1995]

print(math.e)
for i in l:
    r = formula_morma2(i, 1970, 2020)
    print(f"{i} = {r}, {round(1 - r, 2)}")