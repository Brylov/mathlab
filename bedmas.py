import sympy as sp
import random

class Bedmas:
    def __init__(self):
        self.current_problem = ""
        self.difficulty = "medium"  # Default difficulty

    def generate_bedmas_problem(self):
        def get_random_number():
            return random.randint(1, 20)  # Ensure positive numbers

        def generate_random_expression(num_vars):
            if num_vars <= 1:
                return str(get_random_number())

            # Randomly choose an operator and build expressions recursively
            operators = ['+', '-', '*', ':']
            operator = random.choice(operators)
            left_vars = random.randint(1, num_vars - 1)
            right_vars = num_vars - left_vars

            left = generate_random_expression(left_vars)
            right = generate_random_expression(right_vars)

            if random.random() < 0.2:  # Add parentheses occasionally
                return f"({left} {operator} {right})"
            return f"{left} {operator} {right}"

        # Generate a number of variables between 4 and 8
        num_vars = random.randint(4, 8)
        
        # Generate the BEDMAS problem
        problem = generate_random_expression(num_vars)
        
        # Ensure the problem evaluates to a non-negative result
        try:
            expression = sp.sympify(problem)
            result = expression.evalf()
            while result < 0:
                num_vars = random.randint(4, 8)  # Adjust number of variables
                problem = generate_random_expression(num_vars)
                expression = sp.sympify(problem)
                result = expression.evalf()
        except:
            return self.generate_bedmas_problem()  # Retry on failure

        self.current_problem = problem
        return problem, result

    def check_answer(self, user_answer):
        try:
            correct_answer = int(sp.sympify(self.current_problem).evalf())
            print(correct_answer)
            return "Correct!" if int(correct_answer) == int(user_answer.strip()) else "Incorrect"
        except:
            return "Invalid expression"
