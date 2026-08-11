import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import os
# Definiamo la cartella corretta una volta sola
OUTPUT_DIR = r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05"


def calcola_decimali_colonna(incertezze, n_sig_figs=2):
    """Calcola quanti decimali servono per tutta la colonna in base a 2 cifre significative."""
    decimali = []
    for u in incertezze:
        if u > 0 and not np.isnan(u):
            prima_cifra = int(np.floor(np.log10(abs(u))))
            decimali.append(max(0, -prima_cifra + (n_sig_figs - 1)))
    return max(decimali) if decimali else 2

def formatta_cella(x, u_x, decimali_colonna):
    """Formatta la misura applicando un numero fisso di decimali per l'intera colonna."""
    if x == '-':
        return "-"
    if u_x <= 0 or np.isnan(u_x):
        return f"${x:.{decimali_colonna}f}$"
    
    # Costruiamo i pezzi separati per evitare conflitti con le f-string
    valore_str = f"{x:.{decimali_colonna}f}"
    incertezza_str = f"{u_x:.{decimali_colonna}f}"
    
    # Uniamo tutto usando una stringa RAW (r"...") pura con un solo doppio backslash per LaTeX
    return r"$" + valore_str + r" \pm " + incertezza_str + r"$"

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
def format_misura(x, u_x, n=1):
    # 1. Trova la posizione della prima cifra significativa
    prima_cifra = int(np.floor(np.log10(abs(u_x))))
    
    # 2. Calcola quanti decimali servono per averne 'n' significative
    # Se il risultato è negativo (es. incertezza sulle centinaia), usiamo 0 decimali
    decimali = max(0, -prima_cifra + (n - 1))
    
    # 3. Restituisce la stringa formattata
    return f"{x:.{decimali}f}\\\\pm {u_x:.{decimali}f}"

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
#teta.. = -gamma*teta.-beta*sign(gamma.)-omega_0^2*sin(teta) + tau_0

def comma_to_float(s):
    return float(s.replace(',', '.'))

