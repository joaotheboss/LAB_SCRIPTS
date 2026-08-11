import numpy as np
from scipy.optimize import least_squares
import matplotlib
import matplotlib.pyplot as plt
import os
# Definiamo la cartella corretta una volta sola
OUTPUT_DIR = r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\espII_25_05"

def format_misura(x, u_x, n=1):
    # 1. Trova la posizione della prima cifra significativa
    prima_cifra = int(np.floor(np.log10(abs(u_x))))
    
    # 2. Calcola quanti decimali servono per averne 'n' significative
    # Se il risultato è negativo (es. incertezza sulle centinaia), usiamo 0 decimali
    decimali = max(0, -prima_cifra + (n - 1))
    
    # 3. Restituisce la stringa formattata
    return f"{x:.{decimali}f}±{u_x:.{decimali}f}"

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

def fai_tabelle(p, up, q, uq, G, uG, f):
	col = [r'$p (m)$', r'$q (m)$', r'$G$']
	str_p = [format_misura(r,up) for r in p]
	str_q = [format_misura(r,u) for r,u in zip (q, uq)]
	str_G = [format_misura(r,u) for r,u in zip (G, uG)]
	data =list(zip(str_p, str_q, str_G))
	fig, ax = plt.subplots(figsize=(6, 2))  # Senza figsize
	ax.axis('off')

	tabella = ax.table(
		cellText=data,          
		colLabels=col,   
		loc='center',           
		cellLoc='center'        
	)

	for (row, col), cell in tabella.get_celld().items():
		if row == 0:
			cell.set_text_props(weight='bold')
	# Prima avevi: plt.savefig('valori_fili.pgf')
	plt.tight_layout()
	plt.savefig(os.path.join(OUTPUT_DIR, f'misure_lente{f}.pgf'))
	plt.close() # <-- Importante chiuderlo!


def dati_200():
	p = np.array([0.3, 0.605, 0.26, 0.865, 0.499, 0.399, 0.33]) #p fissato
	up = 0.001/np.sqrt(3)

	l_min = np.array([0.889, 0.900, 1.145, 1.125, 0.83, 0.798, 0.83]) #lunghezza sul metro del qmin +p
	l_max = np.array([0.943, 0.930, 1.164, 1.137, 0.852, 0.82, 0.86]) #lunghezza sul metro del qmax +p
	l = (l_min+l_max)/2

	q_min = l_min-p
	q_max = l_max-p
	q = (q_min+q_max)/2 #calcolo di q
	uq = (q_max-q_min)/np.sqrt(12)

	h1 = np.array([0.039, 0.02, 0.01, 0.04, 0.04, 0.04, 0.04]) #h prima di ingrandimento
	h2 = np.array([0.079, 0.01, 0.038, 0.014, 0.029, 0.042, 0.064]) #h ingrandito
	u_h = 0.001/np.sqrt(3) #incertezza di h
	G = -h2/h1 #ingrandimento, è ribaltato
	#Gh = h2/h1 -> u_gh = np.sqrt((u_h/h1)**2 + (u_h*h2/(h1**2))**2 )
	uG = np.sqrt((u_h/h1)**2 + (u_h*h2/(h1**2))**2 )
	fai_tabelle(p, up, q, uq, G, uG, 200)

def dati_100():
	p = np.array([0.135, 0.388, 0.374, 0.33, 0.28, 0.22, 0.16]) #p fissato
	up = 0.001/np.sqrt(3)

	l_min = np.array([0.515, 0.52, 0.503, 0.472, 0.433, 0.398, 0.411]) #lunghezza sul metro del qmin+p
	l_max = np.array([0.529, 0.53, 0.516, 0.479, 0.441, 0.407, 0.439]) #lunghezza sul metro del qmax+p
	l = (l_min+l_max)/2

	q_min = l_min-p
	q_max = l_max-p
	q = (q_min+q_max)/2 #calcolo di q
	uq = (q_max-q_min)/np.sqrt(12)

	h1 = np.array([0.039, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04 ]) #h prima di ingrandimento
	h2 = np.array([0.110, 0.017, 0.016, 0.02, 0.025, 0.036, 0.068 ]) #h ingrandito
	u_h = 0.001/np.sqrt(3) #incertezza di h
	G = -h2/h1 #ingrandimento, è ribaltato
	uG = np.sqrt((u_h/h1)**2 + (u_h*h2/(h1**2))**2 )
	fai_tabelle(p, up, q, uq, G, uG, 100)


