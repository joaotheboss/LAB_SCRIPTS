import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import odr
from scipy import stats
import math
import matplotlib
import os
OUTPUT_DIR = r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\espII_13_04"


matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

def comma_to_float(s):
    return float(s.replace(',', '.'))

def comma_to_float_lengths(s):
    return 0.01*float(s.replace(',', '.'))

def determina_decimali_colonna(u_vettore, n=1):
    # Prendiamo il valore minimo non nullo per garantire la massima precisione necessaria
    u_min = np.min(u_vettore[u_vettore > 0])
    prima_cifra = int(np.floor(np.log10(abs(u_min))))
    return max(0, -prima_cifra + (n - 1))

def format_misura(x, u_x, n=1):
    # 1. Trova la posizione della prima cifra significativa
    prima_cifra = int(np.floor(np.log10(abs(u_x))))
    
    # 2. Calcola quanti decimali servono per averne 'n' significative
    # Se il risultato è negativo (es. incertezza sulle centinaia), usiamo 0 decimali
    decimali = max(0, -prima_cifra + (n - 1))
    
    # 3. Restituisce la stringa formattata
    return f"{x:.{decimali}f}±{u_x:.{decimali}f}"

u_x = 0.001/np.sqrt(6)

def thickness_measure(thick, eq=False):

	#MISURA SPESSORE
	#u2_instr = ((0.00005)**2)/12
	#per spessore dei fili 2 opzioni:
	#- valori diversi: media e propagazione
	#- valori simili: u_strumento
	n = len(thick)
	u2_instr = ((0.00005)**2)/12
	if eq == False:
		s = np.mean(thick)
		u2_s = 1/(n*(n-1))*np.sum((thick-s)**2)
		u = np.sqrt(u2_s+u2_instr)
	else:
		s = np.median(thick)
		u = np.sqrt(u2_instr)
	return s, u

def measurement_4everyl(meas_s, g, tension=False):
	#accuratezza corrente: 1% + 61e-6
	#accuratezza tensione: 1% + 0.0025/g con g guadagno
	to_Add = 61e-6
	if tension == True: to_Add = 0.0025/g
	#per le u_str si ha u_str = acc/sqrt(3)
	m, u_m = [], []
	for meas in meas_s:
		mu = np.mean(meas)
		m.append(mu)

		n = len(meas)
		u = np.sqrt(1/(n*(n-1))*np.sum((meas-mu)**2)+((0.01*mu+to_Add)**2)/3)
		u_m.append(u)
	return np.array(m), np.array(u_m)

def R_compute(V, I, u_v, u_i):
	R = V/I
	#u_r = sqrt(u_i^2 * V/I^2 + u_v^2 * 1/I)
	u_R = np.sqrt((u_i**2)*V/(I**2) + (u_v**2)*1/I)
	return R, u_R

def ohm(x, b):
	y = b*x
	return y

def ohm_odr(B, x):
	y = B[0]*x
	return y

def no_ux_fit(y, u_y, x):
	return optimize.curve_fit(ohm, x, y, sigma=u_y, absolute_sigma = True)

def ux_fit(y, u_y, x, u_x):
	odr_ohm = odr.Model(ohm_odr)
	w_x, w_y = 1/(u_x**2), 1/(u_y**2)
	data = odr.Data(x, y, w_x, w_y)
	odr_ob = odr.ODR(data, odr_ohm, [1])
	return odr_ob.run().beta, odr_ob.run().sd_beta


t1, b1 = np.array([0.9, 0.8, 0.8, 0.8, 0.8, 0.8])/1000, True ##
t2, b2 = np.array([0.9, 0.9, 0.9, 0.85, 0.8, 0.85])/1000, False
t3, b3 = np.array([0.8, 0.8, 0.85, 0.85, 0.85, 0.85])/1000, False
t4, b4 = np.array([0.3, 0.3, 0.35, 0.3, 0.4, 0.3])/1000, False
#NON CANCELLARE QUESTI SONO GLI UNICI DATI CHE HAI
#t5, b5 = np.array([0.95, 0.95, 0.95, 0.95, 0.95, 0.95]), True ##
#t6, b6 = np.array([1.1, 1.1, 1.1, 1.1, 1.1, 1.1]), True ##
#t7, b7 = np.array([0.7, 0.65, 0.7, 0.65, 0.65, 0.65]), False
#t8, b8 = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.85]), True ##