def find_index(data, rows, padding, personal=False):
    #il padding (non per_padding) è stato inserito per aggiustare meglio il taglio dei dati
    run = []
    per_padding = [1, 3, 3, 2, 2]
    for j in range(1, 20, 4):
        #trovo il massimo punto a cui lo mettiamo
        i_max = 0
        i = 1
        while i<rows and np.isnan(data[i][j]) == False:
            if data[i][j]>=data[i_max][j]: i_max = i
            i+=1
        #trovo il punto più vicino all'angolo 1 rad da cui iniziare il fit
        i_start = i_max
        i = i_max+1
        while i<rows and np.isnan(data[i][j]) == False:
            if abs(data[i][j]-1)<=abs(data[i_start][j]-1): i_start = i
            i+=1
        #trovo il punto di stop
        i_end = rows-1
        while np.isnan(data[i_end][j+1]) or abs(data[i_end][j+1])<0.001:
            i_end-=1
        if personal==True: run.append([i_start+per_padding[j//4], i_end])
        else: run.append([i_start+padding, i_end])
    return run

def get_data(path, padding=0, personal=False):
    data = np.genfromtxt(path, delimiter=';', skip_header=3, converters={i: comma_to_float for i in range(20)})
    rows = len(data)
    index = find_index(data, rows, padding)
    p = []
    #metto gli elementi negli array che mi servono per i fit
    ele = np.array([data[i][1+j*4] for j in range(5) for i in range(index[j][0], index[j][1]+1)])
    p.append(ele)
    ele = np.array([data[i][2+j*4] for j in range(5) for i in range(index[j][0], index[j][1]+1)])
    p.append(ele)
    ele = np.array([data[i][3+j*4] for j in range(5) for i in range(index[j][0], index[j][1]+1)])
    p.append(ele)
    ele = np.array([data[i][j*4] for j in range(5) for i in range(index[j][0], index[j][1]+1)])
    p.append(ele)
    return p, index

def plotting(p, ind, k):
    #funzione per graficare le oscillazioni
    a = -ind[0][0]+ind[0][1]
    b = -ind[1][0]+ind[1][1]
    c = -ind[2][0]+ind[2][1]
    d = -ind[3][0]+ind[3][1]
    e = -ind[4][0]+ind[4][1]
    plt.figure(k)
    plt.subplot(2, 3, 1)
    plt.plot(p[3][0:a], p[0][0:a])
    plt.subplot(2, 3, 2)
    plt.plot(p[3][a+1:a+b+1], p[0][a+1:a+b+1])
    plt.subplot(2, 3, 3)
    plt.plot(p[3][a+b+2:a+b+c+2], p[0][a+b+2:a+b+c+2])
    plt.subplot(2, 3, 4)
    plt.plot(p[3][a+b+c+3:a+b+c+d+3], p[0][a+b+c+3:a+b+c+d+3])
    plt.subplot(2, 3, 5)
    plt.plot(p[3][a+b+c+d+4:a+b+c+d+e+4], p[0][a+b+c+d+4:a+b+c+d+e+4])


# p[0] = teta   p[1] = omega   p[2] = alfa   p[3] = tempo
'''
NOTA!!!!
avrei dovuto fare la selezione a mano per ogni run però troppo tempo troppo pigro
quindi ho fatto una prima selezione degli intervalli per ogni run in modo automatico con find_index
poi siccome era una generalizzazione eccessiva per ogni file ho inserito un padding manuale fisso
tale padding viene applicato indistintamente a tutte le run anche se ad alcune non servirebbe
l'unico dove ho fatto dei padding ad hoc è stato il file B3_pettine, che ha la flag personal settata a True
per vedere i grafici delle oscillazioni teta decommenta plt.show() alla fine di questo blocco
'''


noB_piena, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\piena_noB.csv", 3)
plotting(noB_piena, ind, 1)
noB_pettine, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\pettine_noB.csv", 2)
plotting(noB_pettine, ind, 2)
noB_fessurato, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\fessurato_noB.csv", 1)
plotting(noB_fessurato, ind, 3)
B1_piena, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\piena_B1.csv", 5)
plotting(B1_piena, ind, 4)
B1_pettine, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\pettine_B1.csv", 21) 
plotting(B1_pettine, ind, 5)
B1_fessurato, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\fessurato_B1.csv", 3)
plotting(B1_fessurato, ind, 6)
B2_piena, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\piena_B2.csv", 1)
plotting(B2_piena, ind, 7)
B2_pettine, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\pettine_B2.csv", 1)
plotting(B2_pettine, ind, 8)
B2_fessurato, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\fessurato_B2.csv", 4)
plotting(B2_fessurato, ind, 9)
B3_piena, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\piena_B3.csv", 1)
plotting(B3_piena, ind, 10)
B3_pettine, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\pettine_B3.csv", 0, True)
plotting(B3_pettine, ind, 11)
B3_fessurato, ind = get_data(r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_11_05\fessurato_B3.csv", 2)
plotting(B3_fessurato, ind, 12)
#plt.show()
plt.close()

def fitting(p, u):
    #fitto come da teoria
    W = np.diag(1/u**2)
    Y = p[2].reshape(-1, 1)
    c1 = np.ones(len(p[0]))
    c2 = -np.sin(p[0])
    c3 = -np.sign(p[1])
    c4 = -p[1]
    X = np.column_stack((c1, c2, c3, c4))
    COV_1 = np.dot(np.dot(np.transpose(X), W), X)
    B = np.dot(np.dot(np.transpose(X), W), Y)
    A = np.linalg.solve(COV_1, B)
    COV = np.linalg.pinv(COV_1)
    return A, COV

#calcolo incertezza di alfa
fs = 1/0.05
u_a = 2*(fs**2)*0.09/180*np.pi*1/np.sqrt(3)
print(u_a)

col = [
    'Configurazione piastre', 
    r'$\tau_0$ $(rad/s^{2})$', 
    r'$\omega_0^2$ $(1/s^{2})$', 
    r'$\beta$ $(rad/s^{2})$', # Modificato in \beta coerentemente con i print
    r'$\gamma$ $(rad/s)$', 
    r'$\gamma_m$ $(rad/s)$'
]

dist = [
    'B assente', 
    r'$d = 0.02700 \pm 0.00003$ m', 
    r'$d = 0.03190 \pm 0.00003$ m', 
    r'$d = 0.03920 \pm 0.00003$ m'
]



# 1. Lastra piena senza B
u = np.full(len(noB_piena[2]), u_a)
Ap, U_Ap = fitting(noB_piena, u)
U_Ap = np.diag(U_Ap)

# 2. Lastra piena con B1
u = np.full(len(B1_piena[2]), u_a)
Ap1, U_Ap1 = fitting(B1_piena, u)
U_Ap1 = np.diag(U_Ap1)
u_gmp1 = np.sqrt(U_Ap1[3]**2 + U_Ap[3]**2)

# 3. Lastra piena con B2
u = np.full(len(B2_piena[2]), u_a)
Ap2, U_Ap2 = fitting(B2_piena, u)
U_Ap2 = np.diag(U_Ap2)
u_gmp2 = np.sqrt(U_Ap2[3]**2 + U_Ap[3]**2)

# 4. Lastra piena con B3
u = np.full(len(B3_piena[2]), u_a)
Ap3, U_Ap3 = fitting(B3_piena, u)
U_Ap3 = np.diag(U_Ap3)
u_gmp3 = np.sqrt(U_Ap3[3]**2 + U_Ap[3]**2)



u_tau_list = [U_Ap[0], U_Ap1[0], U_Ap2[0], U_Ap3[0]]
dec_tau = calcola_decimali_colonna(u_tau_list, 2)

u_omega_list = [U_Ap[1], U_Ap1[1], U_Ap2[1], U_Ap3[1]]
dec_omega = calcola_decimali_colonna(u_omega_list, 2)

u_beta_list = [U_Ap[2], U_Ap1[2], U_Ap2[2], U_Ap3[2]]
dec_beta = calcola_decimali_colonna(u_beta_list, 2)

u_gamma_list = [U_Ap[3], U_Ap1[3], U_Ap2[3], U_Ap3[3]]
dec_gamma = calcola_decimali_colonna(u_gamma_list, 2)

u_gammam_list = [u_gmp1, u_gmp2, u_gmp3]
dec_gammam = calcola_decimali_colonna(u_gammam_list, 2)


data = [
    [
        dist[0],
        formatta_cella(Ap[0][0], U_Ap[0], dec_tau),
        formatta_cella(Ap[1][0], U_Ap[1], dec_omega),
        formatta_cella(Ap[2][0], U_Ap[2], dec_beta),
        formatta_cella(Ap[3][0], U_Ap[3], dec_gamma),
        '-'
    ],
    [
        dist[1],
        formatta_cella(Ap1[0][0], U_Ap1[0], dec_tau),
        formatta_cella(Ap1[1][0], U_Ap1[1], dec_omega),
        formatta_cella(Ap1[2][0], U_Ap1[2], dec_beta),
        formatta_cella(Ap1[3][0], U_Ap1[3], dec_gamma),
        formatta_cella(Ap1[3][0] - Ap[3][0], u_gmp1, dec_gammam)
    ],
    [
        dist[2],
        formatta_cella(Ap2[0][0], U_Ap2[0], dec_tau),
        formatta_cella(Ap2[1][0], U_Ap2[1], dec_omega),
        formatta_cella(Ap2[2][0], U_Ap2[2], dec_beta),
        formatta_cella(Ap2[3][0], U_Ap2[3], dec_gamma),
        formatta_cella(Ap2[3][0] - Ap[3][0], u_gmp2, dec_gammam)
    ],
    [
        dist[3],
        formatta_cella(Ap3[0][0], U_Ap3[0], dec_tau),
        formatta_cella(Ap3[1][0], U_Ap3[1], dec_omega),
        formatta_cella(Ap3[2][0], U_Ap3[2], dec_beta),
        formatta_cella(Ap3[3][0], U_Ap3[3], dec_gamma),
        formatta_cella(Ap3[3][0] - Ap[3][0], u_gmp3, dec_gammam)
    ]
]


fig, ax = plt.subplots(figsize=(8, 1.5))
ax.axis('off')

tabella = ax.table(
    cellText=data,          
    colLabels=col,   
    loc='center',           
    cellLoc='center'        
)


for (row, col_idx), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')


plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'lastra_piena.pgf'))
plt.close()





# 1. Lastra piena senza B
u = np.full(len(noB_pettine[2]), u_a)
Ap, U_Ap = fitting(noB_pettine, u)
U_Ap = np.diag(U_Ap)

# 2. Lastra piena con B1
u = np.full(len(B1_pettine[2]), u_a)
Ap1, U_Ap1 = fitting(B1_pettine, u)
U_Ap1 = np.diag(U_Ap1)
u_gmp1 = np.sqrt(U_Ap1[3]**2 + U_Ap[3]**2)

# 3. Lastra piena con B2
u = np.full(len(B2_pettine[2]), u_a)
Ap2, U_Ap2 = fitting(B2_pettine, u)
U_Ap2 = np.diag(U_Ap2)
u_gmp2 = np.sqrt(U_Ap2[3]**2 + U_Ap[3]**2)

# 4. Lastra piena con B3
u = np.full(len(B3_pettine[2]), u_a)
Ap3, U_Ap3 = fitting(B3_pettine, u)
U_Ap3 = np.diag(U_Ap3)
u_gmp3 = np.sqrt(U_Ap3[3]**2 + U_Ap[3]**2)



u_tau_list = [U_Ap[0], U_Ap1[0], U_Ap2[0], U_Ap3[0]]
dec_tau = calcola_decimali_colonna(u_tau_list, 2)

u_omega_list = [U_Ap[1], U_Ap1[1], U_Ap2[1], U_Ap3[1]]
dec_omega = calcola_decimali_colonna(u_omega_list, 2)

u_beta_list = [U_Ap[2], U_Ap1[2], U_Ap2[2], U_Ap3[2]]
dec_beta = calcola_decimali_colonna(u_beta_list, 2)

u_gamma_list = [U_Ap[3], U_Ap1[3], U_Ap2[3], U_Ap3[3]]
dec_gamma = calcola_decimali_colonna(u_gamma_list, 2)

u_gammam_list = [u_gmp1, u_gmp2, u_gmp3]
dec_gammam = calcola_decimali_colonna(u_gammam_list, 2)


data = [
    [
        dist[0],
        formatta_cella(Ap[0][0], U_Ap[0], dec_tau),
        formatta_cella(Ap[1][0], U_Ap[1], dec_omega),
        formatta_cella(Ap[2][0], U_Ap[2], dec_beta),
        formatta_cella(Ap[3][0], U_Ap[3], dec_gamma),
        '-'
    ],
    [
        dist[1],
        formatta_cella(Ap1[0][0], U_Ap1[0], dec_tau),
        formatta_cella(Ap1[1][0], U_Ap1[1], dec_omega),
        formatta_cella(Ap1[2][0], U_Ap1[2], dec_beta),
        formatta_cella(Ap1[3][0], U_Ap1[3], dec_gamma),
        formatta_cella(Ap1[3][0] - Ap[3][0], u_gmp1, dec_gammam)
    ],
    [
        dist[2],
        formatta_cella(Ap2[0][0], U_Ap2[0], dec_tau),
        formatta_cella(Ap2[1][0], U_Ap2[1], dec_omega),
        formatta_cella(Ap2[2][0], U_Ap2[2], dec_beta),
        formatta_cella(Ap2[3][0], U_Ap2[3], dec_gamma),
        formatta_cella(Ap2[3][0] - Ap[3][0], u_gmp2, dec_gammam)
    ],
    [
        dist[3],
        formatta_cella(Ap3[0][0], U_Ap3[0], dec_tau),
        formatta_cella(Ap3[1][0], U_Ap3[1], dec_omega),
        formatta_cella(Ap3[2][0], U_Ap3[2], dec_beta),
        formatta_cella(Ap3[3][0], U_Ap3[3], dec_gamma),
        formatta_cella(Ap3[3][0] - Ap[3][0], u_gmp3, dec_gammam)
    ]
]


fig, ax = plt.subplots(figsize=(8, 1.5))
ax.axis('off')

tabella = ax.table(
    cellText=data,          
    colLabels=col,   
    loc='center',           
    cellLoc='center'        
)

# Modifica delle proprietà DOPO aver creato la tabella
# Usato 'col_idx' per non sovrascrivere la variabile globale 'col'
for (row, col_idx), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')

# Ottimizzazione e salvataggio
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'lastra_pettine.pgf'))
plt.close()








