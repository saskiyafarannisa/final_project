import pandas as pd

# file data csv
file_path = r'D:\data_final\2\Lead_Content_of_Consumer_Products_tested_in_King_County__Washington.csv'

df = pd.read_csv(file_path)

# Fungsi menghapus kategori produk yang tidak sama
def clean_product_type(product_type):
    if pd.notna(product_type):
        return product_type.split(' -')[0]
    return product_type

#memanggil fungsi untuk mengubah data yang berbeda menjadi sama
df['Product Type'] = df['Product Type'].apply(clean_product_type)

# Menghapus Baris Kosong pada Kolom 'Lead Concentration (ppm)
df = df.dropna(subset=['Lead Concentration (ppm)'])

# Menghapus Baris Kosong Secara Umum
df = df.dropna(how='all')

# Mengisi Baris Qualifier yang kosong dengan -
df = df.fillna('-')

# Menyimpan data yang clean ke csv baru
cleaned_file_path = r"D:\data_final\2\Data_clean_final_project.csv"
df.to_csv(cleaned_file_path, index=False)

print(f"Data cleaned and saved to {cleaned_file_path}")
