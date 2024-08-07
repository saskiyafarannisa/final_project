import pandas as pd

# Baca data dari CSV yang telah dibersihkan
file_path = r'D:\data_final\2\Data_clean_final_project.csv'
df = pd.read_csv(file_path)

# Hapus duplikasi
kategori_df = df[['Product Type']].drop_duplicates().reset_index(drop=True)
program_df = df[['Program']].drop_duplicates().reset_index(drop=True)
data_resource_df = df[['Data source']].drop_duplicates().reset_index(drop=True)
test_df = df[['Test method']].drop_duplicates().reset_index(drop=True)

# Buat ID unik untuk setiap atribut
kategori_df['id_category'] = ['K{:02d}'.format(i) for i in range(1, len(kategori_df) + 1)]
program_df['id_program'] = ['P{:02d}'.format(i) for i in range(1, len(program_df) + 1)]
data_resource_df['id_data'] = ['D{:02d}'.format(i) for i in range(1, len(data_resource_df) + 1)]
test_df['id_test'] = ['T{:02d}'.format(i) for i in range(1, len(test_df) + 1)]

# Atur urutan kolom (ID ditempatkan di awal)
kategori_df = kategori_df[['id_category', 'Product Type']]
program_df = program_df[['id_program', 'Program']]
data_resource_df = data_resource_df[['id_data', 'Data source']]
test_df = test_df[['id_test', 'Test method']]

# Ganti nama kolom sesuai dengan ERD
kategori_df.columns = ['id_category', 'product_type']
program_df.columns = ['id_program', 'program_name']
data_resource_df.columns = ['id_data', 'data_source']
test_df.columns = ['id_test', 'test_method']

# Simpan ke file Excel
with pd.ExcelWriter('data_cleaning_output.xlsx', engine='openpyxl') as writer:
    kategori_df.to_excel(writer, sheet_name='Kategori', index=False)
    program_df.to_excel(writer, sheet_name='Program', index=False)
    data_resource_df.to_excel(writer, sheet_name='Data_Resource', index=False)
    test_df.to_excel(writer, sheet_name='Test', index=False)

print("Excel file created successfully: 'data_cleaning_output.xlsx'")
