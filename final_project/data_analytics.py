import mysql.connector
import pandas as pd
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fungsi untuk membuat koneksi ke database MySQL
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Koneksi ke MySQL berhasil")
    except Error as e:
        print(f"Kesalahan: '{e}' terjadi")
    return connection

# Koneksi ke database final_project
connection = create_connection("localhost", "root", "", "final_project")

# Ambil data dari database
query = """
SELECT Kategori.product_type, AVG(Produk.lead_concentration) AS avg_lead_concentration
FROM Produk
JOIN Kategori ON Produk.id_category = Kategori.id_category
GROUP BY Kategori.product_type
"""
df = pd.read_sql(query, connection)

# Tutup koneksi
if connection.is_connected():
    connection.close()
    print("Koneksi ke MySQL ditutup")

# Fungsi untuk membuat tampilan tkinter
def create_gui():
    # Buat jendela utama
    root = tk.Tk()
    root.title("Analisis Konsentrasi Timbal Berdasarkan Kategori Produk")

    # Tambahkan tabel
    tree = ttk.Treeview(root, columns=("Kategori Produk", "Rata-rata Timbal (ppm)"), show="headings")
    tree.heading("Kategori Produk", text="Kategori Produk")
    tree.heading("Rata-rata Timbal (ppm)", text="Rata-rata Timbal (ppm)")
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Masukkan data ke dalam tabel
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=(row["product_type"], row["avg_lead_concentration"]))

    # Tambahkan grafik batang
    figure, ax = plt.subplots(figsize=(8, 6))
    ax.bar(df["product_type"], df["avg_lead_concentration"], color='skyblue')
    ax.set_xlabel('Kategori Produk')
    ax.set_ylabel('Rata-rata Timbal (ppm)')
    ax.set_title('Rata-rata Konsentrasi Timbal per Kategori Produk')
    ax.set_xticklabels(df["product_type"], rotation=45, ha="right")

    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()

    # Jalankan loop tkinter
    root.mainloop()

# Panggil fungsi untuk membuat tampilan
create_gui()