def dati_2lenti():
	p  = np.array([0.130, 0.136, 0.140, 0.146, 0.150, 0.156, 0.160]) #posizione di ingresso
	up = 0.001/np.sqrt(3)

	d = 0.15 #distanza tra le lenti
	ud = 0.001/np.sqrt(3)

	q_max = np.array([0.121, 0.110, 0.103, 0.097, 0.087, 0.080, 0.078])
	q_min = np.array([0.115, 0.102, 0.099, 0.089, 0.083, 0.076, 0.072])
	q = (q_max+q_min)/2
	uq = (q_max-q_min)/np.sqrt(12)

	h1 = np.array([0.040, 0.040, 0.040, 0.040, 0.040, 0.040, 0.040])#h prima di ingrandimento
	h2 = np.array([0.055, 0.052, 0.051, 0.047, 0.046, 0.044, 0.041])#h ingrandito
	u_h1 = 0.001/np.sqrt(3) #incertezza di h1
	u_h2 = 0.001/np.sqrt(3) #incertezza di h2
	G = -h2/h1 #invertito
	uG = np.sqrt((u_h2/h1)**2 + (u_h1*h2/(h1**2))**2 )
	fai_tabelle(p, up, q, uq, G, uG, 2)


def d_focale_200(par):
	#LENTE CON DISTANZA FOCALE 200 mm
	p = np.array([0.3, 0.605, 0.26, 0.865, 0.499, 0.399, 0.33]) #p fissato
	up = 0.001/np.sqrt(3)

	l_min = np.array([0.889, 0.900, 1.145, 1.125, 0.83, 0.798, 0.83]) #lunghezza sul metro del qmin +p
	l_max = np.array([0.943, 0.930, 1.164, 1.137, 0.852, 0.82, 0.86]) #lunghezza sul metro del qmax +p
	l = (l_min+l_max)/2

	q_min = l_min-p
	q_max = l_max-p
	q = (q_min+q_max)/2 #calcolo di q
	uq = (q_max-q_min)/np.sqrt(12)

	h1 = np.array([0.039, 0.02, 0.01, 0.04, 0.04, 0.04, 0.04]) #h prima di ingrandimento
	h2 = np.array([0.079, 0.01, 0.038, 0.014, 0.029, 0.042, 0.064]) #h ingrandito
	u_h = 0.001/np.sqrt(3) #incertezza di h
	G = -h2/h1 #ingrandimento, è ribaltato
	#Gh = h2/h1 -> u_gh = np.sqrt((u_h/h1)**2 + (u_h*h2/(h1**2))**2 )
	uG = np.sqrt((u_h/h1)**2 + (u_h*h2/(h1**2))**2 )

	#setto dati per il fit
	A, B, C, D = par
	#calcolo R1
	Bs = A*p+B+C*p*q+D*q
	uBs = np.sqrt(((A+C*q)*up)**2+((D+C*p)*uq)**2)
	R1 = Bs/uBs

	#calcolo R2
	As = A+C*q
	uAs = np.sqrt((C*uq)**2)
	uAs_Gy = np.sqrt(uAs**2+uG**2)
	R2 = (As-G)/uAs_Gy

	#calcolo R3
	R3 = np.array([A*D-B*C-1])

	#costruisco vettore con tutti i residui
	Res = np.concatenate([R1, R2, R3])
	return Res


def d_focale_100(par):
	#LENTE CON DISTANZA FOCALE 100 mm
	p = np.array([0.135, 0.388, 0.374, 0.33, 0.28, 0.22, 0.16]) #p fissato
	up = 0.001/np.sqrt(3)

	l_min = np.array([0.515, 0.52, 0.503, 0.472, 0.433, 0.398, 0.411]) #lunghezza sul metro del qmin+p
	l_max = np.array([0.529, 0.53, 0.516, 0.479, 0.441, 0.407, 0.439]) #lunghezza sul metro del qmax+p
	l = (l_min+l_max)/2

	q_min = l_min-p
	q_max = l_max-p
	q = (q_min+q_max)/2 #calcolo di q
	uq = (q_max-q_min)/np.sqrt(12)

	h1 = np.array([0.039, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04 ]) #h prima di ingrandimento
	h2 = np.array([0.110, 0.017, 0.016, 0.02, 0.025, 0.036, 0.068 ]) #h ingrandito
	u_h = 0.001/np.sqrt(3) #incertezza di h
	G = -h2/h1 #ingrandimento, è ribaltato
	uG = np.sqrt((u_h/h1)**2 + (u_h*h2/(h1**2))**2 )

	#setto dati per il fit
	A, B, C, D = par
	#calcolo R1
	Bs = A*p+B+C*p*q+D*q
	uBs = np.sqrt(((A+C*q)*up)**2+((D+C*p)*uq)**2)
	R1 = Bs/uBs

	#calcolo R2
	As = A+C*q
	uAs = np.sqrt((C*uq)**2)
	uAs_Gy = np.sqrt(uAs**2+uG**2)
	R2 = (As-G)/uAs_Gy

	#calcolo R3
	R3 = np.array([A*D-B*C-1])

	#costruisco vettore con tutti i residui
	Res = np.concatenate([R1, R2, R3])
	return Res

