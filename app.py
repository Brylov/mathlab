from flask import Flask, render_template, request
import sympy as sp
from factor import Factor  # Your quadratic factor class

app = Flask(__name__)
factor = Factor()

@app.route('/')
def index():
    # Generate a new equation when the user first accesses the page
    equation, r1, r2 = factor.generate_factorable_quadratic()
    factor.equation = equation  # Store equation in Factor instance
    factor.correct_factors = str(sp.factor(equation))  # Store correct factored form
    return render_template('index.html', equation=factor.format_equation(equation))

@app.route('/solve', methods=['POST'])
def solve():
    user_answer = request.form['user_answer']
    correct_factors = factor.format_factored_form(sp.factor(factor.equation))
    result = "Correct!" if factor.check_ans(user_answer, factor.normalize_factors(correct_factors)) else "Incorrect"

    if result == "Correct!":
        # Display the correct answer and generate a new equation
        equation, r1, r2 = factor.generate_factorable_quadratic()
        factor.equation = equation  # Store new equation
        factor.correct_factors = str(sp.factor(equation))
        return render_template('index.html', equation=factor.format_equation(equation), result=result, 
                               correct_factors=correct_factors, new_equation=True)

    else:
        # If incorrect, show the result and allow the user to retry
        return render_template('index.html', equation=factor.format_equation(factor.equation), result=result, 
                               correct_factors=correct_factors)

@app.route('/new')
def new_equation():
    # Generate a new equation explicitly when requested
    equation, r1, r2 = factor.generate_factorable_quadratic()
    factor.equation = equation  # Store new equation
    factor.correct_factors = str(sp.factor(equation))  # Store correct factored form
    return render_template('index.html', equation=factor.format_equation(equation), result=None)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
