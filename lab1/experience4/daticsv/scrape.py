import pandas as pd
from math import sqrt

def find_Mindex(v, start):
    n = len(v)
    imax = start
    for i in range(start+1, n):
        if v[i]>v[imax]: imax = i
    return imax

def find_mindex(v, start):
    n = len(v)
    imin = start
    for i in range(start+1, n):
        if v[i]<v[imin]: imin = i
    return imin

def find_Zindex(v, start, end, step, eps):
    for i in range(start, end, step):
        if abs(v[i])<(eps): return i

def least_Square(t, v):
    N = len(t)
    Sx = 0
    Sxx = 0
    Sy = 0
    Sxy = 0
    for i in range(N):
        Sx+=t[i]
        Sxx+=t[i]**2
        Sy+=v[i]
        Sxy+=v[i]*t[i]
    det = N*Sxx-Sx*Sx
    detA = Sy*Sxx-Sx*Sxy
    detB = N*Sxy-Sx*Sy
    A = detA/det
    B = detB/det
    #print(f'{A} + x{B}')
    return B, sqrt(N/(N*Sxx-Sx*Sx))*0.000001
    
    
    
def process(t, x, v, st_eps, last=0.00756):
    s, d, es, ed = [], [], [], []
    n = len(v)

    df = find_Mindex(v, 0)
    di = find_Zindex(v, df, -1, -1, st_eps)
    B, e = least_Square(t[di:df+1], v[di:df+1])
    d.append(B)
    ed.append(e)
    si = find_mindex(v, df)
    sf = find_Zindex(v, si, n, 1, 0.00756)
    B, e = least_Square(t[si:sf+1], v[si:sf+1])
    s.append(B)
    es.append(e)

    di = sf+1
    df = find_Mindex(v, di)
    B, e = least_Square(t[di:df+1], v[di:df+1])
    d.append(B)
    ed.append(e)
    si = find_mindex(v, df)
    sf = find_Zindex(v, si, n, 1, 0.00756)
    B, e = least_Square(t[si:sf+1], v[si:sf+1])
    s.append(B)
    es.append(e)

    di = sf+1
    df = find_Mindex(v, di)
    B, e = least_Square(t[di:df+1], v[di:df+1])
    d.append(B)
    ed.append(e)
    si = find_mindex(v, df)
    sf = find_Zindex(v, si, n, 1, last)
    B, e = least_Square(t[si:sf+1], v[si:sf+1])
    s.append(B)
    es.append(e)

    return d, s, ed, es

dI, dII, dIII = [], [], []
sI, sII, sIII = [], [], []
edI, edII, edIII = [], [], []
esI, esII, esIII = [], [], []

for i in range(1,14):
    data = pd.read_csv(rf"C:\\Users\\micha\\Desktop\UNI\\fisica\\EspFisica\\esperimentazioni23_05_2025\\daticsv\\dati{i}.csv", on_bad_lines='warn', decimal=',', sep=';')
    t = list(data['tempo'])
    x = list(data['posizione'])
    v = list(data['velocità'])
    if i == 12 or i == 13: d, s, ed, es = process(t, x, v, 0.001, 0.015)
    elif i == 5: d, s, ed, es = process(t, x, v, 0.02)
    elif i == 2: d, s, ed, es = process(t, x, v, 0.06)
    else: d, s, ed, es = process(t, x, v, 0.001)

    dI.append(d[0])
    dII.append(d[1])
    dIII.append(d[2])
    sI.append(s[0])
    sII.append(s[1])
    sIII.append(s[2])

    edI.append(ed[0])
    edII.append(ed[1])
    edIII.append(ed[2])
    esI.append(es[0])
    esII.append(es[1])
    esIII.append(es[2])

'''
print('DISCESE')
for i in range(13):
    print(f'{dI[i]} ± {edI[i]} m/s')
print('\n')
for i in range(13):
    print(f'{dII[i]} ± {edII[i]} m/s')
print('\n')
for i in range(13):
    print(f'{dIII[i]} ± {edIII[i]} m/s')
print('\n')
print('SALITE')
for i in range(13):
    print(f'{sI[i]} ± {esI[i]} m/s')
print('\n')
for i in range(13):
    print(f'{sII[i]} ± {esII[i]} m/s')
print('\n')
for i in range(13):
    print(f'{sIII[i]} ± {esIII[i]} m/s')
print('\n')'''

