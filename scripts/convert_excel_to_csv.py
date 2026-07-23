"""
Convert all Excel files in data/raw/ to CSV
"""
import pandas as pd
import os

RAW_DIR = 'data/raw'

for file in os.listdir(RAW_DIR):
    if file.endswith('.xlsx'):
        excel_path = os.path.join(RAW_DIR, file)
        csv_path = os.path.join(RAW_DIR, file.replace('.xlsx', '.csv'))
        
        df = pd.read_excel(excel_path)
        df.to_csv(csv_path, index=False)
        print(f'✅ Converted: {file} → {csv_path}') 