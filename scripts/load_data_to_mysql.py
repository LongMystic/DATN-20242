import pymysql
import pandas as pd
import os

# Database connection details
DB_HOST = "localhost"  # Change if MySQL is running in a container
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "test"
TABLE_NAME = "category"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(SCRIPT_DIR, "../data/category_sample.csv")
# Connect to MySQL
connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
cursor = connection.cursor()

row_id = 0
# Read CSV file
df = pd.read_csv(CSV_FILE_PATH, encoding="utf-8", sep=",")

# Replace NaN with None for MySQL
df = df.where(pd.notna(df), None)

# Create database if not exits

create_database_query = f"""
    CREATE DATABASE IF NOT EXISTS test;
"""
cursor.execute(create_database_query)
connection.commit()
print("Database created successfully!")


drop_table_query = f"""
    DROP TABLE IF EXISTS test.{TABLE_NAME};
"""
cursor.execute(drop_table_query)
connection.commit()
print("Table deleted successfully!")

# Create table if it doesn't exist (modify columns as needed)
create_table_query = f"""
CREATE TABLE IF NOT EXISTS test.{TABLE_NAME} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    category_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    level INT,
    parent_category VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    parent_id INT,
    industry_id INT,
    is_selected INT
);
"""
cursor.execute(create_table_query)
connection.commit()
print("Table created successfully!")

# Insert data
for _, row in df.iterrows():
    insert_query = f"""INSERT INTO test.{TABLE_NAME} (
        category_id,
        category_name,
        level,
        parent_category,
        parent_id,
        industry_id,
        is_selected
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    print(row)
    cursor.execute(insert_query, (int(row.iloc[0]),
                                str(row.iloc[1]) if pd.notna(row.iloc[1]) else "",
                                int(row.iloc[2]) if pd.notna(row.iloc[2]) else -1,
                                str(row.iloc[3]) if pd.notna(row.iloc[3]) else "",
                                int(row.iloc[4]) if pd.notna(row.iloc[4]) else -1,
                                int(row.iloc[5]) if pd.notna(row.iloc[5]) else -1,
                                int(row.iloc[6]) if pd.notna(row.iloc[6]) else -1))

connection.commit()
cursor.close()
connection.close()

print("Data successfully loaded into MySQL.")