# 1. Lastra piena senza B
u = np.full(len(noB_fessurato[2]), u_a)
Ap, U_Ap = fitting(noB_fessurato, u)
U_Ap = np.diag(U_Ap)

# 2. Lastra piena con B1
u = np.full(len(B1_fessurato[2]), u_a)
Ap1, U_Ap1 = fitting(B1_fessurato, u)
U_Ap1 = np.diag(U_Ap1)
u_gmp1 = np.sqrt(U_Ap1[3]**2 + U_Ap[3]**2)

# 3. Lastra piena con B2
u = np.full(len(B2_fessurato[2]), u_a)
Ap2, U_Ap2 = fitting(B2_fessurato, u)
U_Ap2 = np.diag(U_Ap2)
u_gmp2 = np.sqrt(U_Ap2[3]**2 + U_Ap[3]**2)

# 4. Lastra piena con B3
u = np.full(len(B3_fessurato[2]), u_a)
Ap3, U_Ap3 = fitting(B3_fessurato, u)
U_Ap3 = np.diag(U_Ap3)
u_gmp3 = np.sqrt(U_Ap3[3]**2 + U_Ap[3]**2)



u_tau_list = [U_Ap[0], U_Ap1[0], U_Ap2[0], U_Ap3[0]]
dec_tau = calcola_decimali_colonna(u_tau_list, 2)

