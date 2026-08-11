import numpy as np 
from scipy import optimize, odr
import matplotlib
import matplotlib.pyplot as plt
import os
# Definiamo la cartella corretta una volta sola
OUTPUT_DIR = r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_18_05"

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
    return f"{x:.{decimali}f}±{u_x:.{decimali}f}"

def determina_decimali_colonna(u_vettore, n=1):
    """
    Trova il numero di decimali ottimale analizzando l'intero array di incertezze.
    Gestisce scientificamente sia incertezze piccolissime (<1) sia incertezze grandi (>=1).
    """
    u_vettore = np.array(u_vettore)
    # Prendiamo il valore minimo non nullo
    u_min = np.min(u_vettore[u_vettore > 0])
    
    # Trova l'ordine di grandezza della prima cifra significativa dell'incertezza
    # Es: 0.005 -> -3 | 1.5 -> 0 | 863 -> 2
    ordine = int(np.floor(np.log10(abs(u_min))))
    
    if ordine >= 0:
        # Se l'incertezza ha la prima cifra significativa prima della virgola (es. 1.5 o 863)
        # Controlliamo se è nel range critico (tra 1.0 e 1.99), nel qual caso si può volere 1 decimale
        if u_min < 2.0:
            return 1
        else:
            return 0
    else:
        # Se l'incertezza è < 1 (es. 0.005 -> ordine = -3), servono decimali dopo la virgola
        return max(0, -ordine + (n - 1))

col_sine = [r'$\omega (rad/s)$', r'$V_a (V)$', r'$\phi_a$', r'$V_b (V)$', r'$\phi_b$']

