from flask import Flask, request, jsonify

app = Flask(__name__)

# Define tax slabs and deductions
def calculate_tax(income, age, deductions):
    # Standard Deduction of ₹50,000
    standard_deduction = 50000
    income -= standard_deduction

    # Ensure deductions do not exceed maximum limits
    max_80c_deduction = 150000
    max_80d_deduction = 25000
    deduction_80c = min(deductions.get('section_80c', 0), max_80c_deduction)
    deduction_80d = min(deductions.get('section_80d', 0), max_80d_deduction)

    # Total applicable deductions
    total_deductions = deduction_80c + deduction_80d
    income -= total_deductions

    # Ensure taxable income is non-negative
    income = max(income, 0)

    # Tax calculation based on age and income slabs
    tax = 0

    if age < 60:
        # Tax Slabs for individuals below 60 years
        if income <= 250000:
            tax = 0
        elif income <= 500000:
            tax = (income - 250000) * 0.05
        elif income <= 1000000:
            tax = (500000 - 250000) * 0.05 + (income - 500000) * 0.20
        else:
            tax = (500000 - 250000) * 0.05 + (1000000 - 500000) * 0.20 + (income - 1000000) * 0.30
    elif 60 <= age < 80:
        # Tax Slabs for senior citizens (60–79 years)
        if income <= 300000:
            tax = 0
        elif income <= 500000:
            tax = (income - 300000) * 0.05
        elif income <= 1000000:
            tax = (500000 - 300000) * 0.05 + (income - 500000) * 0.20
        else:
            tax = (500000 - 300000) * 0.05 + (1000000 - 500000) * 0.20 + (income - 1000000) * 0.30
    else:
        # Tax Slabs for super senior citizens (80+ years)
        if income <= 500000:
            tax = 0
        elif income <= 1000000:
            tax = (income - 500000) * 0.20
        else:
            tax = (1000000 - 500000) * 0.20 + (income - 1000000) * 0.30

    # Apply rebate under Section 87A if income is less than ₹5,00,000
    if income <= 500000:
        tax = max(tax - 12500, 0)

    return round(tax, 2)

# Define the API route for tax calculation
@app.route('/tax_calculator_2', methods=['POST'])
def calculate_tax_endpoint():
    try:
        # Get the JSON data from the request
        data = request.json
        
        # Extracting income, age, and deductions from request
        income = data.get('income')
        age = data.get('age')
        deductions = data.get('deductions', {})

        # Check if income and age are provided and valid
        if income is None or not isinstance(income, (int, float)) or income < 0:
            return jsonify({"error": "Invalid income provided"}), 400
        if age is None or not isinstance(age, int) or age < 0:
            return jsonify({"error": "Invalid age provided"}), 400
        
        # Calculate the tax
        tax = calculate_tax(income, age, deductions)

        # Return the result as JSON
        return jsonify({"income": income, "age": age, "tax": tax}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
