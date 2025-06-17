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
    def __update(cls):
        with open(cls.database, "w") as file:
            json.dump(cls.data, file, indent=4)

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
            if not name or not age or not email or not contact_no or not cnic or not pin:
                st.warning("❌ Please fill these fields")
            elif age < 18 or "@" not in email or len(pin) != 4:
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
                Bank.__update()
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
                Bank.__update()
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
                Bank.__update()
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

        if "verified" not in st.session_state:
            st.session_state.verified = False
        if "user_data" not in st.session_state:
            st.session_state.user_data = None

        acc_no = st.text_input("Enter your account no")
        pin = st.text_input("Enter your 4 digit PIN", type="password")

        if st.button("Verify"):
            try:
                pin_int = int(pin)
            except ValueError:
                st.error("❌ PIN must be a number.")
                return

            user_data = [i for i in Bank.data if i["account_no"] == acc_no and i["pin"] == pin_int]
            if not user_data:
                st.error("❌ No matching account found.")
            else:
                st.session_state.verified = True
                st.session_state.user_data = user_data[0]

        if st.session_state.verified and st.session_state.user_data:
            user = st.session_state.user_data

            name = st.text_input("New Name", value=user["name"])
            email = st.text_input("New Email", value=user["email"])
            new_pin = st.text_input("New Pin", value=str(user["pin"]))
            cnic = st.text_input("New CNIC Number", value=str(user["CNIC_no"]))

            if st.button("Update"):
                updated_data = {
                    "name": name if name.strip() else user["name"],
                    "email": email if email.strip() else user["email"],
                    "pin": int(new_pin) if new_pin.strip() else user["pin"],
                    "CNIC_no": int(cnic) if cnic.strip() else user["CNIC_no"],
                    "account_no": user["account_no"],
                    "balance": user["balance"],
                    "age": user["age"]
                }

                changes_made = False
                for key in updated_data:
                    if user[key] != updated_data[key]:
                        user[key] = updated_data[key]
                        changes_made = True

                if changes_made:
                    for idx, i in enumerate(Bank.data):
                        if i["account_no"] == user["account_no"]:
                            Bank.data[idx] = user  # 🔄 Overwrite in original list
                            break
                    Bank.__update()
                    st.success("✅ Details updated successfully.")
                else:
                    st.info("ℹ️ No changes were made.")

                st.session_state.verified = False
                st.session_state.user_data = None

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
                Bank.__update()
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








