import streamlit as st
from datetime import datetime

# Initialize state
if 'balance' not in st.session_state:
    st.session_state.balance = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'pin' not in st.session_state:
    st.session_state.pin = "1234" # Default PIN for demo
if 'card_last_four' not in st.session_state:
    st.session_state.card_last_four = "XXXX"

def main():
    st.title("Welcome to PyBank ATM")

    if not st.session_state.logged_in:
        st.subheader("Login")
        card = st.text_input("What is your Bank, 8 digit, ID (e.g., 1234-5678):")
        pin_input = st.text_input("Please enter your PIN:", type="password")
        if st.button("Login"):
            if pin_input == st.session_state.pin:
                st.session_state.logged_in = True
                st.session_state.card_last_four = card[-4:] if card else "XXXX"
                st.rerun()
            else:
                st.error("Incorrect PIN")
    else:
        st.write(f"Hello PyBank customer ending in {st.session_state.card_last_four}. You are logged in")

        choice = st.selectbox(
            "Operations:",
            ['Select...', 'Deposit', 'Withdrawal', 'Check Balance',
             'Pie Chart: Deposits vs Withdrawal', 'Bar Graph of Transactions', 'Change PIN']
        )

        if choice == 'Deposit':
            st.subheader("Deposit")
            amount = st.number_input("Deposit Amount: $", min_value=0.0)
            if st.button("Deposit"):
                if amount > 0:
                    st.session_state.balance += amount
                    st.session_state.history.append({'type': 'deposit', 'amount': amount, 'date': datetime.now()})
                    st.success(f"Deposit Complete! New Balance: ${st.session_state.balance:.2f}")
                else:
                    st.error("Error: Deposit must be more than $0!")

        elif choice == 'Withdrawal':
            st.subheader("Withdrawal")
            amount = st.number_input("Withdraw Amount: $", min_value=0.0)
            if st.button("Withdraw"):
                if 0 < amount <= st.session_state.balance:
                    st.session_state.balance -= amount
                    st.session_state.history.append({'type': 'withdrawal', 'amount': -amount, 'date': datetime.now()})
                    st.success(f"Withdrawal Complete! New Balance: ${st.session_state.balance:.2f}")
                else:
                    st.error("Insufficient funds or invalid amount!")

        elif choice == 'Check Balance':
            st.subheader("Check Balance")
            st.info(f"Your Current Balance: ${st.session_state.balance:.2f}")

        elif choice == 'Pie Chart: Deposits vs Withdrawal':
            st.subheader("Pie Chart: Deposits vs Withdrawal")
            total_dep = sum(h['amount'] for h in st.session_state.history if h['type'] == 'deposit')
            total_wit = abs(sum(h['amount'] for h in st.session_state.history if h['type'] == 'withdrawal'))
            total = total_dep + total_wit
            if total > 0:
                deposit_pct = (total_dep / total) * 100
                withdraw_pct = (total_wit / total) * 100
                st.write(f"Deposits: {total_dep:.2f} ({deposit_pct:.1f}%) -- Withdrawals: {total_wit:.2f} ({withdraw_pct:.1f}%) ")
                st.write(f"Total Money Moved: ${total:.2f}")
            else:
                st.write("No transaction history yet!")

        elif choice == 'Bar Graph of Transactions':
            st.subheader("Bar Graph of Transactions")
            if not st.session_state.history:
                st.write("No transactions yet!")
            else:
                st.write("Transaction History (Text Bar Graph)")
                st.write("Time         | Amount     | Type")
                st.write("-" * 40)
                for h in st.session_state.history:
                    time_str = h['date'].strftime("%H:%M:%S")
                    amount_str = f"${h['amount']:+.2f}"  # + for deposit, - for withdraw
                    type_str = "Deposit  " if h['type'] == 'deposit' else "Withdraw "
                    # Make a simple bar with #
                    bar_length = int(abs(h['amount']) // 5)  # 1 # per $5
                    bar = "#" * bar_length
                    st.write(f"{time_str} | {amount_str:>8} | {type_str} {bar}")
                st.write(f"\nCurrent Balance: ${st.session_state.balance:.2f}")

        elif choice == 'Change PIN':
            st.subheader("Change PIN")
            old_pin = st.text_input("Old PIN:", type="password")
            new_pin = st.text_input("New PIN:", type="password")
            if st.button("Update PIN"):
                if old_pin == st.session_state.pin:
                    if new_pin:
                        st.session_state.pin = new_pin
                        st.success("PIN Changed Successfully!")
                    else:
                        st.error("Error: New PIN cannot be empty!")
                else:
                    st.error("Error: Wrong old PIN!")

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