VaR1, uVaR1, waR1, uwaR1, phiaR1, uphiaR1, kaR1, ukaR1, VbR1, uVbR1, wbR1, uwbR1, phibR1, uphibR1, kbR1, ukbR1= [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
VaR1LC, uVaR1LC, waR1LC, uwaR1LC, phiaR1LC, uphiaR1LC, kaR1LC, ukaR1LC, VbR1LC, uVbR1LC, wbR1LC, uwbR1LC, phibR1LC, uphibR1LC, kbR1LC, ukbR1LC= [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
VaR33, uVaR33, waR33, uwaR33, phiaR33, uphiaR33, kaR33, ukaR33, VbR33, uVbR33, wbR33, uwbR33, phibR33, uphibR33, kbR33, ukbR33= [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
VaR33LC, uVaR33LC, waR33LC, uwaR33LC, phiaR33LC, uphiaR33LC, kaR33LC, ukaR33LC, VbR33LC, uVbR33LC, wbR33LC, uwbR33LC, phibR33LC, uphibR33LC, kbR33LC, ukbR33LC= [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

def collect_R1_R(Va, uVa, wa, uwa, phia, uphia, ka, uka, Vb, uVb, wb, uwb, phib, uphib, kb, ukb):
    VaR1.append(abs(Va))
    uVaR1.append(uVa)
    waR1.append(wa)
    uwaR1.append(uwa)
    phiaR1.append(phia)
    uphiaR1.append(uphia)
    kaR1.append(ka)
    ukaR1.append(uka)
    VbR1.append(abs(Vb))
    uVbR1.append(uVb)
    wbR1.append(wb)
    uwbR1.append(uwb)
    phibR1.append(phib)
    uphibR1.append(uphib)
    kbR1.append(kb)
    ukbR1.append(ukb)

def collect_R1_LC(Va, uVa, wa, uwa, phia, uphia, ka, uka, Vb, uVb, wb, uwb, phib, uphib, kb, ukb):
    VaR1LC.append(abs(Va))
    uVaR1LC.append(uVa)
    waR1LC.append(wa)
    uwaR1LC.append(uwa)
    phiaR1LC.append(phia)
    uphiaR1LC.append(uphia)
    kaR1LC.append(ka)
    ukaR1LC.append(uka)

    VbR1LC.append(abs(Vb))
    uVbR1LC.append(uVb)
    wbR1LC.append(wb)
    uwbR1LC.append(uwb)
    phibR1LC.append(phib)
    uphibR1LC.append(uphib)
    kbR1LC.append(kb)
    ukbR1LC.append(ukb)

def collect_R33_R(Va, uVa, wa, uwa, phia, uphia, ka, uka, Vb, uVb, wb, uwb, phib, uphib, kb, ukb):
    VaR33.append(abs(Va))
    uVaR33.append(uVa)
    waR33.append(wa)
    uwaR33.append(uwa)
    phiaR33.append(phia)
    uphiaR33.append(uphia)
    kaR33.append(ka)
    ukaR33.append(uka)
    VbR33.append(abs(Vb))
    uVbR33.append(uVb)
    wbR33.append(wb)
    uwbR33.append(uwb)
    phibR33.append(phib)
    uphibR33.append(uphib)
    kbR33.append(kb)
    ukbR33.append(ukb)

def collect_R33_LC(Va, uVa, wa, uwa, phia, uphia, ka, uka, Vb, uVb, wb, uwb, phib, uphib, kb, ukb):
    VaR33LC.append(abs(Va))
    uVaR33LC.append(uVa)
    waR33LC.append(wa)
    uwaR33LC.append(uwa)
    phiaR33LC.append(phia)
    uphiaR33LC.append(uphia)
    kaR33LC.append(ka)
    ukaR33LC.append(uka)

    VbR33LC.append(abs(Vb))
    uVbR33LC.append(uVb)
    wbR33LC.append(wb)
    uwbR33LC.append(uwb)
    phibR33LC.append(phib)
    uphibR33LC.append(uphib)
    kbR33LC.append(kb)
    ukbR33LC.append(ukb)


def comma_to_float(s):
    return float(s.replace(',', '.'))

def get_data(path):
    #112 colonne
    data = np.genfromtxt(path, delimiter=';', skip_header=1, converters={i: comma_to_float for i in range(112)})
    rows = len(data)
    ds = []
    #28 set da 4 colonne = 112 colonne
    for i in range(28): ds.append(data[:, i*4:(i+1)*4].T)
    return ds

def voltage_fit(x, A, w, phi, b):
    # p = [A, omega, phi, b]
    y = A*np.cos(w*x+phi) + b
    return y

def voltage_odr(p, x):
    # p = [A, omega, phi, b]
    y = p[0]*np.cos(p[1]*x+p[2]) + p[3]
    return y

def processing(data, w0, f, mode='N'):

    R3_LC = {44616: 0.8041, 53008: 0.6843,  62979: 0.4833,  74825: 0.1793, 81559: 0.0001, 96900: 0.3435, 115128: 0.5961, 136783: 0.7521, 149093: 0.8041}
    R1_LC = {44616: 0.9758, 53008: 0.9516,  62979: 0.8766,  74825: 0.5153, 81559: 0.0001, 96901: 0.7701, 115128: 0.9259, 136783: 0.9665, 149093: 0.9758}
    g = 1
    if 200<=w0 and w0<=2000: g = 100
    #tolgo i nan
    data_columns = np.any(~np.isnan(data), axis=0)
    last = np.flatnonzero(data_columns)[-1]
    data = data[:, :last + 1]
    #print(data)

    #calcolo incertezze su Va e Vb
    u_Va = np.sqrt(1/3*(data[1]*0.01+2.5e-3/g)**2)
    u_Vb = np.sqrt(1/3*(data[3]*0.01+2.5e-3/g)**2)

    #tagli ad hoc dei dati
    
    t_a, v_a= data[0], data[1]
    t_b, v_b = data[2], data[3]

    if w0 == 81559*2*np.pi and mode=='R1_81':
            t_a, v_a, u_Va = data[0][:120], data[1][:120], u_Va[:120]
            t_b, v_b, u_Vb = data[2][:120], data[3][:120], u_Vb[:120]


    if w0 == 149093*2*np.pi and mode=='R1_149':
        t_a, v_a, u_Va = data[0][:300], data[1][:300], u_Va[:300]
        t_b, v_b, u_Vb = data[2][:300], data[3][:300], u_Vb[:300]

    if w0 == 149093*2*np.pi and mode=='R3_149':
        t_a, v_a, u_Va = data[0][-300:], data[1][-300:], u_Va[-300:]
        t_b, v_b, u_Vb = data[2][:-300], data[3][:-300], u_Vb[:-300]

    if w0 == 115128*2*np.pi and mode=='R3_115':
        t_a, v_a, u_Va = data[0][:200], data[1][:200], u_Va[:200]
        t_b, v_b, u_Vb = data[2][:200], data[3][:200], u_Vb[:200]
    
    if w0 == 136783*2*np.pi and mode=='R3_136':
        t_a, v_a, u_Va = data[0][:300], data[1][:300], u_Va[:300]
        t_b, v_b, u_Vb = data[2][:300], data[3][:300], u_Vb[:300]
    
    if w0 == 57779*2*np.pi and mode=='R3_57':
        t_a, v_a, u_Va = data[0][:300], data[1][:300], u_Va[:300]
        t_b, v_b, u_Vb = data[2][:300], data[3][:300], u_Vb[:300]

    if w0 == 250000*2*np.pi and mode=='R3_250':
        mask_a = np.isfinite(data[0]) & np.isfinite(data[1]) & (u_Va > 0)
        mask_b = np.isfinite(data[2]) & np.isfinite(data[3]) & (u_Vb > 0)
        t_a, v_a, u_Va = data[0][mask_a], data[1][mask_a], u_Va[mask_a]
        t_b, v_b, u_Vb = data[2][mask_b], data[3][mask_b], u_Vb[mask_b]

    #trovo valori iniziali del fit
    A0 = (max(v_a)-min(v_a))/2 #ampiezza della tensione totale (canale a)
    B0 = (max(v_b)-min(v_b))/2 #ampiezza della tensione su R o LC (canale b)
    phi_a0 = np.arccos(np.clip(v_a[0]/A0, -1, 1))
    phi_b0 = np.arccos(np.clip(v_b[0]/B0, -1, 1))
    if w0>2*np.pi*81559: phi_b0 = -abs(phi_b0)
    else: phi_b0 = abs(phi_b0)
    b_a0 = min(abs(v_a))
    b_b0 = min(abs(v_b))
    #print(f"A0={A0}, B0={B0}, phi_a0={phi_a0}, phi_b0={phi_b0}, w0 = {w0}")

    #faccio fit
    voltage = odr.Model(voltage_odr)

    Va = odr.Data(t_a, v_a, wd = 1/(u_Va**2))
    Va_odr = odr.ODR(Va, voltage, [A0, w0, phi_a0, b_a0], maxit=1000)
    res = Va_odr.run()
    par_a, u_a = res.beta, res.sd_beta

    Vb = odr.Data(t_b, v_b, wd = 1/(u_Vb**2))
    Vb_odr = odr.ODR(Vb, voltage, [B0, w0, phi_b0, b_b0])
    res = Vb_odr.run()
    par_b, u_b = res.beta, res.sd_beta

    return par_a, u_a, par_b, u_b


def frequency_analysis(set, f, mode):
    #funzione in cui per ogni frequenza e dataset realizzo fit e printo risultati
    print(f"Frequenza scelta = {f}    Pulsazione associaata = {2*np.pi*f}")
    pa, ua, pb, ub = processing(set, 2*np.pi*f, f, mode)
    
    print(f'V_a = {pa[0]}cos({pa[1]}t + {pa[2]}) + {pa[3]}')
    print(ua)
    print(f'V_b = {pb[0]}cos({pb[1]}t + {pb[2]}) + {pb[3]}')
    print(ub)

    if mode in ['R1','R1_81','R1_149', 'R1_48']: collect_R1_R(pa[0], ua[0], pa[1], ua[1], pa[2], ua[2], pa[3], ua[3], pb[0], ub[0], pb[1], ub[1], pb[2], ub[2], pb[3], ub[3])
    elif mode in ['R3', 'R3_115', 'R3_136', 'R3_57', 'R3_250', 'R3_149', 'R3_200']:
        collect_R33_R(pa[0], ua[0], pa[1], ua[1], pa[2], ua[2], pa[3], ua[3], pb[0], ub[0], pb[1], ub[1], pb[2], ub[2], pb[3], ub[3])
    elif mode == 'R1_LC': collect_R1_LC(pa[0], ua[0], pa[1], ua[1], pa[2], ua[2], pa[3], ua[3], pb[0], ub[0], pb[1], ub[1], pb[2], ub[2], pb[3], ub[3])
    elif mode == 'R3_LC': collect_R33_LC(pa[0], ua[0], pa[1], ua[1], pa[2], ua[2], pa[3], ua[3], pb[0], ub[0], pb[1], ub[1], pb[2], ub[2], pb[3], ub[3])
    uph = np.sqrt(ub[2]**2+ua[2]**2)
    ug = np.sqrt((ub[0]/pa[0])**2+(pb[0]*ua[0]/(pa[0]**2))**2)
    phase = pb[2]-pa[2]
    print(f'dphi = {phase} = π*{(phase)/np.pi}')
    gain = abs(pb[0]/pa[0])
    gain_dB = 20*np.log10(gain)
    ug_dB = np.sqrt((20*ug/(np.log(10)*gain))**2)
    print(f'gain = {gain}  gain_dB = {gain_dB} dB')
    print('\n')
    return phase, gain, gain_dB, uph, ug, ug_dB

def bode_plot(w_dict):
    #faccio diagramma di bode
    ws = w_dict.keys()
    y = w_dict.values()
    plt.semilogx(ws, y, 'o', label='Valori misurati')

def bode_gain(p, w):
    y = 1/np.sqrt(1+(p[0]*(w/p[1]-p[1]/w))**2)
    return y

def bode_gain_fit(Q, w0, w_dict, u_dict):
    ws = np.array(list(w_dict.keys()))
    gains = np.array(list(w_dict.values()))
    u = np.array(list(u_dict.values()))
    Hgain = odr.Model(bode_gain)
    bode_data = odr.Data(ws, gains, wd = 1/(u**2))
    bode_odr = odr.ODR(bode_data, Hgain, [Q, w0])
    res = bode_odr.run()
    par, u = res.beta, res.sd_beta
    return par, u

def bode_gain_dB(p, w):
    y = -10*np.log10(1+(p[0]*(w/p[1]-p[1]/w))**2)
    return y

def bode_gain_dB_fit(Q, w0, w_dict, u_dict):
    ws = np.array(list(w_dict.keys()))
    gains = np.array(list(w_dict.values()))
    u = np.array(list(u_dict.values()))
    Hgain = odr.Model(bode_gain_dB)
    bode_data = odr.Data(ws, gains, wd = 1/(u**2))
    bode_odr = odr.ODR(bode_data, Hgain, [Q, w0])
    res = bode_odr.run()
    par, u = res.beta, res.sd_beta
    return par, u



#prendo i percorsi per R = 1 kOhm e R = 3 kOhm
path_R1 = r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_18_05\R1\dati_definitivi.csv"
path_R3_3 = r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_18_05\R3_3\dati_definitivi.csv"


def f_R1(num_fig):
    R = 1e+3
    L = 6.8e-3
    C = 560e-12
    print(f" R = 1 kOhm   L = {L} H      C = {C} F")
    print("Pulsazione di risonanza:", 1/np.sqrt(L*C))
    print("Frequenza di risonanza: ", 1/(np.sqrt(L*C)*2*np.pi))
    w0 = 1/np.sqrt(L*C)
    Q = 1/(w0*R*C)
    print('\n')
    #prendo i dati dai file
    path_R1 = r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_18_05\R1\dati_definitivi.csv"
    d_R1 = get_data(path_R1)

    #array con frequenze usate
    fs = np.array([81559, 88900, 96900, 105622, 115128, 125489, 136783, 149093, 74825, 68646, 62979, 57779, 53008, 48631, 44615, 22183, 200000, 250000, 250, 81559, 96901, 115128, 149093, 74825, 62979, 53008, 44616, 136783]) # al 20esimo inizia LC su 81559
    #fs = np.array([81559, 88900, 96900, 105622, 115128, 125489, 136783, 149093, 74825, 68646, 62979, 57779, 53008, 48631, 44615, 22183, 200000, 250000, 250])

    #salvo fasi e guadagni associati a frequenze
    phaseR = {}
    phaseR_deg = {}
    gainR = {}
    gainR_dB = {}
    uphaseR = {}
    ugainR = {}
    ugainR_dB = {}
    phaseLC = {}
    phaseLC_deg = {}
    gainLC = {}
    gainLC_dB = {}
    uphaseLC = {}
    ugainLC = {}
    ugainLC_dB = {}

    for i, f in enumerate(fs):
        #distinguo i capi di R da quelli di LC 
        if i<19:
            
            #setto parole operative per casi strani di fit
            if f in [149093, 250000, 22183]: continue
            mode = 'R1'
            if f == 81559: mode='R1_81'
            if f == 149093: mode= 'R1_149'
            if f == 48631: mode = 'R1_48'
            print('Capi di R1')
            phase, gain, gain_dB, uph, ug, ug_dB = frequency_analysis(d_R1[i], f, mode)
            phaseR[2*np.pi*f] = phase
            phaseR_deg[2*np.pi*f] = phase*180/np.pi
            gainR[2*np.pi*f] = gain
            gainR_dB[2*np.pi*f] = gain_dB
            uphaseR[2*np.pi*f] = uph
            ugainR[2*np.pi*f] = ug
            ugainR_dB[2*np.pi*f] = ug_dB
        else:
            if f in [149093, 74825]: continue
            mode = 'R1_LC'
            print('Capi di LC')
            phase, gain, gain_dB, uph, ug, ug_dB = frequency_analysis(d_R1[i], f, mode)
            phaseLC[2*np.pi*f] = phase
            phaseLC_deg[2*np.pi*f] = phase*180/np.pi
            gainLC[2*np.pi*f] = gain
            gainLC_dB[2*np.pi*f] = gain_dB
            uphaseLC[2*np.pi*f] = uph
            ugainLC[2*np.pi*f] = ug
            ugainLC_dB[2*np.pi*f] = ug_dB

    parH, uH = bode_gain_fit(Q, w0, gainR, ugainR)
    parH_dB, uH_dB = bode_gain_dB_fit(Q, w0, gainR_dB, ugainR_dB)
    print(f"Q atteso: {Q}")
    print(f"w0 atteso: {w0}")
    print("FIT SU GUADAGNO NUMERICO")
    print(f"Q = {parH[0]} ± {uH[0]}")
    print(f"w0 = {parH[1]} ± {uH[1]}")
    print("FIT SU GUADAGNO IN dB")
    print(f"Q = {parH_dB[0]} ± {uH_dB[0]}")
    print(f"w0 = {parH_dB[1]} ± {uH_dB[1]}")
    print('\n')
    
    fig = plt.figure(2*num_fig+1)
    plt.subplot(1, 2, 1)
    bode_plot(gainR_dB)
    ww = np.linspace(min(np.array(list(gainR_dB.keys()))), max(np.array(list(gainR_dB.keys())))+10000, 50)
    plt.semilogx(ww, bode_gain_dB(parH_dB, ww), 'r--', label='Valori modello')
    plt.xlabel(r'$\omega (rad/s)$')
    plt.ylabel('Ampiezza (dB)')
    plt.subplot(1, 2, 2)
    bode_plot(phaseR_deg)
    plt.xlabel(r'$\omega (rad/s)$')
    plt.ylabel('Fase (°)')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'bodeR1.pgf'))
    plt.close() # <-- Importante chiuderlo!
    fig = plt.figure(2*num_fig+2)
    plt.subplot(1, 2, 1)
    bode_plot(gainLC_dB)
    plt.xlabel(r'$\omega (rad/s)$')
    plt.ylabel('Ampiezza (dB)')
    plt.subplot(1, 2, 2)
    bode_plot(phaseLC_deg)
    plt.xlabel(r'$\omega (rad/s)$')
    plt.ylabel('Fase (°)')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'bodeR1LC.pgf'))
    plt.close() # <-- Importante chiuderlo!

    # ==================== SALVATAGGIO TABELLE GUADAGNO R1 ====================
    # Definizione delle intestazioni con le corrette unità di misura
    col_gain = [r'$\omega$ (rad/s)', r'Guadagno $H$']
    col_gain_dB = [r'$\omega$ (rad/s)', r'Guadagno (dB)']

    # 1. Preparazione Dati: Frequenza e Guadagno non in dB
    data_gain = []
    for w, g in gainR.items():
        ug = ugainR[w]
        str_w = f"{w:.0f}" # La pulsazione non ha incertezza calcolata qui
        str_g = format_misura(g, ug, n=2) # 2 cifre significative
        data_gain.append([str_w, str_g])
    
    # Creazione Tabella Guadagno Lineare
    n_righe = len(data_gain)
    #altezza = max(2.0, n_righe * 0.45 + 0.8)  # 0.45 pollici per riga + header
    altezza = 3.5
    fig_tab1, ax_tab1 = plt.subplots(figsize=(5, altezza))
    ax_tab1.axis('off')
    tab1 = ax_tab1.table(cellText=data_gain, colLabels=col_gain, loc='center', cellLoc='center')
    tab1.set_fontsize(10)
    tab1.auto_set_column_width(col=list(range(len(col_gain))))
    for (row, col), cell in tab1.get_celld().items():
        if row == 0: cell.set_text_props(weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'tabella_guadagno_R1.pgf'), bbox_inches='tight')
    plt.close(fig_tab1)

    # 2. Preparazione Dati: Frequenza e Guadagno in dB
    data_gain_dB = []
    for w, g_dB in gainR_dB.items():
        ug_dB = ugainR_dB[w]
        str_w = f"{w:.0f}"
        str_g_dB = format_misura(g_dB, ug_dB, n=2) # 2 cifre significative
        data_gain_dB.append([str_w, str_g_dB])
    
    # Creazione Tabella Guadagno in dB
    fig_tab2, ax_tab2 = plt.subplots(figsize=(5, altezza))
    ax_tab2.axis('off')
    tab2 = ax_tab2.table(cellText=data_gain_dB, colLabels=col_gain_dB, loc='center', cellLoc='center')
    tab2.set_fontsize(10)
    tab2.auto_set_column_width(col=list(range(len(col_gain_dB))))
    for (row, col), cell in tab2.get_celld().items():
        if row == 0: cell.set_text_props(weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'tabella_guadagno_dB_R1.pgf'), bbox_inches='tight')
    plt.close(fig_tab2)
    # =========================================================================
    


