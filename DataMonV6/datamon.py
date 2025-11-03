"""
Datamon

A math problem helper that helps students, teachers and parents
make math fun.

Haylee Kaheel Teresa Aryan James
"""
#tested code for pull request

from AnswerChecker import run_math_quiz
from memorybank import memory_main
from ElectroFlash import electro_flash

player_points = 0

def menu():
    
    print("\n" + "=" * 10 + " Menu " + "=" * 10)
    print("1) Answer Checker")
    print("2) Memory Bank")
    print("3) Electro Flash")
    print("4) Exit")
    print("=" * 26)

def main():
    
    global player_points
    choice = ""
    
    while choice != "4":
        print(f"\nTotal Points: {player_points}")
        menu()
        choice = input("Which one will you choose? ")

        if choice == "1":    
            print("\n--- Starting Answer Checker ---\n")
            player_points += run_math_quiz()
            
        elif choice == "2":
            print("\n--- Starting Memory Bank ---\n")
            player_points += memory_main()
            
        elif choice == "3":
            print("\n--- Starting Electro Flash ---\n")
            player_points += electro_flash()
            
        elif choice == "4":
            print(f"\nGoodbye! You earned a total of {player_points} points!")
            
        else:
            print("Please choose between 1 and 4.")

if __name__ == "__main__":
    main()
