"""
Datamon

A math problem helper that helps students, teachers and parents
make math fun.

Haylee Kaheel Teresa Aryan James
"""
import operator

# A dictionary of operators and their corresponding functions
operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def check_answer(problem):
    
    try:
        equation, user_answer = problem.split('=')
        operator_symbol = None
        first_num = second_num = None

        matched = [(symbol, equation.split(symbol)) for symbol in operators if symbol in equation]

        if not matched or len(matched[0][1]) != 2:
            print("Invalid equation format.")
            return False

        operator_symbol, (left, right) = matched[0]
        first_num = float(left)
        second_num = float(right)

        operator_function = operators[operator_symbol]
        correct_answer = operator_function(first_num, second_num)

        if float(user_answer) == correct_answer:
            print("Correct!")
            return True
        else:
            print(f"Wrong! The correct answer is {correct_answer}.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def run_math_quiz():
    
    score = 0
    problem_count = 0

    while problem_count < 10:
        print(f"\nProblem {problem_count + 1}:")
        problem = input("Enter a math problem (e.g., 4+4=8): ").strip()
        if check_answer(problem):
            score += 1
        problem_count += 1

    print(f"\nYou answered {score} out of 10 problems correctly!")
    return score

if __name__ == "__main__":
    run_math_quiz()