def f_R3_3(num_fig):
    R = 3.3e+3
    L = 6.8e-3
    C = 560e-12
    print(f" R = 3.3 kOhm   L = {L} H      C = {C} F")
    print("Pulsazione di risonanza:", 1/np.sqrt(L*C))
    print("Frequenza di risonanza: ", 1/(np.sqrt(L*C)*2*np.pi))
    w0 = 1/np.sqrt(L*C)
    Q = 1/(w0*R*C)
    print('\n')
    
    #prendo i dati dai file
    path_R3_3 = r"E:\UNI\fisica\II ANNO\II_semestre\Esperimentazioni II\esp_18_05\R3_3\dati_definitivi.csv"
    d_R33 = get_data(path_R3_3)

    #array con frequenze usate
    fs = np.array([81559, 88900, 96900, 105622, 115128, 125489, 136783, 149093, 74825, 68647, 62979, 57779, 53008, 48631, 44616, 250, 22183, 250000, 200000, 81559, 96900, 115128, 149093, 74825, 62979, 53008, 44616, 136783]) # al 20esimo inizia LC su 81559
    #fs = np.array([81559, 88900, 96900, 105622, 115128, 125489, 136783, 149093, 74825, 68646, 62979, 57779, 53008, 48631, 44615, 22183, 200000, 250000, 250])

    #salvo fasi e guadagni associati a frequenze
    phaseR = {}
    phaseR_deg = {}
    gainR = {}
    gainR_dB = {}
    uphaseR = {}
    ugainR = {}
    ugainR_dB = {}
    phaseLC = {}
    phaseLC_deg = {}
    gainLC = {}
    gainLC_dB = {}
    uphaseLC = {}
    ugainLC = {}
    ugainLC_dB = {}

    for i, f in enumerate(fs):
        #distinguo i capi di R da quelli di LC 
        if i<19:
            #setto parole operative per casi strani di fit
            if f in [149093, 250000, 22183]: continue
            mode = 'R3'
            if f == 115128: mode='R3_115'
            if f == 136783: mode= 'R3_136'
            if f == 57779: mode='R3_57'
            if f == 250000: mode= 'R3_250'
            if f == 149093: mode = 'R3_149'
            if f == 200000: mode = 'R3_200'
            print('Capi di R3_3')
            phase, gain, gain_dB, uph, ug, ug_dB = frequency_analysis(d_R33[i], f, mode)
            phaseR[2*np.pi*f] = phase
            phaseR_deg[2*np.pi*f] = phase*180/np.pi
            gainR[2*np.pi*f] = gain
            gainR_dB[2*np.pi*f] = gain_dB
            uphaseR[2*np.pi*f] = uph
            ugainR[2*np.pi*f] = ug
            ugainR_dB[2*np.pi*f] = ug_dB
        else:
            if f in [149093, 74825]: continue
            mode = 'R3_LC'
            print('Capi di LC')
            phase, gain, gain_dB, uph, ug, ug_dB = frequency_analysis(d_R33[i], f, mode)
            phaseLC[2*np.pi*f] = phase
            phaseLC_deg[2*np.pi*f] = phase*180/np.pi
            gainLC[2*np.pi*f] = gain
            gainLC_dB[2*np.pi*f] = gain_dB
            uphaseLC[2*np.pi*f] = uph
            ugainLC[2*np.pi*f] = ug
            ugainLC_dB[2*np.pi*f] = ug_dB

    parH, uH = bode_gain_fit(Q, w0, gainR, ugainR)
    parH_dB, uH_dB = bode_gain_dB_fit(Q, w0, gainR_dB, ugainR_dB)
    print(f"Q atteso: {Q}")
    print(f"w0 atteso: {w0}")
    print("FIT SU GUADAGNO NUMERICO")
    print(f"Q = {parH[0]} ± {uH[0]}")
    print(f"w0 = {parH[1]} ± {uH[1]}")
    print("FIT SU GUADAGNO IN dB")
    print(f"Q = {parH_dB[0]} ± {uH_dB[0]}")
    print(f"w0 = {parH_dB[1]} ± {uH_dB[1]}")
    print('\n')

    fig = plt.figure(2*num_fig+1)
    plt.subplot(1, 2, 1)
    bode_plot(gainR_dB)
    ww = np.linspace(min(np.array(list(gainR_dB.keys()))), max(np.array(list(gainR_dB.keys())))+10000, 50)
    plt.semilogx(ww, bode_gain_dB(parH_dB, ww), 'r--', label='Valori modello')
    plt.xlabel(r'$\omega (rad/s)$')
    plt.ylabel('Ampiezza (dB)')
    plt.subplot(1, 2, 2)
    bode_plot(phaseR_deg)
    plt.xlabel(r'$\omega (rad/s)$')
    plt.ylabel('Fase (°)')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'bodeR33.pgf'))
    plt.close() # <-- Importante chiuderlo!
    fig = plt.figure(2*num_fig+2)
    plt.subplot(1, 2, 1)
    bode_plot(gainLC_dB)
    plt.xlabel(r'$\omega (rad/s)$')
    plt.ylabel('Ampiezza (dB)')
    plt.subplot(1, 2, 2)
    bode_plot(phaseLC_deg)
    plt.xlabel(r'$\omega (rad/s)$')
    plt.ylabel('Fase (°)')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'bodeR33LC.pgf'))
    plt.close() # <-- Importante chiuderlo!

    # ==================== SALVATAGGIO TABELLE GUADAGNO R3_3 ====================
    # Definizione delle intestazioni con le corrette unità di misura
    col_gain = [r'$\omega$ (rad/s)', r'Guadagno $H$']
    col_gain_dB = [r'$\omega$ (rad/s)', r'Guadagno (dB)']

    # 1. Preparazione Dati: Frequenza e Guadagno non in dB
    data_gain = []
    for w, g in gainR.items():
        ug = ugainR[w]
        str_w = f"{w:.0f}"
        str_g = format_misura(g, ug, n=2) # 2 cifre significative
        data_gain.append([str_w, str_g])
    
    # Creazione Tabella Guadagno Lineare
    n_righe = len(data_gain)
    #altezza = max(2.0, n_righe * 0.45 + 0.8)  # 0.45 pollici per riga + header
    altezza = 3.5
    fig_tab1, ax_tab1 = plt.subplots(figsize=(5, altezza))
    ax_tab1.axis('off')
    tab1 = ax_tab1.table(cellText=data_gain, colLabels=col_gain, loc='center', cellLoc='center')
    tab1.set_fontsize(10)
    tab1.auto_set_column_width(col=list(range(len(col_gain))))
    for (row, col), cell in tab1.get_celld().items():
        if row == 0: cell.set_text_props(weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'tabella_guadagno_R33.pgf'), bbox_inches='tight')
    plt.close(fig_tab1)

    # 2. Preparazione Dati: Frequenza e Guadagno in dB
    data_gain_dB = []
    for w, g_dB in gainR_dB.items():
        ug_dB = ugainR_dB[w]
        str_w = f"{w:.0f}"
        str_g_dB = format_misura(g_dB, ug_dB, n=2) # 2 cifre significative
        data_gain_dB.append([str_w, str_g_dB])
    
    # Creazione Tabella Guadagno in dB
    fig_tab2, ax_tab2 = plt.subplots(figsize=(5, altezza))
    ax_tab2.axis('off')
    tab2 = ax_tab2.table(cellText=data_gain_dB, colLabels=col_gain_dB, loc='center', cellLoc='center')
    tab2.set_fontsize(10)
    tab2.auto_set_column_width(col=list(range(len(col_gain_dB))))
    for (row, col), cell in tab2.get_celld().items():
        if row == 0: cell.set_text_props(weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'tabella_guadagno_dB_R33.pgf'), bbox_inches='tight')
    plt.close(fig_tab2)
    # ===========================================================================