#calcolo spessore e sezione di ogni filo
t_1, u_1 = thickness_measure(t1, b1)
print(f'Diametro filo 1: {format_misura(t_1, u_1)}')
t_2, u_2 = thickness_measure(t2, b2)
print(f'Diametro filo 2: {format_misura(t_2, u_2)}')
t_3, u_3 = thickness_measure(t3, b3)
print(f'Diametro filo 3: {format_misura(t_3, u_3)}')
t_4, u_4 = thickness_measure(t4, b4)
print(f'Diametro filo 4: {format_misura(t_4, u_4)}')
a_1, u_a1 = (t_1**2)*np.pi/4, 2*t_1*np.pi/4*u_1
print(f'Sezione filo 1: {format_misura(a_1, u_a1)}')
a_2, u_a2 = (t_2**2)*np.pi/4, 2*t_2*np.pi/4*u_2
print(f'Sezione filo 2: {format_misura(a_2, u_a2)}')
a_3, u_a3 = (t_3**2)*np.pi/4, 2*t_3*np.pi/4*u_3
print(f'Sezione filo 3: {format_misura(a_3, u_a3)}')
a_4, u_a4 = (t_4**2)*np.pi/4, 2*t_4*np.pi/4*u_4
print(f'Sezione filo 4: {format_misura(a_4, u_a4)}')
#print(f'{t_1}+-{u_1}\n', f'{t_2}+-{u_2}\n', f'{t_3}+-{u_3}\n', f'{t_4}+-{u_4}\n')
col_fili = ['Barretta', 'Diametro (m)', 'Sezione (m^2)']
data =[ ['1', format_misura(t_1, u_1), format_misura(a_1, u_a1)], ['2', format_misura(t_2, u_2), format_misura(a_2, u_a2)],
	   ['3', format_misura(t_3, u_3), format_misura(a_3, u_a3)], ['4', format_misura(t_4, u_4), format_misura(a_4, u_a4)],]
fig, ax = plt.subplots(figsize=(6.5, 1.5))  # Senza figsize
ax.axis('off')

tabella = ax.table(
    cellText=data,          
    colLabels=col_fili,   
    loc='center',           
    cellLoc='center'        
)

for (row, col), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')
# Prima avevi: plt.savefig('valori_fili.pgf')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'valori_fili.pgf'))
plt.close() # <-- Importante chiuderlo!


#qui mi sono preso i dati dai file
#prima, settima, nona
r_1 = np.genfromtxt(
	r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\espII_13_04\filo1.csv", 
	delimiter=';', skip_header=1, usecols=(0, 6, 8),
    converters={
        0: comma_to_float_lengths,
        6: comma_to_float, 
        8: comma_to_float 
    }
)


r_2 = np.genfromtxt(
	r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\espII_13_04\filo2.csv", 
	delimiter=';', skip_header=1, usecols=(0, 2, 4),
    converters={
        0: comma_to_float_lengths,
        2: comma_to_float, 
        4: comma_to_float 
    }
)

r_3 = np.genfromtxt(
	r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\espII_13_04\filo3.csv", 
	delimiter=';', skip_header=1, usecols=(0, 2, 4),
    converters={
        0: comma_to_float_lengths,
        2: comma_to_float, 
        4: comma_to_float 
    }
)

r_4 = np.genfromtxt(
	r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\espII_13_04\filo4.csv", 
	delimiter=';', skip_header=1, usecols=(0, 2, 4),
    converters={
        0: comma_to_float_lengths,
        2: comma_to_float, 
        4: comma_to_float 
    }
)

