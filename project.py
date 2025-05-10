#credentials

CREDENTIALS_FILE = 'user.txt'
ACCOUNT_NUMBER_FILE = 'last_account_number.txt'
transaction_history_file ='transaction_history.txt'

accounts = { }
new_account_number = 508021  

def load_last_account_number():
    try:
        with open(ACCOUNT_NUMBER_FILE, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 508021


def save_last_account_number(account_number):
    with open(ACCOUNT_NUMBER_FILE, 'w') as f:
        f.write(str(account_number))


def read_credentials(file_path):
    creds = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    username, password, role = line.split(':')
                    creds[username] = {'password': password, 'role': role}
                except ValueError:
                    print(f"Skipping invalid line in credentials: {line}")
    except FileNotFoundError:
        print(f"Credentials file '{file_path}' not found. No users loaded🤔.")
    return creds



# Create a new bank account

def create_account():
    global new_account_number

    name = input('Enter your name: ')
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    print("Choose account type:")
    print("1. Saving_account💰")
    print("2. Current_account🏦")
    account_type_choice = input("Enter choice (1 or 2): ")

    if account_type_choice == '1':
        account_type = 'Saving_account'
    elif account_type_choice == '2':
        account_type = 'Current_accountS'
    else:
        print("Invalid account type selected😏.")
        return

    try:
        balance = float(input("Enter initial balance: "))
    except ValueError:
        print("Invalid input👎🏻. Balance must be a number.")
        return

    if balance < 0:
        print("Initial balance cannot be negative.")
        return

    #account details

    accounts[new_account_number] = {
        'name': name,
        'username': username,
        'password': password,
        'account_type': account_type,
        'balance': balance,
        'transactions': [f"{account_type} account created with balance {balance}"]
    }

    #account details to 'account_details.txt'

    with open('account_details.txt', 'a') as file:
        file.write(f'{new_account_number}:{name}:{username}:{account_type}:{balance}\n')
        

    #edentials file to 'user.txt'

    with open(CREDENTIALS_FILE, 'a') as file:
        file.write(f'{username}:{password}:user\n')

    with open(transaction_history_file, 'a') as file:
        file.write(f'{new_account_number}:Your Add Balance is:{balance}\n')

    print(f"{account_type} 🤗account created successfully!✅ Your account number is {new_account_number}")

    
    new_account_number += 1
    save_last_account_number(new_account_number)


# Deposit money 

def deposit_money():
    try:
        acc = int(input("Enter account number: "))
        
        
        with open("account_details.txt", 'r') as file:
            lines = file.readlines()
        
        account_found = False  
        updated_lines = []  
        
        for line in lines:
            getAcc = line.strip().split(":")  
            
            if int(getAcc[0]) == acc:
                account_found = True
                amount = float(input("Enter deposit amount: "))
                
                if amount <= 0:
                    print("Amount must be a positive number. ❌")
                else:
                    balance = float(getAcc[4])
                    balance += amount
                    getAcc[4] = str(balance)  
                    
                    print(f"New balance is: {balance} ✅")
                
                updated_lines.append(":".join(getAcc) + "\n")
            else:
                updated_lines.append(line)  

        if not account_found:
            print("Account does not exist. 😒👎🏻")
        
        
        with open("account_details.txt", 'w') as file:
            file.writelines(updated_lines)

        
        with open("transaction_history.txt", 'a') as file:
            file.write(f'{acc}:Your deposit amount is: {amount}\n')

        print("Deposit successful! ✅")

    except ValueError:
        print("Invalid input ❌.")


# Withdraw money 

def withdraw_money():
    try:
        acc = int(input('Enter account number: '))
        with open("account_details.txt", 'r') as file:
            lines = file.readlines()

        account_found = False  
        updated_lines = []  
        
        for line in lines:
            getAcc = line.strip().split(":")  
            
            if int(getAcc[0]) == acc:
                account_found = True
                amount = float(input("Enter withdraw amount: "))

                if amount <= 0:
                    print("Amount must be a positive number. ❌")
                else:
                    balance = float(getAcc[4])
                    balance -= amount
                    getAcc[4] = str(balance)  
                    
                    print(f"New balance is: {balance} ✅")
                
                updated_lines.append(":".join(getAcc) + "\n")
            else:
                updated_lines.append(line)  

        if not account_found:
            print("Account does not exist. 😒👎🏻")
        
        
        with open("account_details.txt", 'w') as file:
            file.writelines(updated_lines)

        
        with open("transaction_history.txt", 'a') as file:
            file.write(f'{acc}:Your withdraw amount is: {amount}\n')

        print("Withdraw successful! ✅")

    except ValueError:
        print("Invalid input ❌.")


# Check  balance

def check_balance():
    try:
        acc = int(input("Enter account number: "))
        with open("account_details.txt", 'r') as file:
            lines = file.readlines()
        
        account_found = False  
        updated_lines = []  
        
        for line in lines:
            getAcc = line.strip().split(":")  
            
            if int(getAcc[0]) == acc:
                account_found = True
                balance=getAcc[4]
                print(f"New balance is:{balance} ✅")
            updated_lines.append(":".join(getAcc) + "\n")
        
        else:
            updated_lines.append(line)
        if not account_found:
            print("Account does not exist😒.")

        with open("account_details.txt", 'w') as file:
            file.writelines(updated_lines)

        
        with open("transaction_history.txt", 'a') as file:
            file.write(f'{acc}:Your balance is: {balance}\n')

    except ValueError:
        print("Invalid input❌.")


#transaction history

def transaction_history():
    try:
        acc = int(input("Enter account number: "))
        
        # Read account details
        with open("account_details.txt", 'r') as file:
            lines = file.readlines()
        
        account_found = False

        for line in lines:
            getAcc = line.strip().split(":")  
            
            if int(getAcc[0]) == acc:
                account_found = True
                
                
                try:
                    with open("transaction_history.txt", 'r') as file:
                        transactions = file.readlines()
                    
                    print(f"Transaction history for account {acc}:")
                    
                    for transaction in transactions:
                        if transaction.startswith(f"{acc}:"):
                            print(transaction.strip())  # Display transactions
                    
                except FileNotFoundError:
                    print("No transaction history found.")

        if not account_found:
            print("Account does not exist 😒.")

    except ValueError:
        print("Invalid input ❌.")


#Main banking menu-driven interface

def main_menu():
    while True:
        print("\n-----🏦💸Mini Banking System💸🏦-----")
        print("1. Create account🪪")
        print("2. Deposit money💸")
        print("3. Withdraw money💴")
        print("4. Check balance💰")
        print("5. Transaction history💱")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            transaction_history()
        elif choice == '6':
            print("🏦😉Thank you for using the Mini Banking System!!🫡🙏.")
            break
        else:
            print("Invalid option. Please choose between 1 to 6😊.")

def user_menu():
    while True:
        print("\n-----🏦💸Mini Banking System💸🏦-----")
        print("1. Deposit money💸")
        print("2. Withdraw money💴")
        print("3. Check balance💰")
        print("4. Transaction history💱")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")
        if choice == '1':
            deposit_money()
        elif choice == '2':
            withdraw_money()
        elif choice == '3':
            check_balance()
        elif choice == '4':
            transaction_history()
        elif choice == '5':
            print("🏦😉Thank you for using the Mini Banking System🫡🙏.")
            break
        else:
            print("Invalid option. Please choose between 1 to 5😊.")


# Login system based on credentials

def login(creds):
    input_username = input("Enter the username: ")
    input_password = input("Enter the password: ")

    if input_username in creds and creds[input_username]['password'] == input_password:
        role = creds[input_username]['role']
        print(f"Login successful✅. Role: {role}")
        if role in ['admin']:
            main_menu()
        else:
            role in ['user']
            user_menu()
    else:
        print("Login failed. Wrong credentials😒❌.")


# Main entry point

def main():
    global new_account_number
    new_account_number = load_last_account_number()
    creds = read_credentials(CREDENTIALS_FILE)
    login(creds)


main()