f_R1(0)
f_R3_3(1)
# Chiude le figure precedenti per non sovrapporre i grafici alle tabelle

# Calcolo dei decimali corretto per ogni tabella
decVaR1, decwaR1, decphiaR1, deckaR1, decVbR1, decwbR1, decphibR1, deckbR1 = determina_decimali_colonna(uVaR1), determina_decimali_colonna(uwaR1), determina_decimali_colonna(uphiaR1), determina_decimali_colonna(ukaR1), determina_decimali_colonna(uVbR1), determina_decimali_colonna(uwbR1), determina_decimali_colonna(uphibR1), determina_decimali_colonna(ukbR1)
decVaR1LC, decwaR1LC, decphiaR1LC, deckaR1LC, decVbR1LC, decwbR1LC, decphibR1LC, deckbR1LC = determina_decimali_colonna(uVaR1LC), determina_decimali_colonna(uwaR1LC), determina_decimali_colonna(uphiaR1LC), determina_decimali_colonna(ukaR1LC), determina_decimali_colonna(uVbR1LC), determina_decimali_colonna(uwbR1LC), determina_decimali_colonna(uphibR1LC), determina_decimali_colonna(ukbR1LC)
decVaR33, decwaR33, decphiaR33, deckaR33, decVbR33, decwbR33, decphibR33, deckbR33 = determina_decimali_colonna(uVaR33), determina_decimali_colonna(uwaR33), determina_decimali_colonna(uphiaR33), determina_decimali_colonna(ukaR33), determina_decimali_colonna(uVbR33), determina_decimali_colonna(uwbR33), determina_decimali_colonna(uphibR33), determina_decimali_colonna(ukbR33)
decVaR33LC, decwaR33LC, decphiaR33LC, deckaR33LC, decVbR33LC, decwbR33LC, decphibR33LC, deckbR33LC = determina_decimali_colonna(uVaR33LC), determina_decimali_colonna(uwaR33LC), determina_decimali_colonna(uphiaR33LC), determina_decimali_colonna(ukaR33LC), determina_decimali_colonna(uVbR33LC), determina_decimali_colonna(uwbR33LC), determina_decimali_colonna(uphibR33LC), determina_decimali_colonna(ukbR33LC)