#abbiamo fatto 10 misurazioni per ciascuna delle 11 lunghezze = 110
r_1, r_2, r_3, r_4 = r_1[:110], r_2[:110], r_3[:110], r_4[:110]
#isolo le lunghezze in x
#le x hanno incertezza standard u_x (vedi inizio)
x = [r_1[i][0] for i in range(0,101,10)]
#divido le tensioni e le correnti associate a ciascuna lunghezza per ogni filo
V_1 = [[r_1[i][1] for i in range(j*10, (j+1)*10)] for j in range(11)]
I_1 = [[r_1[i][2] for i in range(j*10, (j+1)*10)] for j in range(11)]
V_2 = [[r_2[i][1] for i in range(j*10, (j+1)*10)] for j in range(11)]
I_2 = [[r_2[i][2] for i in range(j*10, (j+1)*10)] for j in range(11)]
V_3 = [[r_3[i][1] for i in range(j*10, (j+1)*10)] for j in range(11)]
I_3 = [[r_3[i][2] for i in range(j*10, (j+1)*10)] for j in range(11)]
V_4 = [[r_4[i][1] for i in range(j*10, (j+1)*10)] for j in range(11)]
I_4 = [[r_4[i][2] for i in range(j*10, (j+1)*10)] for j in range(11)]

#adesso faccio tutti i conti che mi servono
V_1, u_v1 = measurement_4everyl(V_1, 10, True)
for v,u in zip(V_1, u_v1): print(f'Tensione filo 1: {v}±{u}')
I_1, u_i1 = measurement_4everyl(I_1, 10)
for i,u in zip(I_1, u_i1): print(f'Corrente filo 1: {i}±{u}')
V_2, u_v2 = measurement_4everyl(V_2, 10, True)
for v,u in zip(V_2, u_v2): print(f'Tensione filo 2: {v}±{u}')
I_2, u_i2 = measurement_4everyl(I_2, 10)
for i,u in zip(I_2, u_i2): print(f'Corrente filo 2: {i}±{u}')
V_3, u_v3 = measurement_4everyl(V_3, 10, True)
for v,u in zip(V_3, u_v3): print(f'Tensione filo 3: {v}±{u}')
I_3, u_i3 = measurement_4everyl(I_3, 10)
for i,u in zip(I_3, u_i3): print(f'Corrente filo 3: {i}±{u}')
V_4, u_v4 = measurement_4everyl(V_4, 10, True)
for v,u in zip(V_4, u_v4): print(f'Tensione filo 4: {v}±{u}')
I_4, u_i4 = measurement_4everyl(I_4, 10)
for i,u in zip(I_4, u_i4): print(f'Corrente filo 4: {i}±{u}')

#stimo le resistenze
col_fili = ['Lunghezza (m)', r'Resistenze barretta 1 ($\Omega$)',r'Resistenze barretta 2 ($\Omega$)',r'Resistenze barretta 3 ($\Omega$)', r'Resistenze barretta 4 ($\Omega$)']
data =[]



R_1, u_R1 = R_compute(V_1, I_1, u_v1, u_i1)
for r,u in zip(R_1, u_R1): print(f'Resistenza filo 1: {r}±{u}')
R_2, u_R2 = R_compute(V_2, I_2, u_v2, u_i2)
for r,u in zip(R_2, u_R2): print(f'Resistenza filo 2: {r}±{u}')
R_3, u_R3 = R_compute(V_3, I_3, u_v3, u_i3)
for r,u in zip(R_3, u_R3): print(f'Resistenza filo 3: {r}±{u}')
R_4, u_R4 = R_compute(V_4, I_4, u_v4, u_i4)
for r,u in zip(R_4, u_R4): print(f'Resistenza filo 4: {r}±{u}')

dec_R1 = determina_decimali_colonna(u_R1, n=1)
dec_V1 = determina_decimali_colonna(u_v1, n=1)
dec_I1 = determina_decimali_colonna(u_i1, n=1)
dec_R2 = determina_decimali_colonna(u_R2, n=1)
dec_V2 = determina_decimali_colonna(u_v2, n=1)
dec_I2 = determina_decimali_colonna(u_i2, n=1)
dec_R3 = determina_decimali_colonna(u_R3, n=1)
dec_V3 = determina_decimali_colonna(u_v3, n=1)
dec_I3 = determina_decimali_colonna(u_i3, n=1)
dec_R4 = determina_decimali_colonna(u_R4, n=1)
dec_V4 = determina_decimali_colonna(u_v4, n=1)
dec_I4 = determina_decimali_colonna(u_i4, n=1)

