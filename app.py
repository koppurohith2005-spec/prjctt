import streamlit as st
import time

# --- BUSINESS LOGIC ---
class BankApplication:
    bank_name = 'State Bank of India'

    def __init__(self, name, account_number, age, mobile_number, balance):
        self.name = name
        self.account_number = account_number
        self.age = age
        self.mobile_number = mobile_number
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            return "❌ Please enter a valid amount", False
        if amount <= self.balance:
            self.balance -= amount
            return f'✅ Transaction successful! Withdrew ${amount}', True
        return '❌ Insufficient Balance', False

    def deposit(self, amount):
        if amount <= 0:
            return "❌ Please enter a valid amount", False
        self.balance += amount
        return f'✅ Success! ${amount} deposited.', True

# --- PAGE CONFIG ---
st.set_page_config(page_title="SBI Digital", page_icon="🏦", layout="wide")

# --- CUSTOM CSS FOR BEAUTIFICATION ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 40px;
        color: #1e88e5;
    }
    .status-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state.user = None

# --- SIDEBAR (REGISTRATION) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/State_Bank_of_India_logo.svg/640px-State_Bank_of_India_logo.svg.png", width=100)
    st.title("User Portal")
    
    if not st.session_state.user:
        with st.form("reg_form"):
            st.subheader("📝 Open Account")
            name = st.text_input("Full Name")
            acc = st.text_input("Account Number")
            age = st.number_input("Age", 18, 100)
            mob = st.text_input("Mobile")
            bal = st.number_input("Initial Deposit ($)", min_value=0)
            submit = st.form_submit_button("Create My Account")
            
            if submit:
                if name and acc and mob:
                    st.session_state.user = BankApplication(name, acc, age, mob, bal)
                    st.success("Account Ready!")
                    st.rerun()
                else:
                    st.error("Please fill all fields")
    else:
        st.write(f"Logged in as: **{st.session_state.user.name}**")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

# --- MAIN INTERFACE ---
if st.session_state.user:
    user = st.session_state.user
    
    # Header Section
    st.title(f"🏦 {BankApplication.bank_name}")
    st.markdown(f"Welcome back, **{user.name}**! Manage your funds securely.")
    
    # Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Current Balance", f"${user.balance:,.2f}")
    with m2:
        st.metric("Account Type", "Savings")
    with m3:
        st.metric("Status", "Active ✅")

    st.divider()

    # Operations Section
    col_left, col_right = st.columns([2, 1])

    with col_left:
        tab1, tab2 = st.tabs(["💸 Withdraw Funds", "💰 Deposit Funds"])
        
        with tab1:
            st.subheader("Withdrawal")
            w_amt = st.number_input("Amount to Withdraw", min_value=0, key="w_val")
            if st.button("Execute Withdrawal"):
                msg, success = user.withdraw(w_amt)
                if success:
                    with st.spinner("Processing..."):
                        time.sleep(1)
                    st.toast(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
        with tab2:
            st.subheader("Deposit")
            d_amt = st.number_input("Amount to Deposit", min_value=0, key="d_val")
            if st.button("Execute Deposit"):
                msg, success = user.deposit(d_amt)
                if success:
                    with st.spinner("Updating Ledger..."):
                        time.sleep(1)
                    st.toast(msg)
                    st.rerun()

    with col_right:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.subheader("👤 Profile Details")
        st.write(f"**A/C No:** `{user.account_number}`")
        st.write(f"**Mobile:** {user.mobile_number}")
        st.write(f"**Age:** {user.age}")
        st.write(f"**Bank:** {BankApplication.bank_name}")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Landing Page for Unregistered users
    st.title("🏦 SBI Digital Banking")
    st.info("👈 Please use the sidebar to register or login to your account.")
    
    # Add a nice placeholder image/graphic
    st.image("https://img.freepik.com/free-vector/online-banking-concept-illustration_114360-17333.jpg", use_container_width=True)