# ==================== TABELLA R1 ====================
str_Va = [format_misura(r, u, 2) for r, u in zip(VaR1, uVaR1)]
str_wa = [format_misura(r, u, 2) for r, u in zip(waR1, uwaR1)]
str_phia = [format_misura(r, u, 2) for r, u in zip(phiaR1, uphiaR1)]
str_ka = [format_misura(r, u, 2) for r, u in zip(kaR1, ukaR1)]
str_Vb = [format_misura(r, u, 2) for r, u in zip(VbR1, uVbR1)]
str_wb = [format_misura(r, u, 2) for r, u in zip(wbR1, uwbR1)]
str_phib = [format_misura(r, u, 2) for r, u in zip(phibR1, uphibR1)]
str_kb = [format_misura(r, u, 2) for r, u in zip(kbR1, ukbR1)]

data = list(zip(str_wa, str_Va, str_phia, str_Vb, str_phib))
n_righe = len(data)
#altezza = max(2.0, n_righe * 0.45 + 0.8)  # 0.45 pollici per riga + header
altezza = 3.2
fig, ax = plt.subplots(figsize=(7.5, altezza))
ax.axis('off')

tabella = ax.table(cellText=data, colLabels=col_sine, loc='center', cellLoc='center')
#tabella.auto_set_font_size(False)
tabella.set_fontsize(8)
tabella.auto_set_column_width(col=list(range(len(col_sine)))) # <--- Ridimensiona le colonne in base al testo

