from flask import Flask, render_template, request

app = Flask(__name__)

# Постійні значення
Q_C = 32.68  # МДж/кг
ETA_ZU = 0.985  # Ефективність очищення
AVYN_VUHILLYA = 0.80  # Рідке шлаковидалення (вугілля)
AVYN_MAZUT = 1.00
ETA_I = 0.05  # Без десульфуризації
G_VIN_VUHILLYA = 1.5  # %
G_VIN_MAZUT = 0.0  # %

def k_tv(Ar, q4, Qri, a_vyn, eta_zu, G_vin):
    return ((Ar * a_vyn * Q_C * (1 - q4 / 100) * (1 - eta_zu) * (1 - G_vin / 100)) / Qri)

def calculate_emission(k_tv, B, Qri):
    return k_tv * (B * 1e6) / (Qri * 1e3) / 1e3  # г → кг → т

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        # Отримуємо вхідні дані
        B_coal = float(request.form["B_coal"])
        B_oil = float(request.form["B_oil"])
        V_gas = float(request.form["V_gas"])

        # Параметри
        Qri_coal = 20.47
        Ar_coal = 25.2
        q4_coal = 0.5
        G_vin_coal = G_VIN_VUHILLYA

        Qri_oil = 40.4
        Ar_oil = 0.15
        q4_oil = 0.3
        G_vin_oil = G_VIN_MAZUT

        Qri_gas = 33.08
        rho_gas = 0.723

        # kтв
        k_coal = k_tv(Ar_coal, q4_coal, Qri_coal, AVYN_VUHILLYA, ETA_ZU, G_vin_coal)
        k_oil = k_tv(Ar_oil, q4_oil, Qri_oil, AVYN_MAZUT, ETA_ZU, G_vin_oil)

        # Валові викиди
        E_coal = calculate_emission(k_coal, B_coal, Qri_coal)
        E_oil = calculate_emission(k_oil, B_oil, Qri_oil)
        E_gas = 0  # Природний газ – 0 тверді частинки

        result = {
            "k_coal": round(k_coal, 2),
            "E_coal": round(E_coal, 2),
            "k_oil": round(k_oil, 2),
            "E_oil": round(E_oil, 2),
            "k_gas": 0,
            "E_gas": 0,
            "E_total": round(E_coal + E_oil, 2)
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
