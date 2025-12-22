ab = 32.7
bc = 25.0
cd = [16.3, 20.2, 20.3, 18.5, 16.9]

for cdj in cd:
    wj = ((ab + bc) * (bc + cdj))/(bc*(ab+bc+cdj))
    
    e1 = 0.2 / (ab + bc)
    e2 = 0.2 / (bc + cdj)
    e3 = 0.1 / bc
    e4 = 0.3 / (ab + bc + cdj)
    e = e1 + e2 + e3 + e4
    
    print('wj=',wj)
    print('e=',e)
    print('dwj=',wj*e)