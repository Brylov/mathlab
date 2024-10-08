import random
import sympy as sp
import re

class Factor:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.r1 = 0
        self.r2 = 0

    def generate_factorable_quadratic(self):
        # Generate two random roots
        self.r1 = random.randint(-10, 10)
        self.r2 = random.randint(-10, 10)

        # Create coefficients a, b, c based on roots r1 and r2
        self.a = random.randint(1, 5)  # Keep 'a' simple to make the equations more manageable
        self.b = -self.a * (self.r1 + self.r2)
        self.c = self.a * self.r1 * self.r2

        # Form the quadratic equation
        x = sp.symbols('x')
        equation = self.a * x**2 + self.b * x + self.c

        return equation, self.r1, self.r2

    def format_equation(self, equation):
        # Convert the equation to a string
        equation_str = str(equation)

        # Replace ** with superscript
        equation_str = re.sub(r'\*\*(\d+)', lambda match: self.superscript(match.group(1)), equation_str)

        # Remove multiplication signs for better readability
        equation_str = equation_str.replace('*', '')

        return equation_str

    def format_factored_form(self, factored_expr):
        # Convert the factored expression to a string
        factored_str = str(factored_expr)

        # Replace * with no space and handle power notation by converting ** to superscript
        formatted_str = factored_str.replace('*', '')

        # Convert powers (**) to superscript using Unicode
        formatted_str = re.sub(r'\*\*(\d+)', lambda match: self.superscript(match.group(1)), formatted_str)

        return formatted_str

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
        
        # Compare sorted factors with correct sorted factors
        return user_factors == correct_factors

def main():
    while True:
        factor = Factor()
        equation, r1, r2 = factor.generate_factorable_quadratic()

        # Format the quadratic equation as a string and apply superscript to powers
        equation_str = factor.format_equation(equation)

        # Display the quadratic equation to solve
        print(f"Solve the following quadratic equation by factoring:\n{equation_str} = 0")

        # Factor the equation using SymPy
        factored_form = sp.factor(equation)

        # Format and normalize the correct factored form
        formatted_factored_str = factor.format_factored_form(factored_form)
        normalized_correct_factors = factor.normalize_factors(formatted_factored_str)

        # Prompt the user for their answer
        user_answer = input("Enter the factored form (e.g., (x-1)(x+2)): ").strip()

        # Check if the user's answer matches the correct answer
        if factor.check_ans(user_answer, normalized_correct_factors):
            print("Correct! Well done.")
        else:
            print(f"Incorrect. The correct factored form is: {formatted_factored_str}")

        print(f"The roots are: x = {r1}, x = {r2}")

        # Ask the user if they want to solve another problem
        quit_choice = input("Do you want to solve another problem? (yes/no): ").strip().lower()
        if quit_choice != 'yes':
            print("Thank You")
            break

if __name__ == "__main__":
    main()
