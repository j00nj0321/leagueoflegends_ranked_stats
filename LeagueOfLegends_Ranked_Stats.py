import riotapi_methods as rm

if __name__ == "__main__":
    
    print("Choose a simple menu (uses default values for params) or normal menu (user input params)")
    while True:
        print("\n1. simple menu    2. for normal menu    3. to exit")
        while True:
            try:
                menu_choice = int(input("1, 2, or 3: "))
                break
            except:
                print("choose a number 1, 2, or 3")
        if menu_choice == 1:
            rm.simple_menu()
        elif menu_choice == 2:
            rm.normal_menu()
        elif menu_choice == 3:
            break
        
        
