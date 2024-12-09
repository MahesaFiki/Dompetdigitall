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

# Inisialisasi data
data = load_data()

# Fungsi untuk registrasi atau membuat akun
def create_account(username, pin):
    if username in data:
        return "Akun sudah ada!"
    if len(pin) != 4 or not pin.isdigit():
        return "PIN harus 4 digit angka!"
    data[username] = {"pin": pin, "saldo": 0, "riwayat": []}
    save_data(data)
    return "Akun berhasil dibuat!"

# Fungsi untuk login
def login(username, pin):
    if username not in data:
        return False, "Akun tidak ditemukan!"
    if data[username]["pin"] != pin:
        return False, "PIN salah!"
    return True, "Login berhasil!"

# Fungsi untuk menambah saldo
def tambah_saldo(username, jumlah):
    if jumlah <= 0:
        return "Jumlah harus lebih dari 0!"
    data[username]["saldo"] += jumlah
    save_data(data)
    return f"Saldo berhasil ditambahkan. Saldo saat ini: {data[username]['saldo']}"

# Fungsi untuk transfer
def transfer(username, penerima, jumlah, pin):
    if data[username]["pin"] != pin:
        return "PIN salah! Transfer dibatalkan."
    if penerima not in data:
        return "Penerima tidak ditemukan!"
    if jumlah <= 0 or jumlah > data[username]["saldo"]:
        return "Saldo tidak cukup atau jumlah tidak valid!"
    data[username]["saldo"] -= jumlah
    data[penerima]["saldo"] += jumlah
    data[username]["riwayat"].append(f"Transfer ke {penerima}: {jumlah}")
    data[penerima]["riwayat"].append(f"Diterima dari {username}: {jumlah}")
    save_data(data)
    return "Transfer berhasil!"

# Fungsi untuk cek saldo
def cek_saldo(username):
    return f"Saldo saat ini: {data[username]['saldo']}"

# Fungsi untuk cek riwayat transfer
def cek_riwayat(username):
    return data[username]["riwayat"]

# Aplikasi Streamlit
st.title("Dompet Digital")

# Halaman login dan registrasi
menu = st.sidebar.selectbox("Menu", ["Login", "Registrasi"])

if menu == "Registrasi":
    st.subheader("Registrasi Akun")
    username = st.text_input("Nama Pengguna")
    pin = st.text_input("Buat PIN (4 digit)", type="password")
    if st.button("Buat Akun"):
        if username and pin:
            result = create_account(username, pin)
            st.success(result)
        else:
            st.error("Harap isi semua kolom!")

elif menu == "Login":
    st.subheader("Login")
    username = st.text_input("Nama Pengguna")
    pin = st.text_input("PIN", type="password")
    if st.button("Login"):
        if username and pin:
            success, message = login(username, pin)
            if success:
                st.success(message)
                # Menu utama setelah login
                page = st.selectbox("Menu Utama", ["Tambah Saldo", "Transfer", "Cek Saldo", "Riwayat Transfer"])
                if page == "Tambah Saldo":
                    jumlah = st.number_input("Jumlah Saldo", min_value=0, step=1)
                    if st.button("Tambah"):
                        result = tambah_saldo(username, jumlah)
                        st.success(result)
                elif page == "Transfer":
                    penerima = st.text_input("Nama Penerima")
                    jumlah = st.number_input("Jumlah Transfer", min_value=0, step=1)
                    pin_konfirmasi = st.text_input("Konfirmasi PIN", type="password")
                    if st.button("Kirim"):
                        result = transfer(username, penerima, jumlah, pin_konfirmasi)
                        if "berhasil" in result:
                            st.success(result)
                        else:
                            st.error(result)
                elif page == "Cek Saldo":
                    st.info(cek_saldo(username))
                elif page == "Riwayat Transfer":
                    riwayat = cek_riwayat(username)
                    st.write("Riwayat Transaksi:")
                    for item in riwayat:
                        st.write(f"- {item}")
            else:
                st.error(message)
        else:
            st.error("Harap isi semua kolom!")
