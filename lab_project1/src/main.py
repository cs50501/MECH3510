from ex1_1_part1visualize import main as run_ex1_1


def main():
    while True:
        print("\nChoose an exercise:")
        print("1. Exercise 1-1 (1) - Visualize both STL Files")
        print("2. Exercise 1-2")
        print("3. Exercise 1-3")
        print("4. Exercise 2")
        print("99. Terminate Program")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("Close the figure windows to return to the menu.")
            run_ex1_1()
        elif choice == "99":
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Please try again.")
        
    
if __name__ == "__main__":
    main()