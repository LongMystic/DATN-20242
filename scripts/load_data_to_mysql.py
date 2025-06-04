import pymysql
import pandas as pd
import os
import time

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "test"
TABLE_NAME = "category"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(SCRIPT_DIR, "..", "data/")


def create_database(cursor, connection):
    # Create database if not exits

    create_database_query = f"""
        CREATE DATABASE IF NOT EXISTS test;
    """
    cursor.execute(create_database_query)
    connection.commit()
    print("Database created successfully!")


def load_holidays_events(cursor, connection, csv_file_path, table_name):
    row_id = 0
    # Read CSV file
    df = pd.read_csv(csv_file_path, encoding="utf-8", sep=",")

    # Replace NaN with None for MySQL
    df = df.where(pd.notna(df), None)

    drop_table_query = f"""
        DROP TABLE IF EXISTS test.{table_name};
    """
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully!")

    # Create table if it doesn't exist (modify columns as needed)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS test.{table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        type VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        locale VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        locale_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        description VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        transferred BOOLEAN
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully!")

    # Insert data
    for _, row in df.iterrows():
        insert_query = f"""INSERT INTO test.{table_name} (
            date,
            type,
            locale,
            locale_name,
            description,
            transferred
        ) VALUES (%s, %s, %s, %s, %s, %s)"""
        # print(row)
        cursor.execute(insert_query, (
                                    row.iloc[0],
                                    row.iloc[1],
                                    row.iloc[2],
                                    row.iloc[3],
                                    row.iloc[4],
                                    row.iloc[5]))

    connection.commit()


    print(f"Table {table_name} successfully loaded into MySQL.")


def load_items(cursor, connection, csv_file_path, table_name):
    row_id = 0
    # Read CSV file
    df = pd.read_csv(csv_file_path, encoding="utf-8", sep=",")

    # Replace NaN with None for MySQL
    df = df.where(pd.notna(df), None)

    drop_table_query = f"""
        DROP TABLE IF EXISTS test.{table_name};
    """
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully!")

    # Create table if it doesn't exist (modify columns as needed)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS test.{table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_nbr INT,
        family VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        class INT,
        perishable INT
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print(f"Table {table_name} created successfully!")

    # Insert data
    for _, row in df.iterrows():
        insert_query = f"""INSERT INTO test.{table_name} (
            item_nbr,
            family,
            class,
            perishable
        ) VALUES (%s, %s, %s, %s)"""
        # print(row)
        cursor.execute(insert_query, (
            row.iloc[0],
            row.iloc[1],
            row.iloc[2],
            row.iloc[3]))

    connection.commit()

    print(f"Table {table_name} successfully loaded into MySQL.")


def load_oil(cursor, connection, csv_file_path, table_name):
    row_id = 0
    # Read CSV file 
    df = pd.read_csv(csv_file_path, encoding="utf-8", sep=",")

    # Replace NaN with None for MySQL
    df = df.where(pd.notna(df), None)

    drop_table_query = f"""
        DROP TABLE IF EXISTS test.{table_name}; 
    """
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully!")

    # Create table if it doesn't exist (modify columns as needed)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS test.{table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        dcoilwtico DOUBLE
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print(f"Table {table_name} created successfully!")

    # Insert data   
    for _, row in df.iterrows():
        insert_query = f"""INSERT INTO test.{table_name} (
            date,
            dcoilwtico
        ) VALUES (%s, %s)"""
        # print(row)
        cursor.execute(insert_query, (
            row.iloc[0] if pd.notna(row.iloc[0]) else None,
            row.iloc[1] if pd.notna(row.iloc[1]) else -1))

    connection.commit()

    print(f"Table {table_name} successfully loaded into MySQL.")


def load_stores(cursor, connection, csv_file_path, table_name):
    row_id = 0
    # Read CSV file
    df = pd.read_csv(csv_file_path, encoding="utf-8", sep=",")


    # Replace NaN with None for MySQL
    df = df.where(pd.notna(df), None)

    drop_table_query = f"""
        DROP TABLE IF EXISTS test.{table_name};
    """

    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully!")

    # Create table if it doesn't exist (modify columns as needed)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS test.{table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        store_nbr INT,
        city VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        state VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        type VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        cluster INT
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print(f"Table {table_name} created successfully!")

    # Insert data
    for _, row in df.iterrows():
        insert_query = f"""INSERT INTO test.{table_name} (
            store_nbr,
            city,
            state,
            type,
            cluster
        ) VALUES (%s, %s, %s, %s, %s)"""
        # print(row)
        cursor.execute(insert_query, (
            int(row.iloc[0]) if pd.notna(row.iloc[0]) else -1,
            str(row.iloc[1]) if pd.notna(row.iloc[1]) else "",
            str(row.iloc[2]) if pd.notna(row.iloc[2]) else "",
            str(row.iloc[3]) if pd.notna(row.iloc[3]) else "",
            int(row.iloc[4]) if pd.notna(row.iloc[4]) else -1))

    connection.commit()

    print(f"Table {table_name} successfully loaded into MySQL.")


