from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home4.html')

def new_tax(income):
    n = 400000
    if income <= 1200000:
        tax = 0
    elif income <= 1600000:
        tax = 0 + (n * 0.05) + (n * 0.1) + (income - 1200000) * 0.15
    elif income <= 2000000:
        tax = 0 + (n * 0.05) + (n * 0.1) + (n * 0.15) + (income - 1600000) * 0.2
    elif income <= 2400000:
        tax = 0 + (n * 0.05) + (n * 0.1) + (n * 0.15) + (n * 0.2) + (income - 2000000) * 0.25
    else:
        tax = 0 + (n * 0.05) + (n * 0.1) + (n * 0.15) + (n * 0.2) + (n * 0.25) + (income - 2400000) * 0.3

    effect = (tax / income * 100) if income > 0 else 0
    return tax, effect

def old_tax(income):
    n = 300000
    if income <= 700000:
        tax = 0
    elif income <= 900000:
        tax = (n * 0.05) + (income - 600000) * 0.1
    elif income <= 1200000:
        tax = (n * 0.05) + (n * 0.1) + (income - 900000) * 0.15
    elif income <= 1500000:
        tax = (n * 0.05) + (n * 0.1) + (n * 0.15) + (income - 1200000) * 0.2
    else:
        tax = (n * 0.05) + (n * 0.1) + (n * 0.15) + (n * 0.2) + (income - 1500000) * 0.3

    effect = (tax / income * 100) if income > 0 else 0
    return tax, effect

@app.route('/calculate_tax', methods=['GET'])
def calculate_tax():
    try:
        income = int(request.args.get('income'))

        new_tax_value, new_effect = new_tax(income)
        old_tax_value, old_effect = old_tax(income)

        return jsonify({
            "income": income,
            "new_regime": {
                "tax_payable": round(new_tax_value, 2),
                "effective_tax_rate": round(new_effect, 2)
            },
            "old_regime": {
                "tax_payable": round(old_tax_value, 2),
                "effective_tax_rate": round(old_effect, 2)
            }
        })
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. Please provide a valid income."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
