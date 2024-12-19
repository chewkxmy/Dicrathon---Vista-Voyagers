import csv
import sqlite3
from datetime import datetime

import csv

def read_csv(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
    except UnicodeDecodeError:
        # If UTF-8 fails, try Latin-1 encoding
        with open(file_path, mode='r', encoding='latin1') as file:
            reader = csv.reader(file)
            data = list(reader)
    return data

def create_database(csv_data, db_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Get column names from the first row of CSV data
    columns = csv_data[0]

    # Generate SQL query to create table with dynamic columns
    create_table_query = f"CREATE TABLE IF NOT EXISTS category_categoryactivities ({', '.join([f'{column} TEXT' for column in columns])})"
    c.execute(create_table_query)

    # Insert data into table
    for row in csv_data[1:]:
        # Check if 'published_date' exists and format as datetime
        if 'published_date' in columns:
            index = columns.index('published_date')
            try:
                row[index] = datetime.strptime(row[index], '%Y-%m-%d').isoformat()
            except ValueError:
                # Use current datetime if conversion fails
                row[index] = datetime.now().isoformat()

        c.execute(f"INSERT INTO category_categoryactivities VALUES ({', '.join(['?' for _ in range(len(row))])})", row)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def main():
    # Path to CSV file
    csv_file_path = 'smart-trips\\category\\data-article.csv'
    
    # Path to SQLite database file
    db_file = 'smart-trips\\db.sqlite3'

    # Read data from CSV
    csv_data = read_csv(csv_file_path)

    # Create SQLite database and insert data
    create_database(csv_data, db_file)

    print("Database created successfully!")

if __name__ == "__main__":
    main()
