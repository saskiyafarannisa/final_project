import pandas as pd
import mysql.connector
from mysql.connector import Error

# File path for Excel
excel_path = r'data_cleaning_output.xlsx'

# Baca data dari Excel
kategori_df = pd.read_excel(excel_path, sheet_name='Kategori')
program_df = pd.read_excel(excel_path, sheet_name='Program')
data_resource_df = pd.read_excel(excel_path, sheet_name='Data_Resource')
test_df = pd.read_excel(excel_path, sheet_name='Test')
produk_df = pd.read_excel(excel_path, sheet_name='Produk')

# Fungsi untuk membuat koneksi ke database MySQL
def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Koneksi ke MySQL berhasil")
    except Error as e:
        print(f"Kesalahan: '{e}' terjadi")
    return connection

# Fungsi untuk mengeksekusi kueri SQL
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Kueri berhasil dieksekusi")
    except Error as e:
        print(f"Kesalahan: '{e}' terjadi")

# Koneksi ke server MySQL
connection = create_connection("localhost", "root", "")

# Buat database baru
create_database_query = "CREATE DATABASE IF NOT EXISTS final_project"
execute_query(connection, create_database_query)

# Koneksi ke database baru
connection = create_connection("localhost", "root", "")
connection.database = "final_project"

# Membuat tabel sesuai dengan ERD
create_kategori_table = """
CREATE TABLE IF NOT EXISTS Kategori (
    id_category VARCHAR(3) PRIMARY KEY,
    product_type VARCHAR(255) NOT NULL
);
"""

create_program_table = """
CREATE TABLE IF NOT EXISTS Program (
    id_program VARCHAR(3) PRIMARY KEY,
    program_name VARCHAR(255) NOT NULL
);
"""

create_data_resource_table = """
CREATE TABLE IF NOT EXISTS DataResource (
    id_data VARCHAR(3) PRIMARY KEY,
    data_source VARCHAR(255) NOT NULL
);
"""

create_test_table = """
CREATE TABLE IF NOT EXISTS Test (
    id_test VARCHAR(3) PRIMARY KEY,
    test_method VARCHAR(255) NOT NULL
);
"""

create_produk_table = """
CREATE TABLE IF NOT EXISTS Produk (
    id_product VARCHAR(6) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    brand_name VARCHAR(255),
    manufacture VARCHAR(255),
    country_made VARCHAR(255),
    id_category VARCHAR(3),
    id_program VARCHAR(3),
    id_data VARCHAR(3),
    id_test VARCHAR(3),
    year_tested INT,
    qualifier VARCHAR(10),
    lead_concentration FLOAT,
    FOREIGN KEY (id_category) REFERENCES Kategori(id_category),
    FOREIGN KEY (id_program) REFERENCES Program(id_program),
    FOREIGN KEY (id_data) REFERENCES DataResource(id_data),
    FOREIGN KEY (id_test) REFERENCES Test(id_test)
);
"""

# Eksekusi kueri pembuatan tabel
execute_query(connection, create_kategori_table)
execute_query(connection, create_program_table)
execute_query(connection, create_data_resource_table)
execute_query(connection, create_test_table)
execute_query(connection, create_produk_table)

# Fungsi untuk memasukkan data ke dalam tabel
def insert_data(connection, df, table_name):
    cursor = connection.cursor()
    for _, row in df.iterrows():
        sql = f"INSERT INTO {table_name} VALUES ({'%s, ' * (len(row) - 1)}%s)"
        try:
            cursor.execute(sql, tuple(row))
            connection.commit()
            print(f"Data berhasil dimasukkan ke tabel {table_name}")
        except Error as e:
            print(f"Kesalahan: '{e}' terjadi saat memasukkan data ke tabel {table_name}")

# Masukkan data ke tabel
insert_data(connection, kategori_df, 'Kategori')
insert_data(connection, program_df, 'Program')
insert_data(connection, data_resource_df, 'DataResource')
insert_data(connection, test_df, 'Test')

# Tutup koneksi
if connection.is_connected():
    connection.close()
    print("Koneksi ke MySQL ditutup")
