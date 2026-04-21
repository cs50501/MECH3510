from ex1_1_1 import main as run_ex1_1_1
from ex1_1_2 import main as run_ex1_1_2
from ex1_1_3 import main as run_ex1_1_3
from ex1_2 import main as run_ex1_2
from ex1_3_1 import main as run_ex1_3_1
from ex1_3_2 import main as run_ex1_3_2
from ex1_3_3 import main as run_ex1_3_3


def main():
    while True:
        print("\nChoose an exercise (Type a number):")
        print("1. Exercise 1-1 (1) - Visualize both STL Files")
        print("2. Exercise 1-1 (2) - Rotate the STL Files")
        print("3. Exercise 1-1 (3) - Calculate Total Surface Areas of the STL Files")
        print("4. Exercise 1-2 - Program Periodic Surfaces")
        print("5. Exercise 1-3 (1) - Visualize a sphere")
        print("6. Exercise 1-3 (2) - Visualize union of box and cylinder")
        print("7. Exercise 1-3 (3) - Generate metamorphosis")
        print("99. Terminate Program")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("Close the figure windows to return to the menu.")
            run_ex1_1_1()
        elif choice == "2":
            print("Close the figure windows to return to the menu.")
            run_ex1_1_2()
        elif choice == "3":
            run_ex1_1_3()
        elif choice == "4":
            run_ex1_2()
            print("Close the figure windows to return to the menu.")
        elif choice == "5":
            run_ex1_3_1()
            print("Close the figure windows to return to the menu.")
        elif choice == "6":
            run_ex1_3_2()
            print("Close the figure windows to return to the menu.")
        elif choice == "7":
            run_ex1_3_3()
            print("Close the figure windows to return to the menu.")
        elif choice == "99":
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Please try again.")
        
    
if __name__ == "__main__":
    main()