for (row, col), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'tabellaR1.pgf'), bbox_inches='tight')
plt.close()


# ==================== TABELLA R1 LC ====================
str_Va = [format_misura(r, u, 2) for r, u in zip(VaR1LC, uVaR1LC)]
str_wa = [format_misura(r, u, 2) for r, u in zip(waR1LC, uwaR1LC)]
str_phia = [format_misura(r, u, 2) for r, u in zip(phiaR1LC, uphiaR1LC)]
str_ka = [format_misura(r, u, 2) for r, u in zip(kaR1LC, ukaR1LC)]
str_Vb = [format_misura(r, u, 2) for r, u in zip(VbR1LC, uVbR1LC)]
str_phib = [format_misura(r, u, 2) for r, u in zip(phibR1LC, uphibR1LC)]
str_kb = [format_misura(r, u, 2) for r, u in zip(kbR1LC, ukbR1LC)]

data = list(zip(str_wa, str_Va, str_phia, str_Vb, str_phib))
n_righe = len(data)
#altezza = max(2.0, n_righe * 0.45 + 0.8)  # 0.45 pollici per riga + header
altezza = 3.2
fig, ax = plt.subplots(figsize=(7.5, altezza))
ax.axis('off')

tabella = ax.table(cellText=data, colLabels=col_sine, loc='center', cellLoc='center')
#tabella.auto_set_font_size(False)
tabella.set_fontsize(8)
tabella.auto_set_column_width(col=list(range(len(col_sine))))

