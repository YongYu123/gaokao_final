import os
import pandas as pd
from sqlalchemy import create_engine
import re

# 定义Excel文件所在文件夹
folder_path = 'data_files'

# 连接SQLite数据库
engine = create_engine('sqlite:///data.db')

# 读取文件夹中的所有Excel文件并导入数据
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(folder_path, filename)
        try:
            # 假设文件名包含年份，例如 "data_2023.xlsx"
            match = re.search(r'\d{4}', filename)
            if match:
                year = match.group(0)
            else:
                year = 'Unknown'  # 或者可以设定一个默认年份

            # 指定 engine='openpyxl' 来读取 .xlsx 文件
            df = pd.read_excel(file_path, engine='openpyxl')
            df['年份'] = year  # 添加年份列

            # 将数据写入到指定表中
            df.to_sql('schools', con=engine, if_exists='append', index=False)
            print(f"Data from {filename} imported successfully!")
        
        except Exception as e:
            print(f"Error reading {filename}: {e}")

print("All data imported successfully!")
