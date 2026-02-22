
from datetime import datetime

# ---- Transaction Class ----
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now()

    def display_transaction(self):
        print(f"{self.timestamp} | {self.sender} sent ₹{self.amount} to {self.receiver}")

# ---- Wallet Class ----
class Wallet:
    def __init__(self):
        self.balance = 0
        self.history = []

    def add_money(self, amount):
        self.balance += amount
        print(f"₹{amount} added to wallet. Current Balance: ₹{self.balance}")

    def deduct_money(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            print("Insufficient Wallet Balance!")
            return False

    def show_balance(self):
        print(f"Wallet Balance: ₹{self.balance}")

    def add_transaction(self, transaction):
        self.history.append(transaction)

    def show_transaction_history(self):
        print("---- Transaction History ----")
        for t in self.history:
            t.display_transaction()

# ---- User Class ----
class User:
    def __init__(self, name, phone, upi_pin):
        self.name = name
        self.phone = phone
        self.__upi_pin = upi_pin
        self.wallet = Wallet()

    def verify_pin(self, pin):
        return self.__upi_pin == pin

# ---- Merchant Class ----
class Merchant(User):
    def __init__(self, name, phone, upi_pin, shop_name):
        super().__init__(name, phone, upi_pin)
        self.shop_name = shop_name

# ---- GPay System Class ----
class GPaySystem:
    def __init__(self):
        self.users = {}

    def register_user(self, name, phone, upi_pin):
        if phone in self.users:
            print("User already registered!")
        else:
            self.users[phone] = User(name, phone, upi_pin)
            print(f"User {name} Registered Successfully!")

    def register_merchant(self, name, phone, upi_pin, shop_name):
        if phone in self.users:
            print("Merchant already registered!")
        else:
            self.users[phone] = Merchant(name, phone, upi_pin, shop_name)
            print(f"Merchant {name} Registered Successfully!")

    def send_money(self, sender_phone, receiver_phone, amount, pin):
        sender = self.users.get(sender_phone)
        receiver = self.users.get(receiver_phone)

        if not sender or not receiver:
            print("Invalid Sender or Receiver!")
            return

        if not sender.verify_pin(pin):
            print("Invalid UPI PIN. Transaction Failed!")
            return

        if sender.wallet.deduct_money(amount):
            receiver.wallet.add_money(amount)
            transaction = Transaction(sender.name, receiver.name, amount)
            sender.wallet.add_transaction(transaction)
            receiver.wallet.add_transaction(transaction)
            print(f"Transaction of ₹{amount} Successful from {sender.name} to {receiver.name}")

    def show_user_balance(self, phone):
        user = self.users.get(phone)
        if user:
            user.wallet.show_balance()
        else:
            print("User not found!")

    def show_transaction_history(self, phone):
        user = self.users.get(phone)
        if user:
            user.wallet.show_transaction_history()
        else:
            print("User not found!")

gpay = GPaySystem()

gpay.register_user("vivek", "9876543210", "1234")
gpay.register_merchant("komal", "9999999999", "5678", "komal Electronics")


gpay.users["9876543210"].wallet.add_money(5000)

gpay.show_user_balance("9876543210")
gpay.show_user_balance("9999999999")

gpay.send_money("9876543210", "9999999999", 1500, "1234")

gpay.show_transaction_history("9876543210")
gpay.show_transaction_history("9999999999")
