import numpy as np
from scipy.integrate import odeint

def modelo_fedbatch(y, t, p):
    X, S, V, pH, T = y

    mu_max = p["mu_max"]
    Ks = p["Ks"]
    Yxs = p["Yxs"]
    F = p["F"]
    Sf = p["Sf"]

    Topt = p["Topt"]
    sigT = p["sigT"]
    pHopt = p["pHopt"]
    sigpH = p["sigpH"]

    Tset = p["Tset"]
    q_heat = p["q_heat"]
    k_cool = p["k_cool"]

    fT = np.exp(-((T - Topt)**2) / (2 * sigT**2))
    fpH = np.exp(-((pH - pHopt)**2) / (2 * sigpH**2))

    mu = mu_max * (S / (Ks + S)) * fT * fpH

    dXdt = mu * X - (F / V) * X
    dSdt = -(1 / Yxs) * mu * X + (F / V) * (Sf - S)
    dVdt = F
    dpHdt = -0.01 * mu * X
    dTdt  = q_heat * mu * X - k_cool * (T - Tset)

    return [dXdt, dSdt, dVdt, dpHdt, dTdt]


def simular_fedbatch(tiempo):
    t = np.linspace(0, tiempo, 400)

    y0 = [
        0.1,   # X (g/L)
        5.0,   # S (g/L)
        1.0,   # V (L)
        7.0,   # pH
        30.0   # T (°C)
    ]

    params = {
        "mu_max": 0.6,
        "Ks": 0.5,
        "Yxs": 0.5,
        "F": 0.05,
        "Sf": 20.0,

        "Topt": 37.0,
        "sigT": 5.0,
        "pHopt": 7.0,
        "sigpH": 0.7,

        "Tset": 37.0,
        "q_heat": 0.12,
        "k_cool": 0.25
    }

    sol = odeint(modelo_fedbatch, y0, t, args=(params,))
    X, S, V, pH, T = sol.T

    return t, X, S, V, pH, T


def datos_en_hora(tiempo_total, hora_consulta):
    t, X, S, V, pH, T = simular_fedbatch(tiempo_total)
    idx = np.argmin(np.abs(t - hora_consulta))

    return {
        "hora": round(float(t[idx]), 3),
        "X": round(float(X[idx]), 3),
        "S": round(float(S[idx]), 3),
        "V": round(float(V[idx]), 3),
        "pH": round(float(pH[idx]), 3),
        "T": round(float(T[idx]), 3)
    }
