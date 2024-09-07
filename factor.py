import random
import sympy as sp
import re

class Factor:
    def __init__(self, difficulty='easy'):
        self.difficulty = difficulty  # Difficulty level for adjusting ranges
        self.current_problem = None

    def generate_problem(self):
        # List of functions for different polynomial types
        functions = [
            self.generate_factorable_quadratic,
            self.generate_cubic_problem,
            self.generate_mixed_polynomial,
            # self.generate_other_polynomial
        ]
        
        # Randomly select one function
        selected_function = random.choice(functions)
        
        # Generate and return the problem using the selected function
        return selected_function()

    def generate_factorable_quadratic(self):
        # Set ranges based on difficulty
        if self.difficulty == 'easy':
            r_min, r_max = -5, 5
            a_min, a_max = 1, 2
        elif self.difficulty == 'medium':
            r_min, r_max = -10, 10
            a_min, a_max = 1, 3
        else:  # Hard
            r_min, r_max = -20, 20
            a_min, a_max = 2, 5

        # Generate two random roots based on difficulty
        self.r1 = random.randint(r_min, r_max)
        self.r2 = random.randint(r_min, r_max)

        # Create coefficients a, b, c based on roots r1 and r2
        self.a = random.randint(a_min, a_max)
        self.b = -self.a * (self.r1 + self.r2)
        self.c = self.a * self.r1 * self.r2

        # Form the quadratic equation
        x = sp.symbols('x')
        equation = self.a * x**2 + self.b * x + self.c

        # Return the equation and its string representation
        return equation, self.format_equation(equation)

    def generate_cubic_problem(self):
        # Generate cubic problems with real rational roots
        x = sp.symbols('x')
        root1 = random.randint(-5, 5)
        root2 = random.randint(-5, 5)
        root3 = random.randint(-5, 5)
        
        # Create cubic polynomial with these roots
        polynomial = (x - root1) * (x - root2) * (x - root3)
        equation = sp.expand(polynomial)
        
        return equation, self.format_equation(equation)

    def generate_mixed_polynomial(self):
        # Generate mixed polynomials with real rational roots
        x, y = sp.symbols('x y')
        
        # Example: (x - a)(x - b)(y - c)
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        
        polynomial = (x - a) * (x - b) * (y - c)
        equation = sp.expand(polynomial)
        
        return equation, self.format_equation(equation)

    def generate_other_polynomial(self):
        # Generate polynomials with integer coefficients and real rational solutions
        x, n, k = sp.symbols('x n k')
        
        # Example: n(x - 1) - k(x + 1)
        n_value = random.randint(-5, 5)
        k_value = random.randint(-5, 5)
        
        polynomial = n * (x - 1) - k * (x + 1)
        equation = sp.expand(polynomial)
        
        return equation, self.format_equation(equation)

    def format_equation(self, equation):
        # Convert the equation to a string
        equation_str = str(equation)

        # Replace ** with superscript
        equation_str = re.sub(r'\*\*(\d+)', lambda match: self.superscript(match.group(1)), equation_str)

        # Remove multiplication signs for better readability
        equation_str = equation_str.replace('*', '')

        # Remove unnecessary spaces around operators
        equation_str = re.sub(r'\s*\+\s*', ' + ', equation_str)
        equation_str = re.sub(r'\s*-\s*', ' - ', equation_str)

        return equation_str

    def superscript(self, number):
        # Mapping digits to superscript characters
        superscripts = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
        return ''.join(superscripts[digit] for digit in number)

    def normalize_factors(self, factor_str):
        # Remove spaces and normalize the power notation
        factor_str = factor_str.replace(' ', '')

        # Extract and sort individual factors between parentheses
        factors = re.findall(r'\(.*?\)', factor_str)
        factors = [f.strip() for f in factors]

        # Replace `-` with `x -` and `+` with `x +` for consistency
        factors = [f.replace('x+', 'x + ').replace('x-', 'x - ') for f in factors]

        # Ensure numbers come before 'x' and replace them with each other
        factors = [re.sub(r'(\d+)(x)', r'\2\1', f) for f in factors]

        factors = sorted(factors)

        return factors

    def check_ans(self, ans, correct_factors):
        # Normalize the user's answer
        user_factors = self.normalize_factors(ans)
        print(correct_factors)
        # Compare sorted factors with correct sorted factors
        return user_factors == correct_factors