def load_transactions(cursor, connection, csv_file_path, table_name):
    row_id = 0
    # Read CSV file
    df = pd.read_csv(csv_file_path, encoding="utf-8", sep=",")

    # Replace NaN with None for MySQL
    df = df.where(pd.notna(df), None)

    drop_table_query = f"""
        DROP TABLE IF EXISTS test.{table_name};
    """
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully!")

    # Create table if it doesn't exist (modify columns as needed)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS test.{table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        store_nbr INT,
        transactions INT
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print(f"Table {table_name} created successfully!")

    # Insert data
    for _, row in df.iterrows():
        insert_query = f"""INSERT INTO test.{table_name} (
            date,
            store_nbr,
            transactions  
        ) VALUES (%s, %s, %s)"""
        # print(row)
        cursor.execute(insert_query, (
            row.iloc[0] if pd.notna(row.iloc[0]) else -1,
            int(row.iloc[1]) if pd.notna(row.iloc[1]) else None,
            int(row.iloc[2]) if pd.notna(row.iloc[2]) else -1))

    connection.commit()

    print(f"Table {table_name} successfully loaded into MySQL.")


def load_sales(cursor, connection, csv_file_path, table_name):
    row_id = 0
    # Read CSV file
    df = pd.read_csv(csv_file_path, encoding="utf-8", sep=",", nrows=10000)

    # Replace NaN with None for MySQL
    df = df.where(pd.notna(df), None)

    drop_table_query = f"""
        DROP TABLE IF EXISTS test.{table_name};
    """
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully!")

    # Create table if it doesn't exist (modify columns as needed)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS test.{table_name} (
        id INT PRIMARY KEY,
        date DATE,
        store_nbr INT,
        item_nbr INT,
        unit_sales DOUBLE,
        onpromotion INT
    );
    """ 
    cursor.execute(create_table_query)
    connection.commit()
    print(f"Table {table_name} created successfully!")

    # Insert data
    for _, row in df.iterrows():
        insert_query = f"""INSERT INTO test.{table_name} (
            id,
            date,
            store_nbr,
            item_nbr,
            unit_sales,
            onpromotion
        ) VALUES (%s, %s, %s, %s, %s, %s)"""
        #  print(row)  
        cursor.execute(insert_query, (
            int(row.iloc[0]) if pd.notna(row.iloc[0]) else -1,
            row.iloc[1] if pd.notna(row.iloc[1]) else None,
            int(row.iloc[2]) if pd.notna(row.iloc[2]) else -1,
            int(row.iloc[3]) if pd.notna(row.iloc[3]) else -1,
            float(row.iloc[4]) if pd.notna(row.iloc[4]) else -1,
            int(row.iloc[5]) if pd.notna(row.iloc[5]) else -1))

    connection.commit()

    print(f"Table {table_name} successfully loaded into MySQL.")


def normalize_path(path):
    """Convert Windows path to forward slashes and normalize it"""
    return os.path.normpath(path).replace('\\', '/')

def load_all_sales(cursor, connection, csv_file_path, table_name):
    """
    Load a large CSV file into MySQL using LOAD DATA LOCAL INFILE
    """
    start_time = time.time()
    
    # Normalize the file path
    normalized_path = normalize_path(csv_file_path)
    
    # Drop existing table
    drop_table_query = f"""
        DROP TABLE IF EXISTS test.{table_name};
    """
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully!")

    # Create table if it doesn't exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS test.{table_name} (
        id INT PRIMARY KEY,
        date DATE,
        store_nbr INT,
        item_nbr INT,
        unit_sales DOUBLE,
        onpromotion INT
    );
    """ 
    cursor.execute(create_table_query)
    connection.commit()
    print(f"Table {table_name} created successfully!")

    load_sql = f"""
        LOAD DATA LOCAL INFILE '{normalized_path}'
        INTO TABLE test.{table_name}
        FIELDS TERMINATED BY ',' 
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        (id, date, store_nbr, item_nbr, unit_sales, onpromotion);
    """

    try:
        print(f"Loading data from {normalized_path}...")
        cursor.execute(load_sql)
        connection.commit()
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM test.{table_name}")
        row_count = cursor.fetchone()[0]
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Successfully loaded {row_count:,} rows into {table_name}")
        print(f"Time taken: {duration:.2f} seconds")
        print(f"Loading speed: {row_count/duration:.2f} rows/second")
        
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        connection.rollback()
        raise

def main():
    # Connect to MySQL
    connection = pymysql.connect(
        host=DB_HOST, 
        port=DB_PORT, 
        user=DB_USER, 
        password=DB_PASSWORD,
        local_infile=True)
    cursor = connection.cursor()
    create_database(cursor, connection)
    try:
        load_holidays_events(cursor, connection, CSV_FILE_PATH + "holidays_events.csv", "holidays_events")
        load_items(cursor, connection, CSV_FILE_PATH + "items.csv", "items")
        load_oil(cursor, connection, CSV_FILE_PATH + "oil.csv", "oil")
        load_stores(cursor, connection, CSV_FILE_PATH + "stores.csv", "stores")
        load_transactions(cursor, connection, CSV_FILE_PATH + "transactions.csv", "transactions")
        load_sales(cursor, connection, CSV_FILE_PATH + "sales.csv", "sales_limit")
        # sales_file = os.path.join(CSV_FILE_PATH, "sales.csv")
        # load_all_sales(cursor, connection, sales_file, "sales")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()

