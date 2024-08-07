import pandas as pd
import mysql.connector
from mysql.connector import Error

# File path for Excel
excel_path = r'data_cleaning_output.xlsx'

# Baca data dari sheet Produk
produk_df = pd.read_excel(excel_path, sheet_name='Produk')

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

# Fungsi untuk memasukkan data ke dalam tabel Produk
def insert_produk_data(connection, df):
    cursor = connection.cursor()
    for _, row in df.iterrows():
        # SQL query untuk memasukkan data ke tabel Produk
        sql = """
        INSERT INTO Produk (id_product, product_name, brand_name, manufacture, country_made,
                            id_category, id_program, id_data, id_test, year_tested, qualifier, lead_concentration)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Buat tuple dari row DataFrame
        values = (
            row['id_product'], row['product_name'], row['brand_name'], row['manufacture'], row['country_made'],
            row['id_category'], row['id_program'], row['id_data'], row['id_test'],
            int(row['year_tested']), row['qualifier'], float(row['lead_concentration'])
        )
        try:
            cursor.execute(sql, values)
            connection.commit()
            print(f"Data {row['product_name']} berhasil dimasukkan ke tabel Produk")
        except Error as e:
            print(f"Kesalahan: '{e}' terjadi saat memasukkan data {row['product_name']}")

# Koneksi ke database final_project
connection = create_connection("localhost", "root", "", "final_project")

# Masukkan data ke tabel Produk
insert_produk_data(connection, produk_df)

# Tutup koneksi
if connection.is_connected():
    connection.close()
    print("Koneksi ke MySQL ditutup")