# Se preferisci che TUTTE le colonne di tutta la tabella abbiano lo stesso numero 
# di decimali (es. 4 decimali per tutti), puoi forzarlo scommentando la riga sotto:
# dec_1 = dec_2 = dec_3 = dec_4 = 4

# 3. Formattiamo le colonne usando i rispettivi decimali fissi
str_R1 = [f"{r:.{dec_R1}f}±{u:.{dec_R1}f}" for r, u in zip(R_1, u_R1)]
str_V1 = [f"{r:.{dec_V1}f}±{u:.{dec_V1}f}" for r, u in zip(V_1, u_v1)]
str_I1 = [f"{r:.{dec_I1}f}±{u:.{dec_I1}f}" for r, u in zip(I_1, u_i1)]
str_R2 = [f"{r:.{dec_R2}f}±{u:.{dec_R2}f}" for r, u in zip(R_2, u_R2)]
str_V2 = [f"{r:.{dec_V2}f}±{u:.{dec_V2}f}" for r, u in zip(V_2, u_v2)]
str_I2 = [f"{r:.{dec_I2}f}±{u:.{dec_I2}f}" for r, u in zip(I_2, u_i2)]
str_R3 = [f"{r:.{dec_R3}f}±{u:.{dec_R3}f}" for r, u in zip(R_3, u_R3)]
str_V3 = [f"{r:.{dec_V3}f}±{u:.{dec_V3}f}" for r, u in zip(V_3, u_v3)]
str_I3 = [f"{r:.{dec_I3}f}±{u:.{dec_I3}f}" for r, u in zip(I_3, u_i3)]
str_R4 = [f"{r:.{dec_R4}f}±{u:.{dec_R4}f}" for r, u in zip(R_4, u_R4)]
str_V4 = [f"{r:.{dec_V4}f}±{u:.{dec_V4}f}" for r, u in zip(V_4, u_v4)]
str_I4 = [f"{r:.{dec_I4}f}±{u:.{dec_I4}f}" for r, u in zip(I_4, u_i4)]
str_x = [format_misura(c, u_x) for c in x]

# 3. Trasformiamo le colonne in RIGHE per matplotlib usando zip
# data sarà una lista del tipo: [[R1_mis1, R2_mis1, R3_mis1, R4_mis1], [R1_mis2, ...]]

data = list(zip(str_x,str_R1,str_R2, str_R3, str_R4))

# 4. Disegniamo la tabella
fig, ax = plt.subplots(figsize=(6.5, 2.5))
ax.axis('off')

tabella = ax.table(
    cellText=data,          
    colLabels=col_fili,   
    loc='center',           
    cellLoc='center'        
)
#for i in range(len(col_fili)): tabella.auto_set_column_width(i)

for (row, col), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')
# Prima avevi: plt.savefig('valori_fili.pgf')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'resistenze_fili.pgf'))
plt.close() # <-- Importante chiuderlo!

col_fili = ['Lunghezza (m)', 'V barr. 1 (V)', 'I barr. 1 (A)','V barr. 2 (V)', 'I barr. 2 (A)','V barr. 3 (V)', 'I barr. 3 (A)','V barr. 4 (V)', 'I barr. 4 (A)']

data = list(zip(str_x,str_V1, str_I1, str_V2, str_I2,str_V3,  str_I3,str_V4, str_I4))
fig, ax = plt.subplots(figsize=(6.5, 2.5))
ax.axis('off')

tabella = ax.table(
    cellText=data,          
    colLabels=col_fili,   
    loc='center',           
    cellLoc='center'        
)
#for i in range(len(col_fili)): tabella.auto_set_column_width(i)

for (row, col), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')
# Prima avevi: plt.savefig('valori_fili.pgf')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'VI_fili.pgf'))
plt.close() # <-- Importante chiuderlo!


