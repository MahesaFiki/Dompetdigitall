import streamlit as st
import json
import os

# File untuk menyimpan data
DATA_FILE = "dompet_digital.json"

# Fungsi untuk memuat data dari file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Fungsi untuk menyimpan data ke file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Fungsi untuk registrasi akun
def register():
    st.subheader("Registrasi Akun")
    username = st.text_input("Nama Pengguna")
    pin = st.text_input("Buat PIN (4 digit)", type="password")
    if st.button("Buat Akun"):
        if username in data:
            st.error("Akun sudah ada!")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN harus 4 digit angka!")
        else:
            data[username] = {"pin": pin, "saldo": 0, "riwayat": []}
            save_data(data)
            st.success("Akun berhasil dibuat!")

# Fungsi untuk login
def login():
    st.subheader("Login")
    username = st.text_input("Nama Pengguna")
    pin = st.text_input("PIN", type="password")
    if st.button("Login"):
        if username not in data:
            st.error("Akun tidak ditemukan!")
        elif data[username]["pin"] != pin:
            st.error("PIN salah!")
        else:
            st.session_state["username"] = username
            st.success(f"Selamat datang, {username}!")

# Fungsi untuk tambah saldo
def tambah_saldo():
    st.subheader("Tambah Saldo")
    jumlah = st.number_input("Jumlah Saldo", min_value=0, step=1)
    if st.button("Tambah"):
        data[st.session_state["username"]]["saldo"] += jumlah
        save_data(data)
        st.success(f"Saldo berhasil ditambahkan. Saldo saat ini: {data[st.session_state['username']]['saldo']}")

# Fungsi untuk transfer
def transfer():
    st.subheader("Transfer")
    penerima = st.text_input("Nama Penerima")
    jumlah = st.number_input("Jumlah Transfer", min_value=0, step=1)
    pin = st.text_input("Konfirmasi PIN", type="password")
    if st.button("Kirim"):
        if penerima not in data:
            st.error("Penerima tidak ditemukan!")
        elif jumlah <= 0 or jumlah > data[st.session_state["username"]]["saldo"]:
            st.error("Saldo tidak cukup atau jumlah tidak valid!")
        elif data[st.session_state["username"]]["pin"] != pin:
            st.error("PIN salah!")
        else:
            data[st.session_state["username"]]["saldo"] -= jumlah
            data[penerima]["saldo"] += jumlah
            data[st.session_state["username"]]["riwayat"].append(f"Transfer ke {penerima}: {jumlah}")
            data[penerima]["riwayat"].append(f"Diterima dari {st.session_state['username']}: {jumlah}")
            save_data(data)
            st.success("Transfer berhasil!")

# Fungsi untuk cek saldo
def cek_saldo():
    st.subheader("Cek Saldo")
    saldo = data[st.session_state["username"]]["saldo"]
    st.info(f"Saldo Anda saat ini: {saldo}")

# Fungsi untuk cek riwayat transfer
def cek_riwayat():
    st.subheader("Riwayat Transfer")
    riwayat = data[st.session_state["username"]]["riwayat"]
    if riwayat:
        for item in riwayat:
            st.write(f"- {item}")
    else:
        st.info("Belum ada riwayat transaksi.")

# Fungsi untuk logout
def logout():
    st.session_state.clear()
    st.success("Anda telah logout.")

# Inisialisasi data
data = load_data()

# Streamlit: Logika Menu
st.title("Dompet Digital")

# Cek apakah pengguna sudah login
if "username" in st.session_state:
    st.sidebar.subheader(f"Selamat datang, {st.session_state['username']}!")
    menu = st.sidebar.radio("Menu", ["Tambah Saldo", "Transfer", "Cek Saldo", "Riwayat Transfer", "Logout"])
    
    if menu == "Tambah Saldo":
        tambah_saldo()
    elif menu == "Transfer":
        transfer()
    elif menu == "Cek Saldo":
        cek_saldo()
    elif menu == "Riwayat Transfer":
        cek_riwayat()
    elif menu == "Logout":
        logout()
else:
    menu = st.sidebar.radio("Menu", ["Login", "Registrasi"])
    
    if menu == "Login":
        login()
    elif menu == "Registrasi":
        register()
