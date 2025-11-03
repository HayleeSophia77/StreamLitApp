"""
Datamon

A math problem helper that helps students, teachers and parents
make math fun.

Haylee Kaheel Teresa Aryan James
"""
import random
import ast
import operator

# Supported operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
    
    }

def memory_menu():
    '''
    displays the menu for memory bank.

    Returns
    -------
    None.

    '''
    print()
    print("=" * 10 + " Memory Bank Menu " + "=" * 10)
    print("1) Add problems to the memory bank.")
    print("2) Practice memory bank problems.")
    print("3) Return to the main menu.")
    print("=" * 36)


def fun_feedback(correct, attempts):
    '''
    Depending on how many the user got correct and the attempts will display
    a special message for the user.

    Parameters
    ----------
    correct : integar
        how many problems user got right.
    attempts : int
        number of attempts it took user.

    Returns
    -------
    str
        message to user based on scores.

    '''
    if correct == attempts and attempts != 0:
        return "Perfect score! You're a math wizard!"
    elif correct > attempts * 0.75:
        return "Great job! You really know your stuff."
    elif correct > attempts * 0.5:
        return "Not bad! Keep practicing and you'll get even better."
    elif correct > 0:
        return "You got some right! Don’t give up — try again!"
    else:
        return "Oof, tough round! Time to hit the books."

def memory_addproblems():
    '''
    Allows user to add problems to the memory bank to practice.

    Returns
    -------
    problems - list
        returns the list of the problems added.

    '''
    try:
        #gets info from user
        num_of_problems = int(input("How many problems to add? (max 10): "))
        #evaluates the users input
        if num_of_problems > 10: 
            num_of_problems = 10
        elif num_of_problems < 1:
            print("Number must be at least 1.")
            return []
        
        problems = []
        #allows user to enter the problems for the memory bank.
        for i in range(num_of_problems):
            valid_problem = False
            while not valid_problem:
                problem_input = input(f"Enter problem {i+1} (ex: 5+5): ").strip()
                try:
                    safe_eval(problem_input)
                    problems.append(problem_input)
                    valid_problem = True  # Exit the while loop by setting flag
                except ValueError as ve:
                    print(f"\nInvalid math expression: {ve}. Please try again.")
                except Exception as e:
                    print(f"\nError: {e}. Please try again.")
            
        return problems

    except ValueError:
        print("\nInvalid input. Please enter an integer.")
        return []
    except Exception as err:
        print(f"\nError: {err}")
        return []




def safe_eval(expr):
    """
    Safely evaluate a mathematical expression string using AST parsing.
    Supports +, -, *, /, ** and parentheses.
    """
    def _eval(node):
        
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            op_func = OPERATORS[type(node.op)]
            return op_func(_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):  # unary operations like -1
            op_func = OPERATORS[type(node.op)]
            return op_func(_eval(node.operand))
        else:
            raise TypeError(f"Unsupported type: {node}")
    
    try:
        node = ast.parse(expr, mode='eval')
        return _eval(node)
    except Exception as e:
        raise ValueError(f"Invalid expression: {expr}. Error: {e}")

def memory_bank(problems):
    '''
    prompts user to answer the problem, keeps track of how many questions were
    correct or wrong. Gives user up to 3 tries per problem.

    Parameters
    ----------
    problems : List
        List of problems added to the memory bank.

    Returns
    -------
    None.
    '''
    
    if not problems:
        print("\nNo problems available. Please add problems first.")
        return 0
    
    attempts = 0
    correct_answers = 0
    
    num_problems = len(problems)
    problems_copy = problems.copy()
    
    for _ in range(num_problems):
        rand_index = random.randint(0, len(problems_copy) - 1)
        problem = problems_copy.pop(rand_index)
        print(f"\nSolve this: {problem}")
        
        try:
            answer_checker = safe_eval(problem)
        except Exception as e:
            print(f"Error evaluating problem '{problem}': {e}")
            attempts += 1
            answer_checker = None
        
        if answer_checker is not None:
            tries_left = 3
            correct = False
        
        while tries_left > 0 and not correct:
            try:
                user_answer = float(input(f"Your answer (tries left: {tries_left}): "))
                attempts += 1
                
                if abs(user_answer - answer_checker) < 1e-6:
                    print("Correct!")
                    correct_answers += 1
                    correct = True
                else:
                    print("Incorrect.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                attempts += 1
            
            tries_left -= 1
        
        if not correct:
            print(f"The correct answer was: {answer_checker}")
    
    print(f"\nYou got {correct_answers} correct out of {attempts} attempts.")
    print(fun_feedback(correct_answers, attempts))
    return correct_answers


def memory_main():
    '''
    main memory bank while loop.

    Returns
    -------
    None.

    '''
    problems = []
    option = 0
    total_points = 0
    
    while option != 3:
        memory_menu()
        try:
            option = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input, please enter a number between 1 and 3.")
            option = 0
        
        if option == 1:
            print("Add problems to the memory bank.")
            new_problems = memory_addproblems()
            if new_problems:
                problems.extend(new_problems)
                print(f"Added {len(new_problems)} problem(s).")
            else:
                print("No problems were added.")
                
        elif option == 2:
            print("Practice Memory Problems.")
            points = memory_bank(problems)
            total_points += points
            
        elif option == 3:
            print("\nReturning to main menu!")
            
    return total_points

    
    

