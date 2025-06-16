import streamlit as st
import json
import string
import random
from pathlib import Path

class Bank:
    database = "data.json"
    data = []

    # Load existing data
    try:
        if Path(database).exists():
            with open(database, "r") as file:
                data = json.load(file)
        else:
            st.info("📂 No existing data file found. A new one will be created.")
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")

    @classmethod
    def __add_data(cls):
        with open(cls.database, "w") as file:
            file.write(json.dumps(Bank.data))

    @classmethod
    def __accountno_gene(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        numb = random.choices(string.digits, k=4)
        spchars = random.choices("!@#$%^&*", k=1)
        id = alpha + numb + spchars
        random.shuffle(id)
        return "".join(id)

    def create_account(self):
        st.header("🔐 Create New Bank Account")
        name = st.text_input("Enter your name")
        age = st.number_input("Enter your age", min_value=0)
        email = st.text_input("Enter your email")
        contact_no = st.text_input("Enter your contact number")
        cnic = st.text_input("Enter your CNIC number")
        pin = st.text_input("Set a 4-digit PIN", type="password")

        if st.button("Create Account"):
            if age < 18 or "@" not in email or len(pin) != 4:
                st.warning("❌ Make sure age is 18+, email is valid, and PIN is 4 digits.")
            else:
                info = {
                    "name": name,
                    "age": age,
                    "email": email,
                    "contact_no": int(contact_no),
                    "CNIC_no": int(cnic),
                    "pin": int(pin),
                    "balance": 0,
                    "account_no": Bank.__accountno_gene()
                }
                Bank.data.append(info)
                Bank.__add_data()
                st.success("✅ Account created successfully!")
                st.json(info)

    def deposite_money(self):
        st.header("💰 Deposit Money")
        acc_no = st.text_input("Enter account number")
        pin = st.text_input("Enter your PIN", type="password")
        amount = st.number_input("Enter amount to deposit", min_value=0)

        if st.button("Deposit"):
            user_data = [i for i in Bank.data if i["account_no"] == acc_no and str(i["pin"]) == pin]
            if not user_data:
                st.error("❌ No matching account found.")
            elif amount > 20000:
                st.warning("⚠️ Max deposit limit is Rs.20,000.")
            else:
                user_data[0]["balance"] += amount
                Bank.__add_data()
                st.success(f"✅ Rs.{amount} deposited successfully!")

    def withdraw_money(self):
        st.header("🏧 Withdraw Money")
        acc_no = st.text_input("Enter account number")
        pin = st.text_input("Enter your PIN", type="password")
        amount = st.number_input("Enter amount to withdraw", min_value=0.0)

        if st.button("Withdraw"):
            user_data = [i for i in Bank.data if i["account_no"] == acc_no and str(i["pin"]) == pin]
            if not user_data:
                st.error("❌ No matching account found.")
            elif user_data[0]["balance"] < amount:
                st.warning("❌ Insufficient balance.")
            else:
                user_data[0]["balance"] -= amount
                Bank.__add_data()
                st.success(f"✅ Rs.{amount} withdrawn successfully!")

    def show_details(self):
        st.header("📄 View Account Details")
        acc_no = st.text_input("Enter account number")
        pin = st.text_input("Enter your PIN", type="password")

        if st.button("Show Details"):
            user_data = [i for i in Bank.data if i["account_no"] == acc_no and str(i["pin"]) == pin]
            if not user_data:
                st.error("❌ No matching account found.")
            else:
                st.subheader("🔎 Account Information")
                st.json(user_data[0])

    def update_details(self):
        st.header("✏️ Update Account Details")
        acc_no = st.text_input("Enter account number")
        pin = st.text_input("Enter your PIN", type="password")

        if st.button("Verify"):
            user_data = [i for i in Bank.data if i["account_no"] == acc_no and str(i["pin"]) == pin]
            if not user_data:
                st.error("❌ No matching account found.")
                return

            name = st.text_input("New Name", value=user_data[0]["name"])
            contact_no = st.text_input("New Contact No", value=str(user_data[0]["contact_no"]))
            new_email = st.text_input("New Email", value=user_data[0]["email"])
            new_pin = st.text_input("New PIN", value=str(user_data[0]["pin"]))

            if st.button("Update"):
                user_data[0]["name"] = name
                user_data[0]["contact_no"] = int(contact_no)
                user_data[0]["email"] = new_email
                user_data[0]["pin"] = int(new_pin)
                Bank.__add_data()
                st.success("✅ Account details updated.")

    def delete_account(self):
        st.header("🗑️ Delete Account")
        acc_no = st.text_input("Enter account number")
        pin = st.text_input("Enter your PIN", type="password")

        if st.button("Delete Account"):
            user_data = [i for i in Bank.data if i["account_no"] == acc_no and str(i["pin"]) == pin]
            if not user_data:
                st.error("❌ No matching account found.")
            else:
                Bank.data.remove(user_data[0])
                Bank.__add_data()
                st.success("✅ Account deleted successfully.")


# -------------------- Streamlit UI ------------------------

bank = Bank()

st.title("💼 Python Bank Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    (
        "🏦 Create Account",
        "💰 Deposit Money",
        "🏧 Withdraw Money",
        "📄 View Account Details",
        "✏️ Update Account Info",
        "🗑️ Delete Account"
    )
)

if menu == "🏦 Create Account":
    bank.create_account()
elif menu == "💰 Deposit Money":
    bank.deposite_money()
elif menu == "🏧 Withdraw Money":
    bank.withdraw_money()
elif menu == "📄 View Account Details":
    bank.show_details()
elif menu == "✏️ Update Account Info":
    bank.update_details()
elif menu == "🗑️ Delete Account":
    bank.delete_account()