for (row, col), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'tabellaR1LC.pgf'), bbox_inches='tight')
plt.close()


# ==================== TABELLA R33 ====================
str_Va = [format_misura(r, u, 2) for r, u in zip(VaR33, uVaR33)]
str_wa = [format_misura(r, u, 2) for r, u in zip(waR33, uwaR33)]
str_phia = [format_misura(r, u, 2) for r, u in zip(phiaR33, uphiaR33)]
str_ka = [format_misura(r, u, 2) for r, u in zip(kaR33, ukaR33)]
str_Vb = [format_misura(r, u, 2) for r, u in zip(VbR33, uVbR33)]
str_phib = [format_misura(r, u, 2) for r, u in zip(phibR33, uphibR33)]
str_kb = [format_misura(r, u, 2) for r, u in zip(kbR33, ukbR33)]

data = list(zip(str_wa, str_Va, str_phia, str_Vb, str_phib))
n_righe = len(data)
#altezza = max(2.0, n_righe * 0.45 + 0.8)  # 0.45 pollici per riga + header
altezza = 3.2
fig, ax = plt.subplots(figsize=(7.5, altezza))
ax.axis('off')

tabella = ax.table(cellText=data, colLabels=col_sine, loc='center', cellLoc='center')
#tabella.auto_set_font_size(False)
tabella.set_fontsize(8)
tabella.auto_set_column_width(col=list(range(len(col_sine))))