# I Discesa
dI = [
    0.3579544,
    0.3578681,
    0.3597456,
    0.3571888,
    0.3587442,
    0.3518693,
    0.3589865,
    0.3553058,
    0.3588240,
    0.3563335,
    0.3519386,
    0.3401478,
    0.3460497
]


# II Discesa
dII = [
    0.3574782,
    0.3574644,
    0.3586544,
    0.3587647,
    0.3579095,
    0.3573932,
    0.3581676,
    0.3569681,
    0.3587371,
    0.3563889,
    0.3575616,
    0.3611700,
    0.3582317
]


# III Discesa
dIII = [
    0.359693,
    0.358015,
    0.364237,
    0.358273,
    0.361238,
    0.362014,
    0.359790,
    0.3557229,
    0.3583039,
    0.3553289,
    0.3607423,
    0.3757056,
    0.360660
]


# I Salita
sI = [
    0.3992582,
    0.3970102,
    0.3985762,
    0.3989062,
    0.3974042,
    0.3983229,
    0.3999116,
    0.3977557,
    0.3977672,
    0.3978246,
    0.3990322,
    0.3991658,
    0.3985276
]


# II Salita
sII = [
    0.400458,
    0.397144,
    0.398123,
    0.395192,
    0.395149,
    0.402239,
    0.401025,
    0.397893,
    0.3971623,
    0.3958378,
    0.400311,
    0.392948,
    0.402465
]


# III Salita
sIII = [
    0.407500,
    0.402907,
    0.390987,
    0.399040,
    0.385740,
    0.395973,
    0.387654,
    0.391834,
    0.391935,
    0.390317,
    0.397499,
    0.375895,
    0.392906
]

'''
avgd = [sum(dI)/13, sum(dII)/13, sum(dIII)/13]
avgs = [sum(sI)/13, sum(sII)/13, sum(sIII)/13]
dvsd = [sqrt(sum((x-avgd[0])**2 for x in dI)/12), sqrt(sum((x-avgd[1])**2 for x in dII)/12), sqrt(sum((x-avgd[2])**2 for x in dIII)/12)]
dvss = [sqrt(sum((x-avgs[0])**2 for x in sI)/12), sqrt(sum((x-avgs[1])**2 for x in sII)/12), sqrt(sum((x-avgs[2])**2 for x in sIII)/12)]


print('DISCESA')
for i in range(3):
    print(f'{avgd[i]} ± {dvsd[i]}')
print('\nSALITA')
for i in range(3):
    print(f'{avgs[i]} ± {dvss[i]}')'''

avgd = [0.355, 0.358, 0.361]
dvsd = [0.006, 0.001, 0.005]
avgs = [0.3984, 0.398, 0.393]
dvss = [0.0008, 0.003, 0.008]

print("test tra dI e dII:", " t = ", (avgd[0]-avgd[1])/(sqrt(2/13*(12*dvsd[0]**2+12*dvsd[1]**2)/24)))
print("test tra dI e dIII:", " t = ", (avgd[0]-avgd[2])/(sqrt(2/13*(12*dvsd[0]**2+12*dvsd[2]**2)/24)))
print("test tra dII e dIII:", " t = ", (avgd[1]-avgd[2])/(sqrt(2/13*(12*dvsd[1]**2+12*dvsd[2]**2)/24)))
print("test tra sI e sII:", " t = ", (avgs[0]-avgs[1])/(sqrt(2/13*(12*dvss[0]**2+12*dvss[1]**2)/24)))
print("test tra sI e sIII:", " t = ", (avgs[0]-avgs[2])/(sqrt(2/13*(12*dvss[0]**2+12*dvss[2]**2)/24)))
print("test tra sII e sIII:", " t = ", (avgs[1]-avgs[2])/(sqrt(2/13*(12*dvss[1]**2+12*dvss[2]**2)/24)))

g = (avgd[0]+avgs[0])/(2*0.038208)
print((avgd[1]+avgs[1])/(2*0.038208))
print((avgd[2]+avgs[2])/(2*0.038208))
mu = (avgs[0]-avgd[0])/(2*g*0.999270)
print(mu)
