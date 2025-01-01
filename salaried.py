from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests


# Individual Income Tax Calculation (for salaried individuals)
@app.route('/calculate_tax', methods=['POST'])
def calculate_tax():
    data = request.json
    age_group = data['ageGroup']
    gross_income = data['grossIncome']

    # Deductions
    section80C = min(data['section80C'], 150000)  # Max limit for Section 80C
    section80D = min(data['section80D'], 25000)   # Max limit for Section 80D
    section80E = data['section80E']  # No limit for 80E
    section80G = data['section80G']  # Depends on eligible donations

    # Total deductions
    deductions = section80C + section80D + section80E + section80G
    taxable_income = gross_income - deductions  # Deduct from gross income

    # Apply appropriate tax slab based on age group
    if age_group == "below60":
        tax = calculate_tax_slab(taxable_income)
    elif age_group == "60to80":
        tax = calculate_tax_slab(taxable_income)
    elif age_group == "above80":
        tax = calculate_tax_slab(taxable_income)

    # Apply 4% cess
    tax_with_cess = tax + (tax * 0.04)

    return jsonify({"tax": round(tax_with_cess, 2)})


def calculate_tax_slab(income):
    if income <= 300000:
        return 0
    elif income <= 600000:
        return (income - 300000) * 0.05
    elif income <= 900000:
        return 15000 + (income - 600000) * 0.10
    elif income <= 1200000:
        return 45000 + (income - 900000) * 0.15
    elif income <= 1500000:
        return 90000 + (income - 1200000) * 0.20
    else:
        return 150000 + (income - 1500000) * 0.30


# Corporate/Business Tax Calculation
def calculate_business_tax_logic(total_income, tax_option, surcharge_rate):
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
            'cess': 0,+
            'totalTax': 0,
            'message': "Your tax is NIL due to Section 80IA/80IAC deductions."
        })

    # Calculate deductions and taxable income
    taxable_income = total_income - donations80G

    # Calculate tax
    tax_data = calculate_business_tax_logic(taxable_income, tax_option, surcharge_rate)

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
