from sqlalchemy import create_engine
import pandas as pd

# 连接SQLite数据库
engine = create_engine('sqlite:///data.db')

# 查询数据库中的所有记录
query = "SELECT * FROM schools"
df = pd.read_sql(query, con=engine)

print(df)