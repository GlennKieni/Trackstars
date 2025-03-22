import auth_routes

def main():
    while True:
        print("\n1. Signup")
        print("2. Login")
        print("3. Change Role")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (default is 'user'): ") or "user"
            auth_routes.signup(username, password, role)

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            auth_routes.login(username, password)

        elif choice == '3':
            username = input("Enter username: ")
            new_role = input("Enter new role: ")
            auth_routes.change_role(username, new_role)

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
