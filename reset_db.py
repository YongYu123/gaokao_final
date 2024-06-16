import os

# 定义数据库文件路径
db_path = 'data.db'

# 删除数据库文件
if os.path.exists(db_path):
    os.remove(db_path)
    print("Database file removed successfully!")
else:
    print("Database file does not exist!")

# 创建数据库表
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# 连接SQLite数据库
engine = create_engine(f'sqlite:///{db_path}')

# 创建MetaData实例
metadata = MetaData()

# 定义表结构
schools = Table('schools', metadata,
                Column('id', Integer, primary_key=True),
                Column('专业', String),
                Column('学校', String),
                Column('计划数', Integer),
                Column('位次', Integer),
                Column('年份', String))

# 创建表
metadata.create_all(engine)

print("Database and table created successfully!")