u_omega_list = [U_Ap[1], U_Ap1[1], U_Ap2[1], U_Ap3[1]]
dec_omega = calcola_decimali_colonna(u_omega_list, 2)

u_beta_list = [U_Ap[2], U_Ap1[2], U_Ap2[2], U_Ap3[2]]
dec_beta = calcola_decimali_colonna(u_beta_list, 2)

u_gamma_list = [U_Ap[3], U_Ap1[3], U_Ap2[3], U_Ap3[3]]
dec_gamma = calcola_decimali_colonna(u_gamma_list, 2)

u_gammam_list = [u_gmp1, u_gmp2, u_gmp3]
dec_gammam = calcola_decimali_colonna(u_gammam_list, 2)


data = [
    [
        dist[0],
        formatta_cella(Ap[0][0], U_Ap[0], dec_tau),
        formatta_cella(Ap[1][0], U_Ap[1], dec_omega),
        formatta_cella(Ap[2][0], U_Ap[2], dec_beta),
        formatta_cella(Ap[3][0], U_Ap[3], dec_gamma),
        '-'
    ],
    [
        dist[1],
        formatta_cella(Ap1[0][0], U_Ap1[0], dec_tau),
        formatta_cella(Ap1[1][0], U_Ap1[1], dec_omega),
        formatta_cella(Ap1[2][0], U_Ap1[2], dec_beta),
        formatta_cella(Ap1[3][0], U_Ap1[3], dec_gamma),
        formatta_cella(Ap1[3][0] - Ap[3][0], u_gmp1, dec_gammam)
    ],
    [
        dist[2],
        formatta_cella(Ap2[0][0], U_Ap2[0], dec_tau),
        formatta_cella(Ap2[1][0], U_Ap2[1], dec_omega),
        formatta_cella(Ap2[2][0], U_Ap2[2], dec_beta),
        formatta_cella(Ap2[3][0], U_Ap2[3], dec_gamma),
        formatta_cella(Ap2[3][0] - Ap[3][0], u_gmp2, dec_gammam)
    ],
    [
        dist[3],
        formatta_cella(Ap3[0][0], U_Ap3[0], dec_tau),
        formatta_cella(Ap3[1][0], U_Ap3[1], dec_omega),
        formatta_cella(Ap3[2][0], U_Ap3[2], dec_beta),
        formatta_cella(Ap3[3][0], U_Ap3[3], dec_gamma),
        formatta_cella(Ap3[3][0] - Ap[3][0], u_gmp3, dec_gammam)
    ]
]