def no_unc (R_1, u_R1, x1, R_2, u_R2, x2, R_3, u_R3, x3, R_4, u_R4, x4):
	
	col_fili = [r'Resistività filo 1 ($\Omega$m)', r'Resistività filo 2 ($\Omega$m)', r'Resistività filo 3 ($\Omega$m)', r'Resistività filo 4 ($\Omega$m)']
	data = [[]]
	fig, ax = plt.subplots(figsize=(6.5, 1.0))  # Senza figsize
	ax.axis('off')

	fig_g = plt.figure(2)
	plt.suptitle("Fit")
	print("Fit")
	rho1, cov_rho1 = no_ux_fit(R_1, u_R1, x1)
	data[0].append(format_misura(rho1[0], np.sqrt(cov_rho1[0][0]), 2))
	plt.subplot(2, 2, 1)
	plt.plot(x1, ohm(x1, rho1[0]), '-o')
	plt.title(fr'rho = {format_misura(rho1[0], np.sqrt(cov_rho1[0][0]), 2)} $\Omega$m')
	plt.xlabel('L/A (1/m)')
	plt.ylabel(r'R ($\Omega$)')
	print(f'rho1 = {rho1[0]}±{np.sqrt(cov_rho1[0][0])}')
	residues = R_1 - ohm(x1, rho1[0])
	#faccio il test del chi quadro
	chi_2 = np.sum(residues**2/u_R1**2)
	#posso calcolare chi critico
	alpha = 0.05
	freedom_degrees = len(R_1)-2
	crit_chi_2 = stats.chi2.ppf(1-alpha, df = freedom_degrees)
	print(chi_2/freedom_degrees, crit_chi_2/freedom_degrees)


	rho2, cov_rho2 = no_ux_fit(R_2, u_R2, x2)
	data[0].append(format_misura(rho2[0], np.sqrt(cov_rho2[0][0]), 2))
	plt.subplot(2, 2, 2)
	plt.plot(x2, ohm(x2, rho2[0]), '-o')
	plt.title(fr'rho = {format_misura(rho2[0], np.sqrt(cov_rho2[0][0]), 2)} $\Omega$m')
	plt.xlabel('L/A (1/m)')
	plt.ylabel(r'R ($\Omega$)')
	print(f'rho2 = {rho2[0]}±{np.sqrt(cov_rho2[0][0])}')
	residues = R_2 - ohm(x2, rho2[0])
	#faccio il test del chi quadro
	chi_2 = np.sum(residues**2/u_R2**2)
	#posso calcolare chi critico
	alpha = 0.05
	freedom_degrees = len(R_2)-2
	crit_chi_2 = stats.chi2.ppf(1-alpha, df = freedom_degrees)
	print(chi_2/freedom_degrees, crit_chi_2/freedom_degrees)


	rho3, cov_rho3 = no_ux_fit(R_3, u_R3, x3)
	data[0].append(format_misura(rho3[0], np.sqrt(cov_rho3[0][0]), 2))
	plt.subplot(2, 2, 3)
	plt.plot(x3, ohm(x3, rho3[0]), '-o')
	plt.title(fr'rho = {format_misura(rho3[0], np.sqrt(cov_rho3[0][0]), 2)} $\Omega$m')
	plt.xlabel('L/A (1/m)')
	plt.ylabel(r'R ($\Omega$)')
	print(f'rho3 = {rho3[0]}±{np.sqrt(cov_rho3[0][0])}')
	residues = R_3 - ohm(x3, rho3[0])
	#faccio il test del chi quadro
	chi_2 = np.sum(residues**2/u_R3**2)
	#posso calcolare chi critico
	alpha = 0.05
	freedom_degrees = len(R_3)-2
	crit_chi_2 = stats.chi2.ppf(1-alpha, df = freedom_degrees)
	print(chi_2/freedom_degrees, crit_chi_2/freedom_degrees)


	rho4, cov_rho4 = no_ux_fit(R_4, u_R4, x4)
	data[0].append(format_misura(rho4[0], np.sqrt(cov_rho4[0][0]), 2))
	plt.subplot(2, 2, 4)
	plt.plot(x4, ohm(x4, rho4[0]), '-o')
	plt.title(fr'rho = {format_misura(rho4[0], np.sqrt(cov_rho4[0][0]), 2)} $\Omega$m')
	plt.xlabel('L/A (1/m)')
	plt.ylabel(r'R ($\Omega$)')
	print(f'rho4 = {rho4[0]}±{np.sqrt(cov_rho4[0][0])}')
	residues = R_4 - ohm(x4, rho4[0])
	#faccio il test del chi quadro
	chi_2 = np.sum(residues**2/u_R4**2)
	#posso calcolare chi critico
	alpha = 0.05
	freedom_degrees = len(R_4)-2
	crit_chi_2 = stats.chi2.ppf(1-alpha, df = freedom_degrees)
	print(chi_2/freedom_degrees, crit_chi_2/freedom_degrees)

	tabella = ax.table(
		cellText=data,          
		colLabels=col_fili,   
		loc='center',           
		cellLoc='center'        
	)

	for (row, col), cell in tabella.get_celld().items():
		if row == 0:
			cell.set_text_props(weight='bold')
	# Prima avevi: plt.savefig('valori_fili.pgf')
	plt.tight_layout()
	fig.savefig(os.path.join(OUTPUT_DIR, 'valori_rho.pgf'))
	fig_g.savefig(os.path.join(OUTPUT_DIR, 'grafici_rho.pgf'))
	plt.close() # <-- Importante chiuderlo!




