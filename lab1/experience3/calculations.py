from math import sqrt
file  = open('C:\\Users\\micha\\Desktop\\UNI\\fisica\\EspFisica\\esperimentazioni16_05_2025\\Dati_output_f5_8.txt', 'r')

alive = [[100] for _ in range(11)]
dead = [[0] for _ in range(11)]
for line in file:
    l = line.split()
    ri = int(l[0])
    v = int(l[1])
    alive[ri].append(v)
    dead[ri].append(100-v)
Aavg = [0 for _ in range(16)]
for i in range(16):
    for j in range(1,11):
        Aavg[i]+=alive[j][i]
    Aavg[i] = Aavg[i]/10
Advsc = [0 for _ in range(16)]
for i in range(16):
    for j in range(1,11):
        Advsc[i]+=(alive[j][i]-Aavg[i])**2
    Advsc[i] = Advsc[i]/9
    Advsc[i] = sqrt(Advsc[i])

#NELLA RELAZIONE DIMOSTRATE CHE Aavg[i]+Davg[i] = 100 
 
Davg = [0 for _ in range(16)]
for i in range(16):
    for j in range(1,11):
        Davg[i]+=dead[j][i]
    Davg[i] = Davg[i]/10
Ddvsc = [0 for _ in range(16)]
for i in range(16):
    for j in range(1,11):
        Ddvsc[i]+=(dead[j][i]-Davg[i])**2
    Ddvsc[i] = Ddvsc[i]/9
    Ddvsc[i] = sqrt(Ddvsc[i])

n_dead = [[0] for _ in range(11)]
for i in range(1,11):
    for j in range(1,16):
        n_dead[i].append(alive[i][j-1]-alive[i][j])

n_Davg = [0 for _ in range(16)]
for i in range(16):
    for j in range(1,11):
        n_Davg[i]+=n_dead[j][i]
    n_Davg[i] = n_Davg[i]/10
n_Ddvsc = [0 for _ in range(16)]
for i in range(16):
    for j in range(1,11):
        n_Ddvsc[i]+=(n_dead[j][i]-n_Davg[i])**2
    n_Ddvsc[i] = n_Ddvsc[i]/9
    n_Ddvsc[i] = sqrt(n_Ddvsc[i])

print(Advsc)
input()

'''
for i in range(16):
    print(f"O{i}: ALIVE = [avg = {Aavg[i]}] TOTAL DEAD = [avg = {Davg[i]}] s= {Advsc[i]}; N_DEAD = [avg = {n_Davg[i]} s = {n_Ddvsc[i]} ]")
for i in range(16):
    print(f"O{i}:N_DEAD = [avg = {n_Davg[i]} s = {n_Ddvsc[i]} ]")
for i in range(16):
    print(f"O{i}: s = {Advsc[i]} ]")    
for i in range(16):
    print(f"O{i}: s = {n_Ddvsc[i]} ]")  
'''

Ps = [0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21]
chi = [0 for _ in range(9)]
for i in range(9):
    p = Ps[i]
    for j in range(1,16):
        chi[i]+=(Aavg[j]-100*((1-p)**j))**2/(Advsc[j]**2)

for i in range(9):
    print(f"p = {Ps[i]} -> chi = {chi[i]}")
print('\n')

Ps = [0.165, 0.166, 0.167, 0.168, 0.169, 0.17, 0.171, 0.172, 0.173, 0.174, 0.175]
chi = [0 for _ in range(11)]
for i in range(11):
    p = Ps[i]
    for j in range(1,16):
        chi[i]+=(Aavg[j]-100*((1-p)**j))**2/(Advsc[j]**2)

for i in range(11):
    print(f"p = {Ps[i]} -> chi = {chi[i]}")
print('\n')

Ps = [0.1696, 0.1697, 0.1698, 0.1699, 0.17, 0.1701, 0.1702, 0.1703, 0.1704, 0.1705]
chi = [0 for _ in range(10)]
for i in range(10):
    p = Ps[i]
    for j in range(1,16):
        chi[i]+=(Aavg[j]-100*((1-p)**j))**2/(Advsc[j]**2)

for i in range(10):
    print(f"p = {Ps[i]} -> chi = {chi[i]}")
print('\n')

Ps = [0.16956, 0.16957, 0.16958, 0.16959, 0.1696, 0.16961, 0.16962, 0.16963, 0.16964, 0.16965]
chi = [0 for _ in range(10)]
for i in range(10):
    p = Ps[i]
    for j in range(1,16):
        chi[i]+=(Aavg[j]-100*((1-p)**j))**2/(Advsc[j]**2)

for i in range(10):
    print(f"p = {Ps[i]} -> chi = {chi[i]}")