import streamlit as st
import json
import os

DATA_FILE = "dompet_digital.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

# Fungsi-fungsi lainnya tetap sama, tambahkan key pada elemen
def login():
    st.subheader("🔑 Login")
    username = st.text_input("Nama Pengguna", key="login_username")
    pin = st.text_input("PIN", type="password", key="login_pin")
    if st.button("Login", key="login_button"):
        if username not in data:
            st.error("Akun tidak ditemukan!")
        elif data[username]["pin"] != pin:
            st.error("PIN salah!")
        else:
            st.session_state["username"] = username
            st.experimental_rerun()

# Streamlit Layout
data = load_data()
if "username" not in st.session_state:
    st.session_state["username"] = None

if st.session_state["username"]:
    st.sidebar.success(f"Selamat datang, {st.session_state['username']}!")
    menu = st.sidebar.radio("Menu", ["Tambah Saldo", "Transfer", "Cek Saldo", "Riwayat Transfer", "Logout"], key="menu_select")

    if menu == "Logout":
        st.session_state.clear()
        st.experimental_rerun()
else:
    menu = st.sidebar.radio("Menu", ["Login", "Registrasi"], key="auth_menu")
    if menu == "Login":
        login()
    elif menu == "Registrasi":
        register()