def due_lenti(par):
	
	#prima da 100 mm
	p  = np.array([0.130, 0.136, 0.140, 0.146, 0.150, 0.156, 0.160]) #posizione di ingresso
	up = 0.001/np.sqrt(3)

	d = 0.15 #distanza tra le lenti
	ud = 0.001/np.sqrt(3)

	q_max = np.array([0.121, 0.110, 0.103, 0.097, 0.087, 0.080, 0.078])
	q_min = np.array([0.115, 0.102, 0.099, 0.089, 0.083, 0.076, 0.072])
	q = (q_max+q_min)/2
	uq = (q_max-q_min)/np.sqrt(12)

	h1 = np.array([0.040, 0.040, 0.040, 0.040, 0.040, 0.040, 0.040])#h prima di ingrandimento
	h2 = np.array([0.055, 0.052, 0.051, 0.047, 0.046, 0.044, 0.041])#h ingrandito
	u_h1 = 0.001/np.sqrt(3) #incertezza di h1
	u_h2 = 0.001/np.sqrt(3) #incertezza di h2
	G = -h2/h1 #invertito
	uG = np.sqrt((u_h2/h1)**2 + (u_h1*h2/(h1**2))**2 )

	#setto dati per il fit
	A, B, C, D = par
	#calcolo R1
	Bs = A*p+B+C*p*q+D*q
	uBs = np.sqrt(((A+C*q)*up)**2+((D+C*p)*uq)**2)
	R1 = Bs/uBs

	#calcolo R2
	As = A+C*q
	uAs = np.sqrt((C*uq)**2)
	uAs_Gy = np.sqrt(uAs**2+uG**2)
	R2 = (As-G)/uAs_Gy

	#calcolo R3
	R3 = np.array([A*D-B*C-1])

	#costruisco vettore con tutti i residui
	Res = np.concatenate([R1, R2, R3])
	return Res

def bessel_200():
	L = 1 
	u_L = 0.001/np.sqrt(3)
	print(f"L = {L} ± {u_L}")

	p1_min = 0.27
	p1_max = 0.285
	p1 = (p1_min+p1_max)/2
	u_p1 = (p1_max-p1_min)/np.sqrt(12)
	print(f"p1 = {p1} ± {u_p1}")

	p2_min = 0.71
	p2_max = 0.726
	p2 = (p2_min+p2_max)/2
	u_p2 = (p2_max-p2_min)/np.sqrt(12)
	print(f"p2 = {p2} ± {u_p2}")

	f = (L**2 - (p1-p2)**2)/(4*L)
	u_f = np.sqrt( ((L/4+((p2-p1)**2)/(4*L**2))*u_L)**2 + ((p2-p1)/(2*L)*u_p2)**2 +((p2-p1)/(2*L)*u_p1)**2)
	print(f"f = {f} ± {u_f}")
	#devi propagare incertezza

dati_100()
dati_200()
dati_2lenti()

#faccio il fit per la lente a 200
x0 = [1, 0, -1/0.2, 1]
fit = least_squares(d_focale_200, x0)
par_fit = fit.x
C = fit.jac
cov = np.linalg.inv(np.dot(np.transpose(C), C))
print("Lente con fuoco a 200 mm")
print(f"Valori attesi: A = {x0[0]}, B = {x0[1]}, C = {x0[2]}, D = {x0[3]}")
print(f"A = {par_fit[0]} ± {np.diag(cov)[0]}")
print(f"B = {par_fit[1]} ± {np.diag(cov)[1]}")
print(f"C = {par_fit[2]} ± {np.diag(cov)[2]}")
print(f"D = {par_fit[3]} ± {np.diag(cov)[3]}")
print('\n')

#faccio il fit per la lente a 100
x0 = [1, 0, -1/0.1, 1]
fit = least_squares(d_focale_100, x0)
par_fit = fit.x
C = fit.jac
cov = np.linalg.inv(np.dot(np.transpose(C), C))
print("Lente con fuoco a 100 mm")
print(f"Valori attesi: A = {x0[0]}, B = {x0[1]}, C = {x0[2]}, D = {x0[3]}")
print(f"A = {par_fit[0]} ± {np.diag(cov)[0]}")
print(f"B = {par_fit[1]} ± {np.diag(cov)[1]}")
print(f"C = {par_fit[2]} ± {np.diag(cov)[2]}")
print(f"D = {par_fit[3]} ± {np.diag(cov)[3]}")
print('\n')


#faccio il fit per la doppia lente
x0 = [-0.5, 0.15, -7.5, 0.25]
fit = least_squares(due_lenti, x0)
par_fit = fit.x
C = fit.jac
cov = np.linalg.inv(np.dot(np.transpose(C), C))
print("Sistema con 2 lenti")
print(f"Valori attesi: A = {x0[0]}, B = {x0[1]}, C = {x0[2]}, D = {x0[3]}")
print(f"A = {par_fit[0]} ± {np.diag(cov)[0]}")
print(f"B = {par_fit[1]} ± {np.diag(cov)[1]}")
print(f"C = {par_fit[2]} ± {np.diag(cov)[2]}")
print(f"D = {par_fit[3]} ± {np.diag(cov)[3]}")
print('\n')

print("Metodo di Bessel per f = 200 mm")
bessel_200()