def yes_unc(R_1, u_R1, x1, u_x1, R_2, u_R2, x2, u_x2, R_3, u_R3, x3, u_x3, R_4, u_R4, x4, u_x4):
	col_fili = [r'Resistività filo 1 ($\Omega$m)', r'Resistività filo 2 ($\Omega$m)', r'Resistività filo 3 ($\Omega$m)', r'Resistività filo 4 ($\Omega$m)']
	data = [[]]
	fig, ax = plt.subplots()  # Senza figsize
	ax.axis('off')

	fig_g = plt.figure(2)
	plt.suptitle("ODR fit")
	print("ODR fit")
	rho1, s_rho1 = ux_fit(R_1, u_R1, x1, u_x1)
	data[0].append(format_misura(rho1[0], s_rho1[0], 2))
	plt.subplot(2, 2, 1)
	plt.plot(x1, ohm(x1, rho1[0]), '-o')
	plt.title(fr'rho = {format_misura(rho1[0], s_rho1[0], 2)} $\Omega$m')
	plt.xlabel('L/A (1/m)')
	plt.ylabel(r'R ($\Omega$)')
	print(f'rho1 = {rho1[0]}±{s_rho1[0]}')
	residues = R_1 - ohm(x1, rho1[0])
	#faccio il test del chi quadro
	chi_2 = np.sum(residues**2/u_R1**2)
	#posso calcolare chi critico
	alpha = 0.05
	freedom_degrees = len(R_1)-2
	crit_chi_2 = stats.chi2.ppf(1-alpha, df = freedom_degrees)
	print(chi_2, crit_chi_2)


	rho2, s_rho2 = ux_fit(R_2, u_R2, x2, u_x2)
	data[0].append(format_misura(rho2[0], s_rho2[0], 2))
	plt.subplot(2, 2, 2)
	plt.plot(x2, ohm(x2, rho2[0]), '-o')
	plt.title(fr'rho = {format_misura(rho2[0], s_rho2[0], 2)} $\Omega$m')
	plt.xlabel('L/A (1/m)')
	plt.ylabel(r'R ($\Omega$)')
	print(f'rho2 = {rho2[0]}±{s_rho2[0]}')
	residues = R_2 - ohm(x2, rho2[0])
	#faccio il test del chi quadro
	chi_2 = np.sum(residues**2/u_R2**2)
	#posso calcolare chi critico
	alpha = 0.05
	freedom_degrees = len(R_2)-2
	crit_chi_2 = stats.chi2.ppf(1-alpha, df = freedom_degrees)
	print(chi_2, crit_chi_2)


	rho3, s_rho3 = ux_fit(R_3, u_R3, x3, u_x3)
	data[0].append(format_misura(rho3[0], s_rho3[0], 2))
	plt.subplot(2, 2, 3)
	plt.plot(x3, ohm(x3, rho3[0]), '-o')
	plt.title(fr'rho = {format_misura(rho3[0], s_rho3[0], 2)} $\Omega$m')
	plt.xlabel('L/A (1/m)')
	plt.ylabel(r'R ($\Omega$)')
	print(f'rho3 = {rho3[0]}±{s_rho3[0]}')
	residues = R_3 - ohm(x3, rho3[0])
	#faccio il test del chi quadro
	chi_2 = np.sum(residues**2/u_R3**2)
	#posso calcolare chi critico
	alpha = 0.05
	freedom_degrees = len(R_3)-2
	crit_chi_2 = stats.chi2.ppf(1-alpha, df = freedom_degrees)
	print(chi_2, crit_chi_2)


	rho4, s_rho4 = ux_fit(R_4, u_R4, x4, u_x4)
	data[0].append(format_misura(rho4[0], s_rho4[0], 2))
	plt.subplot(2, 2, 4)
	plt.plot(x4, ohm(x4, rho4[0]), '-o')
	plt.title(fr'rho = {format_misura(rho4[0], s_rho4[0], 2)} $\Omega$m')
	plt.xlabel('L/A (1/m)')
	plt.ylabel(r'R ($\Omega$)')
	print(f'rho4 = {rho4[0]}±{s_rho4[0]}')
	residues = R_4 - ohm(x4, rho4[0])
	#faccio il test del chi quadro
	chi_2 = np.sum(residues**2/u_R4**2)
	#posso calcolare chi critico
	alpha = 0.05
	freedom_degrees = len(R_4)-2
	crit_chi_2 = stats.chi2.ppf(1-alpha, df = freedom_degrees)
	print(chi_2, crit_chi_2)

	tabella = ax.table(
		cellText=data,          
		colLabels=col_fili,   
		loc='center',           
		cellLoc='center'        
	)

	for (row, col), cell in tabella.get_celld().items():
		if row == 0:
			cell.set_text_props(weight='bold')
	# Prima avevi: plt.savefig('valori_fili.pgf')
	plt.tight_layout()
	fig.savefig(os.path.join(OUTPUT_DIR, 'valori_rho.pgf'))
	fig_g.savefig(os.path.join(OUTPUT_DIR, 'grafici_rho.pgf'))
	plt.close() # <-- Importante chiuderlo!



