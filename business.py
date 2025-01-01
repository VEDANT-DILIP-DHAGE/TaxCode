from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

def calculate_tax(total_income, tax_option, surcharge_rate):
    tax_rates = {
        'normal': 0.30,
        '115BA_less_400Cr': 0.25,
        '115BA_more_400Cr': 0.25,
        '115BAA': 0.22,
        '115BAB': 0.15
    }

    # Step 1: Calculate base tax based on tax option
    base_tax = total_income * tax_rates[tax_option]

    # Step 2: Calculate surcharge based on surcharge rate
    surcharge = base_tax * (float(surcharge_rate) / 100)

    # Step 3: Add Health & Education Cess (4%)
    cess = (base_tax + surcharge) * 0.04

    # Step 4: Calculate total tax
    total_tax = base_tax + surcharge + cess

    return {
        'base_tax': base_tax,
        'surcharge': surcharge,
        'cess': cess,
        'total_tax': total_tax
    }

@app.route('/calculate_business_tax', methods=['POST'])
def calculate_business_tax():
    data = request.get_json()

    total_income = data.get('totalIncome')
    deductions80IAIAC = data.get('deductions80IAIAC')
    donations80G = data.get('donations80G')
    tax_option = data.get('taxOption')
    surcharge_rate = data.get('surcharge')

    if deductions80IAIAC == '80IA' or deductions80IAIAC == '80IAC':
        return jsonify({
            'totalIncome': total_income,
            'totalDeductions': 0,
            'taxableIncome': 0,
            'incomeTax': 0,
            'surcharge': 0,
            'cess': 0,
            'totalTax': 0,
            'message': "Your tax is NIL due to Section 80IA/80IAC deductions."
        })

    # Calculate deductions and taxable income
    taxable_income = total_income - donations80G

    # Calculate tax
    tax_data = calculate_tax(taxable_income, tax_option, surcharge_rate)

    return jsonify({
        'totalIncome': total_income,
        'totalDeductions': donations80G,
        'taxableIncome': taxable_income,
        'incomeTax': tax_data['base_tax'],
        'surcharge': tax_data['surcharge'],
        'cess': tax_data['cess'],
        'totalTax': tax_data['total_tax']
    })

if __name__ == '__main__':
    app.run(debug=True)
