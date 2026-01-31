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
    return f'{A} + x{B} (dB = {float(sqrt(N/(N*Sxx-Sx*Sx))*0.000001)}, dA = {float(sqrt(Sxx/(N*Sxx-Sx*Sx))*0.000001)})'
    
    
    
def process(t, x, v, st_eps, last=0.00756):
    n = len(v)

    df = find_Mindex(v, 0)
    di = find_Zindex(v, df, -1, -1, st_eps)
    d = least_Square(t[di:df+1], v[di:df+1])
    #print(di, df)
    si = find_mindex(v, df)
    sf = find_Zindex(v, si, n, 1, 0.01)
    s = least_Square(t[si:sf+1], v[si:sf+1])
    return d, s
    #print(si, sf)
    #print('\n')


dI, dII, dIII = [], [], []
sI, sII, sIII = [], [], []

for i in range(1,4):
    data = pd.read_csv(rf"C:\\Users\\micha\\Desktop\UNI\\fisica\\EspFisica\\esperimentazioni23_05_2025\\altezzecsv\\h{i}.csv", on_bad_lines='warn', decimal=',', sep=';')
    t = list(data['tempo'])
    x = list(data['posizione'])
    v = list(data['velocità'])
    d, s = process(t, x, v, 0.01)
    print( f'Altezza {i}\n', 'discesa:',d, '\n', 'salita:', s, 2*'\n')
    