fig, ax = plt.subplots(figsize=(8, 1.5))
ax.axis('off')

tabella = ax.table(
    cellText=data,          
    colLabels=col,   
    loc='center',           
    cellLoc='center'        
)

# Modifica delle proprietà DOPO aver creato la tabella
# Usato 'col_idx' per non sovrascrivere la variabile globale 'col'
for (row, col_idx), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')

# Ottimizzazione e salvataggio
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'lastra_fessurata.pgf'))
plt.close()



#faccio il fitting per lastra pettine senza B
u = np.full(len(noB_pettine[2]), u_a)
Ape, U_Ape = fitting(noB_pettine, u)
U_Ape = np.diag(U_Ape)
print('LASTRA A PETTINE SENZA B')
print(f'tau_0 = {Ape[0][0]}±{U_Ape[0]}')
print(f'omega_0^2 = {Ape[1][0]}±{U_Ape[1]}')
print(f'beta = {Ape[2][0]}±{U_Ape[2]}')
print(f'gamma (=gamma_a) = {Ape[3][0]}±{U_Ape[3]}')
print('\n')

#faccio il fitting per lastra fessurata senza B
u = np.full(len(noB_fessurato[2]), u_a)
Af, U_Af = fitting(noB_fessurato, u)
U_Af = np.diag(U_Af)
print('LASTRA FESSURATA SENZA B')
print(f'tau_0 = {Af[0][0]}±{U_Af[0]}')
print(f'omega_0^2 = {Af[1][0]}±{U_Af[1]}')
print(f'beta = {Af[2][0]}±{U_Af[2]}')
print(f'gamma (=gamma_a) = {Af[3][0]}±{U_Af[3]}')
print('\n')







