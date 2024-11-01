
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from psycopg2 import sql
# from sqlalchemy import create_engine

load_dotenv()

host=os.getenv('POSTGRES_HOST')
port=os.getenv('POSTGRES_PORT')
database=os.getenv('POSTGRES_DB')
user=os.getenv('POSTGRES_USER')
password=os.getenv('POSTGRES_PASSWORD')
sslmode=os.getenv('POSTGRES_SSLMODE')

def test_connection():
    """Test the connection to the database.
    Returns: Bool
    """
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            sslmode=sslmode
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

print("testing connection please wait...\nis connected?", test_connection())


load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    sslmode=os.getenv('POSTGRES_SSLMODE')
)

cur = conn.cursor()

PATIENT_MEDICATIONS_QUERY = """ SELECT am.brand_name, mr.authored_on
        FROM medication_requests mr
        JOIN active_medications am ON mr.code = am.code
        WHERE mr.patient_id = %s """

encounters_by_date_range_QUERY = """ SELECT e.id, e.patient_id, e.start, e.end, p.full_name
        FROM encounters e
        JOIN patients p ON e.patient_id = p.id
        WHERE e.start >= %s AND e.end <= %s """


def get_patient_medications(patient_id):
    query = sql.SQL(PATIENT_MEDICATIONS_QUERY)
    cur.execute(query, (patient_id,))
    return cur.fetchall()

def get_encounters_by_date_range(start_date, end_date):
    query = sql.SQL(encounters_by_date_range_QUERY)
    cur.execute(query, (start_date, end_date))
    return cur.fetchall()

PATIENT_ID = 'c16b9aea-2b5f-3866-22a1-01dea645c9e1'
patient_meds = get_patient_medications(PATIENT_ID)
for med in patient_meds:
    print(f"Medication: {med[0]}, Prescribed on: {med[1]}")

encounters = get_encounters_by_date_range('2010-01-01', '2020-01-01')
for encounter in encounters:
    print(f"Encounter ID: {encounter[0]}, Patient: {encounter[4]}, Start: {encounter[2]}, End: {encounter[3]}")

cur.close()
conn.close()
