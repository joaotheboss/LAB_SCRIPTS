from math import sqrt

def find_mean(data, n):
    m = len(data[1])
    avg = [0 for _ in range(m)]
    for i in range(m):
        for j in range(1,n+1):
            avg[i]+=data[j][i]
        avg[i] = avg[i]/n
    return avg

def find_stDev(data, avg, n):
    m = len(data[1])
    ds = [0 for _ in range(m)]
    for i in range(m):
        for j in range(1,n+1):
            ds[i]+=(data[j][i]-avg[i])**2
        ds[i] = ds[i]/(n-1)
        ds[i] = sqrt(ds[i])
    return ds

def num_method(values, avg, ds, dec, eps=10e-6):
    n = len(values)
    chi = [0 for _ in range(n)]
    min_chi = 1.7976931348623157e+308
    min_p = -1
    for i in range(9):
        p = values[i]
        for j in range(1,16):
            chi[i]+=(avg[j]-100*((1-p)**j))**2/(ds[j]**2)
        if chi[i]<min_chi:
            min_p = p
            min_chi = chi[i]
    if abs(values[0]-values[1])<eps: return min_p
    dec+=1
    step = 10**(-dec)
    v = [round((min_p+i*step), dec) for i in range(-5, 6)]
    return num_method(v, avg, ds, dec, eps)

file  = open('C:\\Users\\micha\\Desktop\\UNI\\fisica\\EspFisica\\esperimentazioni16_05_2025\\Dati_output_f5_8.txt', 'r')
n = 10
alive = [[100] for _ in range(n+1)]
dead = [[0] for _ in range(n+1)]
for line in file:
    l = line.split()
    ri = int(l[0])
    v = int(l[1])
    alive[ri].append(v)
    dead[ri].append(100-v)
Aavg = find_mean(alive, n)
Davg = [100-x for x in Aavg]
Asd = find_stDev(alive, Aavg, n)
Dsd = Asd[::]
K_Dead = [[0] for _ in range(11)]
for i in range(1,11):
    for j in range(1,16):
        K_Dead[i].append(alive[i][j-1]-alive[i][j])
Kavg = find_mean(K_Dead, n)
Ksd = find_stDev(K_Dead, Kavg, n)
p_value = num_method([0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21], Aavg, Asd, 2)
print(f'p value of the model is {p_value}')