#faccio il fitting per lastra pettine con B1
u = np.full(len(B1_pettine[2]), u_a)
Ape1, U_Ape1 = fitting(B1_pettine, u)
U_Ape1 = np.diag(U_Ape1)
u_gmpe1 = np.sqrt(U_Ape1[3]**2+U_Ape[3]**2)
print('LASTRA A PETTINE CON B1')
print(f'tau_0 = {Ape1[0][0]}±{U_Ape1[0]}')
print(f'omega_0^2 = {Ape1[1][0]}±{U_Ape1[1]}')
print(f'beta = {Ape1[2][0]}±{U_Ape1[2]}')
print(f'gamma = {Ape1[3][0]}±{U_Ape1[3]}')
print(f'gamma_m = {Ape1[3][0]-Ape[3][0]}±{u_gmpe1}')
print('\n')

#faccio il fitting per lastra fessurata con B1
u = np.full(len(B1_fessurato[2]), u_a)
Af1, U_Af1 = fitting(B1_fessurato, u)
U_Af1 = np.diag(U_Af1)
u_gmf1 = np.sqrt(U_Af1[3]**2+U_Af[3]**2)
print('LASTRA FESSURATA CON B1')
print(f'tau_0 = {Af1[0][0]}±{U_Af1[0]}')
print(f'omega_0^2 = {Af1[1][0]}±{U_Af1[1]}')
print(f'beta = {Af1[2][0]}±{U_Af1[2]}')
print(f'gamma = {Af1[3][0]}±{U_Af1[3]}')
print(f'gamma_m = {Af1[3][0]-Af[3][0]}±{u_gmf1}')
print('\n')







