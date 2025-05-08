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
    print("1. Savings💰")
    print("2. Checking🏦")
    account_type_choice = input("Enter choice (1 or 2): ")

    if account_type_choice == '1':
        account_type = 'Savings'
    elif account_type_choice == '2':
        account_type = 'Checking'
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
        if acc not in accounts:
            print("Account does not exist😒👎🏻.")
            return
        amount = float(input("Enter deposit amount: "))
        if amount <= 0:
            print("Amount must be a positive number.")
            return
        accounts[acc]["balance"] += amount
        accounts[acc]["transactions"].append(f"Deposited: {amount}")

        print("Deposit successfully!✅")
        with open(transaction_history_file, 'a') as file:
            file.write(f'{new_account_number}:Your deposit amount is:{amount}\n')
    except ValueError:
        print("Invalid input❌.")


# Withdraw money 
def withdraw_money():
    try:
        acc = int(input('Enter account number: '))
        if acc not in accounts:
            print("Account does not exist😒.")
            return
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return

        account_type = accounts[acc].get('account_type', 'Savings')
        balance = accounts[acc]['balance']

        if account_type == 'Checking':
            overdraft_limit = 500
            if amount > balance + overdraft_limit:
                print("Overdraft limit exceeded🤷‍♂.")
                return
        else:
            if amount > balance:
                print("Insufficient balance😏.")
                return

        accounts[acc]['balance'] -= amount
        accounts[acc]['transactions'].append(f"Withdraw: {amount}")
        print("Withdrawal successful💴✅.")

        with open(transaction_history_file, 'a') as file:
            file.write(f'{new_account_number}:Your withdraw amount is:{amount}\n')
    except ValueError:
        print("Invalid input❌.")


# Check  balance
def check_balance():
    try:
        acc = int(input("Enter account number: "))
        if acc in accounts:
            print(f"Account Type: {accounts[acc].get('account_type', 'Unknown')}")
            print(f"Current balance: {accounts[acc]['balance']}")
        else:
            print("Account does not exist😒.")
    except ValueError:
        print("Invalid input❌.")


#transaction history
def transaction_history():
    try:
        acc = int(input("Enter account number: "))
        if acc in accounts:
            print(f"Account Type: {accounts[acc].get('account_type', 'Unknown')}")
            print("💸Transaction history:")
            for t in accounts[acc]['transactions']:
                print("-", t)

                
        else:
            print("Account does not exist😒.")
    except ValueError:
        print("Invalid input❌.")


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
            print("🏦😉Thank you for using the Mini Banking System🫡🙏.")
            break
        else:
            print("Invalid option. Please choose between 1 to 6😊.")


# Login system based on credentials
def login(creds):
    input_username = input("Enter the username: ")
    input_password = input("Enter the password: ")

    if input_username in creds and creds[input_username]['password'] == input_password:
        role = creds[input_username]['role']
        print(f"Login successful✅. Role: {role}")
        if role in ['admin', 'user']:
            main_menu()
    else:
        print("Login failed. Wrong credentials😒❌.")


# Main entry point
def main():
    global new_account_number
    new_account_number = load_last_account_number()
    creds = read_credentials(CREDENTIALS_FILE)
    login(creds)


main()