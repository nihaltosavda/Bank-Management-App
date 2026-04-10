import streamlit as st
import json
import random
import string
from pathlib import Path
import hashlib

# ---------------- STORAGE LAYER ---------------- #
class Storage:
    FILE = "data.json"

    @staticmethod
    def load():
        if Path(Storage.FILE).exists():
            with open(Storage.FILE, "r") as f:
                return json.load(f)
        return []

    @staticmethod
    def save(data):
        with open(Storage.FILE, "w") as f:
            json.dump(data, f, indent=4)


# ---------------- SERVICE LAYER ---------------- #
class BankService:
    def __init__(self):
        self.data = Storage.load()

    def _save(self):
        Storage.save(self.data)

    def _generate_account_number(self):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=8))

    def _hash_pin(self, pin):
        return hashlib.sha256(pin.encode()).hexdigest()

    def create_account(self, name, age, email, pin):
        if age < 18 or len(pin) != 4:
            return False, "Invalid age or PIN"

        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": self._hash_pin(pin),
            "account_number": self._generate_account_number(),
            "balance": 0,
        }

        self.data.append(account)
        self._save()
        return True, account

    def authenticate(self, acc, pin):
        hashed = self._hash_pin(pin)
        for user in self.data:
            if user["account_number"] == acc and user["pin"] == hashed:
                return user
        return None

    def deposit(self, acc, pin, amount):
        user = self.authenticate(acc, pin)
        if not user:
            return False, "Invalid credentials"

        if amount <= 0 or amount > 10000:
            return False, "Invalid deposit amount"

        user["balance"] += amount
        self._save()
        return True, f"New Balance: {user['balance']}"

    def withdraw(self, acc, pin, amount):
        user = self.authenticate(acc, pin)
        if not user:
            return False, "Invalid credentials"

        if user["balance"] < amount:
            return False, "Insufficient balance"

        user["balance"] -= amount
        self._save()
        return True, f"New Balance: {user['balance']}"

    def get_details(self, acc, pin):
        user = self.authenticate(acc, pin)
        if not user:
            return False, "Invalid credentials"
        return True, user

    def delete_account(self, acc, pin):
        user = self.authenticate(acc, pin)
        if not user:
            return False, "Invalid credentials"

        self.data.remove(user)
        self._save()
        return True, "Account deleted"


# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="Bank App", layout="centered")
st.title("🏦 Simple Bank System")

bank = BankService()

menu = st.sidebar.selectbox("Menu", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Check Details",
    "Delete Account"
])

# ---------------- CREATE ACCOUNT ---------------- #
if menu == "Create Account":
    st.subheader("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create"):
        success, result = bank.create_account(name, age, email, pin)
        if success:
            st.success("Account created!")
            st.json(result)
        else:
            st.error(result)

# ---------------- DEPOSIT ---------------- #
elif menu == "Deposit":
    st.subheader("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        success, msg = bank.deposit(acc, pin, amount)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# ---------------- WITHDRAW ---------------- #
elif menu == "Withdraw":
    st.subheader("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        success, msg = bank.withdraw(acc, pin, amount)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# ---------------- DETAILS ---------------- #
elif menu == "Check Details":
    st.subheader("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Get Details"):
        success, data = bank.get_details(acc, pin)
        if success:
            st.json(data)
        else:
            st.error(data)

# ---------------- DELETE ---------------- #
elif menu == "Delete Account":
    st.subheader("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        success, msg = bank.delete_account(acc, pin)
        if success:
            st.success(msg)
        else:
            st.error(msg)