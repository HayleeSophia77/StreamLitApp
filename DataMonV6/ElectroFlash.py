"""
Datamon

A math problem helper that helps students, teachers and parents
make math fun.

Haylee Kaheel Teresa Aryan James
"""
import random
import time

def electro_flash():
    
    print("Welcome to Electro Flash!")
    print("Practice your math tables the fun way and defeat AntiMath!\n")

    try:
        table = int(input("Pick a base number (e.g. 5): "))
    except ValueError:
        print("Invalid input. Defaulting to 2.")
        table = 2

    operation = input("Choose operation (+, -, *, /): ").strip()
    if operation not in ['+', '-', '*', '/']:
        print("Invalid choice. Defaulting to multiplication (*).")
        operation = '*'

    print(f"\nGreat! Let's practice {table} {operation} problems.")
    print("You'll get 5 problems. Each problem gives you 2 tries.\n")

    start_time = time.time()
    score = 0
    total_questions = 5
    
    numbers = list(range(1, 13))
    random.shuffle(numbers)

    for i in range(total_questions):
        num = numbers[i]
        got_it = False
        
        if operation == '+':
            first = table
            second = num
            correct_answer = first + num
        
        elif operation == '-':
            first = num + table
            second = table
            correct_answer = first - table
            
        elif operation == '*':
            first = table
            second = num
            correct_answer = first * num
            
        elif operation == '/':
            first = num * table
            second = table
            correct_answer = round(first / table, 2)

        attempt = 0
        while attempt < 2 and got_it == False:
            try:
                ans = float(input(f"Problem {i + 1}: {first} {operation} {second} = "))
                if abs(ans - correct_answer) < 0.01:
                    print("Correct!\n")
                    score = score + 1
                    got_it = True
                else:
                    print("Try again.")
            except ValueError:
                print("Please enter a number.")
            attempt = attempt + 1
        
        if got_it == False:
            print(f"Answer was {correct_answer}\n")
            
    elapsed = round(time.time() - start_time, 2)
    print(f"Game Over!\nScore: {score}/{total_questions}\nTime: {elapsed} secounds")
    
    if score == total_questions:
        print("Amazing! You're lighting fast! AntiMath won't stand a chance!")
        
    return score