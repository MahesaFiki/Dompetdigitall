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
def create_account():
    username = input("Masukkan nama pengguna: ")
    if username in data:
        print("Akun sudah ada!")
        return
    pin = input("Buat PIN (4 digit): ")
    if len(pin) != 4 or not pin.isdigit():
        print("PIN harus 4 digit angka!")
        return
    data[username] = {"pin": pin, "saldo": 0, "riwayat": []}
    save_data(data)
    print("Akun berhasil dibuat!")

# Fungsi untuk login
def login():
    username = input("Masukkan nama pengguna: ")
    if username not in data:
        print("Akun tidak ditemukan!")
        return None
    pin = input("Masukkan PIN: ")
    if data[username]["pin"] != pin:
        print("PIN salah!")
        return None
    print("Login berhasil!")
    return username

# Fungsi untuk menambah saldo
def tambah_saldo(username):
    jumlah = int(input("Masukkan jumlah saldo yang ingin ditambahkan: "))
    if jumlah <= 0:
        print("Jumlah harus lebih dari 0!")
        return
    data[username]["saldo"] += jumlah
    save_data(data)
    print(f"Saldo berhasil ditambahkan. Saldo saat ini: {data[username]['saldo']}")

# Fungsi untuk transfer dengan verifikasi PIN
def transfer(username):
    penerima = input("Masukkan nama pengguna penerima: ")
    if penerima not in data:
        print("Penerima tidak ditemukan!")
        return
    jumlah = int(input("Masukkan jumlah transfer: "))
    if jumlah <= 0 or jumlah > data[username]["saldo"]:
        print("Saldo tidak cukup atau jumlah tidak valid!")
        return
    pin = input("Masukkan PIN untuk konfirmasi transfer: ")
    if data[username]["pin"] != pin:
        print("PIN salah! Transfer dibatalkan.")
        return
    data[username]["saldo"] -= jumlah
    data[penerima]["saldo"] += jumlah
    data[username]["riwayat"].append(f"Transfer ke {penerima}: {jumlah}")
    data[penerima]["riwayat"].append(f"Diterima dari {username}: {jumlah}")
    save_data(data)
    print("Transfer berhasil!")

# Fungsi untuk cek saldo
def cek_saldo(username):
    print(f"Saldo saat ini: {data[username]['saldo']}")

# Fungsi untuk cek riwayat transfer
def cek_riwayat(username):
    print("Riwayat transaksi:")
    for riwayat in data[username]["riwayat"]:
        print(f"- {riwayat}")

# Menu utama
def main():
    while True:
        print("\n=== Dompet Digital ===")
        print("1. Buat Akun")
        print("2. Login")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            create_account()
        elif pilihan == "2":
            user = login()
            if user:
                while True:
                    print("\n=== Menu Utama ===")
                    print("1. Tambah Saldo")
                    print("2. Transfer")
                    print("3. Cek Saldo")
                    print("4. Cek Riwayat Transfer")
                    print("5. Logout")
                    sub_pilihan = input("Pilih menu: ")
                    
                    if sub_pilihan == "1":
                        tambah_saldo(user)
                    elif sub_pilihan == "2":
                        transfer(user)
                    elif sub_pilihan == "3":
                        cek_saldo(user)
                    elif sub_pilihan == "4":
                        cek_riwayat(user)
                    elif sub_pilihan == "5":
                        print("Logout berhasil!")
                        break
                    else:
                        print("Pilihan tidak valid!")
        elif pilihan == "3":
            print("Keluar dari aplikasi. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()


