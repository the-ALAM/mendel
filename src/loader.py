
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from psycopg2 import sql
from sqlalchemy import create_engine

load_dotenv()

HOST=os.getenv('POSTGRES_HOST')
PORT=os.getenv('POSTGRES_PORT')
DATABASE=os.getenv('POSTGRES_DB')
USER=os.getenv('POSTGRES_USER')
PASSWORD=os.getenv('POSTGRES_PASSWORD')
SSLMODE=os.getenv('POSTGRES_SSLMODE')

PATIENT_MEDICATIONS_QUERY = """ SELECT am.brand_name, mr.authored_on
        FROM medication_requests mr
        JOIN active_medications am ON mr.code = am.code
        WHERE mr.patient_id = %s """

ENCOUNTERS_BY_DATE_RANGE_QUERY = """ SELECT e.id, e.patient_id, e.start, e.end, p.full_name
        FROM encounters e
        JOIN patients p ON e.patient_id = p.id
        WHERE e.start >= %s AND e.end <= %s """

PATIENT_ID = 'c16b9aea-2b5f-3866-22a1-01dea645c9e1'

OUT_DIRECTORY ='C://locr//mendel//out'

CREATE_TABLES_QUERY_PATH = 'C://locr//mendel//sql//create_tables.sql'
LOAD_DATA_QUERY_PATH = 'C://locr//mendel//sql//load_data.sql'
CREATE_INDEXES_QUERY_PATH = 'C://locr//mendel//sql//create_indexes.sql'


def test_connection():
    """Test the connection to the database.
    Returns: Bool
    """
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE,
            sslmode=SSLMODE
        )
        cursor = conn.cursor()
        cursor.execute('select 1;')
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def test_data():
    """Test basic ops.
    Returns: Bool
    """
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE,
            sslmode=SSLMODE
        )
        cur = conn.cursor()

        def get_patient_medications(patient_id):
            query = sql.SQL(PATIENT_MEDICATIONS_QUERY)
            cur.execute(query, (patient_id,))
            return cur.fetchall()

        def get_encounters_by_date_range(start_date, end_date):
            query = sql.SQL(ENCOUNTERS_BY_DATE_RANGE_QUERY)
            cur.execute(query, (start_date, end_date))
            return cur.fetchall()

        patient_meds = get_patient_medications(PATIENT_ID)
        for med in patient_meds:
            print(f"Medication: {med[0]}, Prescribed on: {med[1]}")

        encounters = get_encounters_by_date_range('2010-01-01', '2020-01-01')
        for encounter in encounters:
            print(f"Encounter ID: {encounter[0]}, Patient: {encounter[4]}, Start: {encounter[2]}, End: {encounter[3]}")

        conn.commit()
        cur.close()
        conn.close()
        return True, patient_meds, encounters
    except Exception as e:
        print(e)
        return False


def execute_sql_file(filepath):
    """Execute SQL commands from a file.
    Args:
        filepath (str): Path to SQL file
    Returns:
        bool: Success status
    """
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD, 
            host=HOST,
            port=PORT,
            database=DATABASE,
            sslmode=SSLMODE
        )
        cursor = conn.cursor()

        with open(filepath, 'r', encoding='utf-8') as f:
            sql_commands = f.read()

        commands = []
        current_command = []
        in_quotes = False
        for char in sql_commands:
            if char == '"' or char == "'":
                in_quotes = not in_quotes
            current_command.append(char)
            if char == ';' and not in_quotes:
                commands.append(''.join(current_command))
                current_command = []

        for command in commands:
            if command.strip():
                cursor.execute(command)

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error executing {filepath}: {e}")
        return False

def run_sql_files(file_paths):
    """Run multiple SQL files in sequence.
    Args:
        file_paths (list): List of SQL file paths
    Returns:
        bool: Overall success status
    """
    success = True
    for filepath in file_paths:
        print(f'running filepath: {filepath}')
        if not execute_sql_file(filepath):
            print(f'error executing filepath: {filepath}')
            success = False
            break
        print(f"Successfully executed {filepath}")
    return success

def upload_csv_to_database(directory):
    """Upload CSV files from a directory to the database."""
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE,
            sslmode=SSLMODE
        )
        cursor = conn.cursor()

        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                table_name = os.path.splitext(filename)[0]
                csv_path = os.path.join(directory, filename)

                df = pd.read_csv(csv_path)

                cols = ", ".join([f"\"{col}\" TEXT" for col in df.columns])
                create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})"
                cursor.execute(create_table)

                values = [tuple(row) for row in df.values]
                placeholders = ", ".join(["%s"] * len(df.columns))
                insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

                cursor.executemany(insert_query, values)
                conn.commit()
                print(f"Uploaded {filename} to table {table_name}")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error uploading CSV files: {e}")
        return False


def main():
    """Main function.
    """

    print("testing database connection please wait...\nis connected?", test_connection())

    # sql_files = [CREATE_TABLES_QUERY_PATH, CREATE_INDEXES_QUERY_PATH]
    # for file in sql_files:
    #     print(f"Executing {file}...")
    #     success = execute_sql_file(file)
    #     if success:
    #         print(f"Successfully executed {file}")
    #     else:
    #         print(f"Failed to execute {file}")
    #         continue # optional to break out of loop

    print("Uploading CSV files from OUT_DIRECTORY...")
    upload_csv_to_database(OUT_DIRECTORY)

if __name__ == '__main__':
    main()