for (row, col), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'tabellaR33.pgf'), bbox_inches='tight')
plt.close()


# ==================== TABELLA R33 LC ====================
str_Va = [format_misura(r, u, 2) for r, u in zip(VaR33LC, uVaR33LC)]
str_wa = [format_misura(r, u, 2) for r, u in zip(waR33LC, uwaR33LC)]
str_phia = [format_misura(r, u, 2) for r, u in zip(phiaR33LC, uphiaR33LC)]
str_ka = [format_misura(r, u, 2) for r, u in zip(kaR33LC, ukaR33LC)]
str_Vb = [format_misura(r, u, 2) for r, u in zip(VbR33LC, uVbR33LC)]
str_phib = [format_misura(r, u, 2) for r, u in zip(phibR33LC, uphibR33LC)]
str_kb = [format_misura(r, u, 2) for r, u in zip(kbR33LC, ukbR33LC)]

data = list(zip(str_wa, str_Va, str_phia, str_Vb, str_phib))
n_righe = len(data)
#altezza = max(2.0, n_righe * 0.45 + 0.8)  # 0.45 pollici per riga + header
altezza = 3.2
fig, ax = plt.subplots(figsize=(7.5, altezza))
ax.axis('off')

tabella = ax.table(cellText=data, colLabels=col_sine, loc='center', cellLoc='center')
#tabella.auto_set_font_size(False)
tabella.set_fontsize(8)
tabella.auto_set_column_width(col=list(range(len(col_sine))))

for (row, col), cell in tabella.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'tabellaR33LC.pgf'), bbox_inches='tight')
plt.close()