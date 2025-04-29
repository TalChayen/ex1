import os
import time
from Cellular_automaton_Basic import CellularAutomatonBasic
from gliders100 import GlidersAutomaton
from BehaviorsAndCycles import main as interesting_main

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu of the program."""
    clear_screen()
    print("\n===== CELLULAR AUTOMATON =====")
    print("1. Basic Cellular Automaton")
    print("2. Gliders Automaton")
    print("3. Interesting Behavior Automaton")
    print("4. Exit")
    print("========================================")
    print("\nPlease select an option (1-4): ")

def main():
    """Main function to run the menu and simulations."""
    while True:
        display_menu()
        choice = input().strip()
        
        if choice == '1':
            # Run basic cellular automaton
            basic_automaton = CellularAutomatonBasic()
            basic_automaton.run()
            print("\nReturning to menu...")
            time.sleep(2)
            
        elif choice == '2':
            # Run gliders automaton
            gliders_automaton = GlidersAutomaton()
            gliders_automaton.run()
            print("\nReturning to menu...")
            time.sleep(2)
            
        elif choice == '3':
            # Run interesting behavior automaton
            interesting_main()
            print("\nReturning to menu...")
            time.sleep(2)
            
        elif choice == '4':
            # Exit the program
            print("\nThank you for using the Cellular Automaton Simulator!")
            time.sleep(1)
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
            time.sleep(2)

if __name__ == "__main__":
    main()