import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from modelo import simular_fedbatch, datos_en_hora
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    grafica = None
    row = None
    t = []
    X = []
    S = []
    V = []
    pH = []
    T = []

    if request.method == "POST":
        tiempo = float(request.form["tiempo"])

        t, X, S, V, pH, T = simular_fedbatch(tiempo)

        # Convert numpy arrays to plain Python lists for the template
        try:
            t = t.tolist()
            X = X.tolist()
            S = S.tolist()
            V = V.tolist()
            pH = pH.tolist()
            T = T.tolist()
        except Exception:
            t = list(t)
            X = list(X)
            S = list(S)
            V = list(V)
            pH = list(pH)
            T = list(T)

        if not os.path.exists("static"):
            os.makedirs("static")

        # Create figure with primary and secondary y-axis
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(t, X, label="Biomasa (g/L)", color="tab:blue")
        ax.plot(t, S, label="Sustrato (g/L)", color="tab:green")
        ax.plot(t, V, label="Volumen (L)", color="tab:purple")
        ax.plot(t, pH, label="pH", color="tab:orange")

        ax.set_xlabel("Tiempo (h)")
        ax.set_ylabel("Concentración / Volumen / pH")
        ax.set_title("Biorreactor Fed-Batch — resultados")
        ax.grid(True)

        # Secondary axis for Temperature
        ax2 = ax.twinx()
        ax2.plot(t, T, label="Temperatura (°C)", color="tab:red", linestyle="--")
        ax2.set_ylabel("Temperatura (°C)")

        # Combine legends from both axes
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc="upper left")

        fig.tight_layout()
        fig.savefig("static/grafica.png")
        plt.close(fig)


        grafica = "grafica.png"

        # Compute single-row data at the final fermentation time (`tiempo`)
        try:
            row = datos_en_hora(tiempo, tiempo)
        except Exception:
            row = None

    return render_template("index.html", grafica=grafica, t=t, X=X, S=S, V=V, pH=pH, T=T, row=row)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
