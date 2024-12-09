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

# Fungsi untuk format Rupiah
def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

# Fungsi untuk registrasi akun
def register():
    st.subheader("📝 Registrasi Akun")
    username = st.text_input("Nama Pengguna")
    pin = st.text_input("Buat PIN (6 digit)", type="password")
    if st.button("Buat Akun"):
        if username in data:
            st.error("Akun sudah ada!")
        elif len(pin) != 6 or not pin.isdigit():
            st.error("PIN harus 6 digit angka!")
        else:
            data[username] = {"pin": pin, "saldo": 0, "riwayat": []}
            save_data(data)
            st.success("Akun berhasil dibuat!")

# Fungsi untuk login
def login():
    st.subheader("🔑 Login")
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

# Fungsi untuk menambah saldo
def tambah_saldo():
    st.subheader("💰 Tambah Saldo")
    jumlah = st.number_input("Jumlah Saldo", min_value=0, step=1)
    if st.button("Tambah"):
        data[st.session_state["username"]]["saldo"] += jumlah
        save_data(data)
        saldo_terbaru = data[st.session_state["username"]]["saldo"]
        st.success(f"Saldo berhasil ditambahkan. Saldo saat ini: {format_rupiah(saldo_terbaru)}")

# Fungsi untuk tarik saldo
def tarik_saldo():
    st.subheader("🏧 Tarik Saldo")
    jumlah = st.number_input("Jumlah Tarik", min_value=0, step=1)
    pin = st.text_input("Konfirmasi PIN", type="password")
    if st.button("Tarik"):
        if jumlah <= 0:
            st.error("Jumlah tarik harus lebih besar dari 0!")
        elif jumlah > data[st.session_state["username"]]["saldo"]:
            st.error("Saldo tidak cukup!")
        elif data[st.session_state["username"]]["pin"] != pin:
            st.error("PIN salah!")
        else:
            data[st.session_state["username"]]["saldo"] -= jumlah
            data[st.session_state["username"]]["riwayat"].append(f"Tarik saldo: {format_rupiah(jumlah)}")
            save_data(data)
            saldo_terbaru = data[st.session_state["username"]]["saldo"]
            st.success(f"Penarikan berhasil. Sisa saldo Anda: {format_rupiah(saldo_terbaru)}")

# Fungsi untuk transfer
def transfer():
    st.subheader("📤 Transfer")
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
            data[st.session_state["username"]]["riwayat"].append(f"Transfer ke {penerima}: {format_rupiah(jumlah)}")
            data[penerima]["riwayat"].append(f"Diterima dari {st.session_state['username']}: {format_rupiah(jumlah)}")
            save_data(data)
            st.success(f"Transfer berhasil! Anda mengirim {format_rupiah(jumlah)} ke {penerima}.")

# Fungsi untuk cek saldo
def cek_saldo():
    st.subheader("📊 Cek Saldo")
    saldo = data[st.session_state["username"]]["saldo"]
    st.info(f"Saldo Anda saat ini: {format_rupiah(saldo)}")

# Fungsi untuk cek riwayat transfer
def cek_riwayat():
    st.subheader("🧾 Riwayat Transfer")
    riwayat = data[st.session_state["username"]]["riwayat"]
    if riwayat:
        for item in riwayat:
            st.write(f"- {item}")
    else:
        st.info("Belum ada riwayat transaksi.")

# Fungsi untuk logout
def logout():
    st.subheader("🚪 Logout")
    st.write("Apakah Anda yakin ingin logout?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Iya"):
            st.session_state.clear()
            st.success("Anda telah logout.")
    with col2:
        if st.button("Tidak"):
            st.info("Logout dibatalkan.")

# Inisialisasi data
data = load_data()

# Streamlit: Header
st.markdown("""
    <div style="background-color: #3498db; padding: 15px; border-radius: 10px;">
        <h1 style="color: white; text-align: center;">🌐 Dompet Digital EasySave</h1>
    </div>
""", unsafe_allow_html=True)

# Cek apakah pengguna sudah login
if "username" in st.session_state:
    st.sidebar.subheader(f"Selamat datang, {st.session_state['username']}!")
    menu = st.sidebar.radio("Menu", ["Tambah Saldo", "Tarik Saldo", "Transfer", "Cek Saldo", "Riwayat Transfer", "Logout"])
    
    if menu == "Tambah Saldo":
        tambah_saldo()
    elif menu == "Tarik Saldo":
        tarik_saldo()
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