#faccio il fitting per lastra pettine con B2
u = np.full(len(B2_pettine[2]), u_a)
Ape2, U_Ape2 = fitting(B2_pettine, u)
U_Ape2 = np.diag(U_Ape2)
u_gmpe2 = np.sqrt(U_Ape2[3]**2+U_Ape[3]**2)
print('LASTRA A PETTINE CON B2')
print(f'tau_0 = {Ape2[0][0]}±{U_Ape2[0]}')
print(f'omega_0^2 = {Ape2[1][0]}±{U_Ape2[1]}')
print(f'beta = {Ape2[2][0]}±{U_Ape2[2]}')
print(f'gamma = {Ape2[3][0]}±{U_Ape2[3]}')
print(f'gamma_m = {Ape2[3][0]-Ape[3][0]}±{u_gmpe2}')
print('\n')

#faccio il fitting per lastra fessurata con B2
u = np.full(len(B2_fessurato[2]), u_a)
Af2, U_Af2 = fitting(B2_fessurato, u)
U_Af2 = np.diag(U_Af2)
u_gmf2 = np.sqrt(U_Af2[3]**2+U_Af[3]**2)
print('LASTRA FESSURATA CON B2')
print(f'tau_0 = {Af2[0][0]}±{U_Af2[0]}')
print(f'omega_0^2 = {Af2[1][0]}±{U_Af2[1]}')
print(f'beta = {Af2[2][0]}±{U_Af2[2]}')
print(f'gamma = {Af2[3][0]}±{U_Af2[3]}')
print(f'gamma_m = {Af2[3][0]-Af[3][0]}±{u_gmf2}')
print('\n')







#faccio il fitting per lastra pettine con B3
u = np.full(len(B3_pettine[2]), u_a)
Ape3, U_Ape3 = fitting(B3_pettine, u)
U_Ape3 = np.diag(U_Ape3)
u_gmpe3 = np.sqrt(U_Ape3[3]**2+U_Ape[3]**2)
print('LASTRA A PETTINE CON B3')
print(f'tau_0 = {Ape3[0][0]}±{U_Ape3[0]}')
print(f'omega_0^2 = {Ape3[1][0]}±{U_Ape3[1]}')
print(f'beta = {Ape3[2][0]}±{U_Ape3[2]}')
print(f'gamma = {Ape3[3][0]}±{U_Ape3[3]}')
print(f'gamma_m = {Ape3[3][0]-Ape[3][0]}±{u_gmpe3}')
print('\n')

#faccio il fitting per lastra fessurata con B3
u = np.full(len(B3_fessurato[2]), u_a)
Af3, U_Af3 = fitting(B3_fessurato, u)
U_Af3 = np.diag(U_Af3)
u_gmf3 = np.sqrt(U_Af3[3]**2+U_Af[3]**2)
print('LASTRA FESSURATA CON B3')
print(f'tau_0 = {Af3[0][0]}±{U_Af3[0]}')
print(f'omega_0^2 = {Af3[1][0]}±{U_Af3[1]}')
print(f'beta = {Af3[2][0]}±{U_Af3[2]}')
print(f'gamma = {Af3[3][0]}±{U_Af3[3]}')
print(f'gamma_m = {Af3[3][0]-Af[3][0]}±{u_gmf3}')
print('\n')