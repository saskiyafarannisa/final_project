import pandas as pd

# File paths
csv_path = r'D:\data_final\2\Data_clean_final_project.csv'
excel_path = r'data_cleaning_output.xlsx'

# Baca data dari CSV dan Excel
csv_data = pd.read_csv(csv_path)
excel_data = pd.ExcelFile(excel_path)

# Baca sheet yang diperlukan dari Excel
kategori_df = pd.read_excel(excel_data, sheet_name='Kategori')
program_df = pd.read_excel(excel_data, sheet_name='Program')
data_resource_df = pd.read_excel(excel_data, sheet_name='Data_Resource')
test_df = pd.read_excel(excel_data, sheet_name='Test')

# Hapus duplikasi dari data CSV (jika ada)
csv_data.drop_duplicates(inplace=True)

# Tambahkan ID untuk Produk berdasarkan CSV data
csv_data['id_product'] = ['PRD{:03d}'.format(i) for i in range(1, len(csv_data) + 1)]

# Gabungkan ID FK dengan data produk berdasarkan kesamaan atribut
produk_df = csv_data.merge(kategori_df, left_on='Product Type', right_on='product_type', how='left') \
    .merge(program_df, left_on='Program', right_on='program_name', how='left') \
    .merge(data_resource_df, left_on='Data source', right_on='data_source', how='left') \
    .merge(test_df, left_on='Test method', right_on='test_method', how='left')

# Pilih dan atur kolom untuk tabel Produk
produk_df = produk_df[['id_product', 'Product Name', 'Brand Name', 'Manufacturer', 'Made in Country',
                       'id_category', 'id_program', 'id_data', 'id_test',
                       'Year tested', 'Qualifier', 'Lead Concentration (ppm)']]

# Ganti nama kolom sesuai dengan ERD
produk_df.columns = ['id_product', 'product_name', 'brand_name', 'manufacture', 'country_made',
                     'id_category', 'id_program', 'id_data', 'id_test',
                     'year_tested', 'qualifier', 'lead_concentration']

# Simpan ke file Excel dengan menambahkan sheet baru
with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    produk_df.to_excel(writer, sheet_name='Produk', index=False)

print("Tabel Produk berhasil ditambahkan ke file Excel: 'data_cleaning_output.xlsx'")