#nel fit ci saranno gli xi = x/ai (i indice), quindi calcolo le incertezze
# roba = lunghezza/area
# u_roba ^2 = (lunghezza/area^2)^2 * u_area^2 + (1/area)^2 * (u_lunghezza)^2
u_x1 = np.sqrt(((x/(a_1**2))**2)*(u_a1**2)+((1/a_1)**2)*(u_x**2))
u_x2 = np.sqrt(((x/(a_2**2))**2)*(u_a2**2)+((1/a_2)**2)*(u_x**2))
u_x3 = np.sqrt(((x/(a_3**2))**2)*(u_a3**2)+((1/a_3)**2)*(u_x**2))
u_x4 = np.sqrt(((x/(a_4**2))**2)*(u_a4**2)+((1/a_4)**2)*(u_x**2))
for l,u in zip(x, u_x1): print(f'Lunghezza/Sezione filo 1: {l/a_1}±{u}')
for l,u in zip(x, u_x2): print(f'Lunghezza/Sezione filo 2: {l/a_2}±{u}')
for l,u in zip(x, u_x3): print(f'Lunghezza/Sezione filo 3: {l/a_3}±{u}')
for l,u in zip(x, u_x4): print(f'Lunghezza/Sezione filo 4: {l/a_4}±{u}')

no_unc(R_1, u_R1, x/a_1, R_2, u_R2, x/a_2, R_3, u_R3, x/a_3, R_4, u_R4, x/a_4)
#yes_unc(R_1, u_R1, x/a_1, u_x1, R_2, u_R2, x/a_2, u_x2, R_3, u_R3, x/a_3, u_x3, R_4, u_R4, x/a_4, u_x4)