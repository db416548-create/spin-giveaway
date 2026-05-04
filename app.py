from flask import Flask, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# stok hadiah (1x per produk)
stock = {
    "HG": 1,
    "PRIME": 1,
    "DRIP": 1
}

def get_reward():
    pool = []

    # hadiah utama kalau masih ada
    for k, v in stock.items():
        if v > 0:
            pool.append(k)

    # kalau semua habis
    if len(pool) == 0:
        return "HABIS"

    # zonk & bonus
    pool += ["ZONK"] * 70
    pool += ["BONUS"] * 20

    return random.choice(pool)

@app.route("/")
def home():
    return "Spin Giveaway Aktif!"

@app.route("/spin")
def spin():
    result = get_reward()

    if result in stock and stock[result] > 0:
        stock[result] -= 1

    code = result + "-" + str(random.randint(10000, 99999))

    return jsonify({
        "result": result,
        "code": code
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
