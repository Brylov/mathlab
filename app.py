from flask import Flask, render_template, request
import sympy as sp
from factor import Factor
from bedmas import Bedmas

app = Flask(__name__)
factor = Factor()
bedmas = Bedmas()

@app.route('/')
def index():
    problem_type = request.args.get('type', 'quadratic')
    difficulty = request.args.get('difficulty', 'easy')  # Get difficulty from query parameters

    # Update the difficulty in the factor generator
    factor.difficulty = difficulty

    if problem_type == 'bedmas':
        problem, result = bedmas.generate_bedmas_problem()
        return render_template('index.html', problem_type=problem_type, problem=problem, result=None, difficulty=difficulty)
    else:
        equation, formatted_equation = factor.generate_problem()  # Generate a random problem
        factor.current_problem = equation  # Store the problem to use for checking answers
        return render_template('index.html', problem_type=problem_type, equation=formatted_equation, result=None, difficulty=difficulty)


@app.route('/solve', methods=['POST'])
def solve():
    user_answer = request.form['user_answer']
    problem_type = request.form['problem_type']

    if problem_type == 'bedmas':
        result = bedmas.check_answer(user_answer)
        if result == "Correct!":
            problem, _ = bedmas.generate_bedmas_problem()
            return render_template('index.html', problem_type=problem_type, problem=problem, result=result, new_problem=True)
        else:
            return render_template('index.html', problem_type=problem_type, problem=bedmas.current_problem, result=result)
    else:
        correct_factors = str(sp.factor(sp.sympify(factor.current_problem)))  # Calculate correct factors
        result = "Correct!" if factor.check_ans(user_answer, factor.normalize_factors(correct_factors)) else "Incorrect"
        if result == "Correct!":
            equation, formatted_equation = factor.generate_problem()  # Generate a new problem
            factor.current_problem = equation  # Update the current problem
            return render_template('index.html', equation=formatted_equation, result=result, new_equation=True)
        else:
            return render_template('index.html', equation=factor.format_equation(factor.current_problem), result=result)

@app.route('/new')
def new_problem():
    problem_type = request.args.get('type', 'quadratic')
    difficulty = request.args.get('difficulty', 'easy')

    # Update the difficulty in the factor generator
    factor.difficulty = difficulty

    if problem_type == 'bedmas':
        problem, _ = bedmas.generate_bedmas_problem()
        return render_template('index.html', problem_type=problem_type, problem=problem, difficulty=difficulty)
    else:
        equation, _ = factor.generate_problem()  # Generate a random problem
        factor.current_problem = equation  # Store the problem to use for checking answers
        return render_template('index.html', equation=factor.format_equation(equation), difficulty=difficulty)

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    difficulty = request.form['difficulty']
    problem_type = request.form['type']  # Get problem type from the form
    factor.difficulty = difficulty
    bedmas.difficulty = difficulty
    return render_template('index.html', problem_type=problem_type, difficulty=difficulty)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
