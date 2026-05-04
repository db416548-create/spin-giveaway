from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# stok hadiah (1x saja)
stock = {
    "HG": 1,
    "PRIME": 1,
    "DRIP": 1
}

codes = {}
used_ip = set()


def get_reward():
    pool = []

    for k, v in stock.items():
        if v > 0:
            pool.append(k)

    if len(pool) == 0:
        return "HABIS"

    pool += ["ZONK"] * 70
    pool += ["BONUS"] * 20

    return random.choice(pool)


@app.route("/spin")
def spin():
    user_ip = request.remote_addr

    # limit 1x per IP
    if user_ip in used_ip:
        return jsonify({"result": "LIMIT", "code": "-"})

    used_ip.add(user_ip)

    result = get_reward()

    if result == "HABIS":
        return jsonify({"result": "HABIS", "code": "-"})

    if result in stock:
        stock[result] -= 1

    code = result + "-" + str(random.randint(10000, 99999))

    codes[code] = {
        "reward": result,
        "used": False
    }

    return jsonify({
        "result": result,
        "code": code
    })


@app.route("/redeem", methods=["POST"])
def redeem():
    code = request.json.get("code")

    if code not in codes:
        return jsonify({"status": "invalid"})

    if codes[code]["used"]:
        return jsonify({"status": "used"})

    codes[code]["used"] = True

    return jsonify({
        "status": "success",
        "reward": codes[code]["reward"]
    })


app.run(host="0.0.0.0", port=5000)
