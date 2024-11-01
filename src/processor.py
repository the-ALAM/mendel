import os
import json
import requests
import pandas as pd
from datetime import datetime

PROJECT_DIRECTORY = os.path.normpath(os.getcwd())
DATA_DIRECTORY = os.path.normpath(os.getcwd() + os.sep + 'data\\')
OUT_DIRECTORY = os.path.normpath(os.getcwd() + os.sep + 'out\\')
print("PROJECT_DIRECTORY", PROJECT_DIRECTORY)
print("DATA_DIRECTORY", DATA_DIRECTORY)
print("OUT_DIRECTORY", OUT_DIRECTORY)


def parse_date(date_string):
    """Parse an ISO 8601 formatted date string to a datetime object."""
    if date_string:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    return None

def format_date(date_string: str):
    """Parse an ISO 8601 formatted date string to a datetime object."""
    if date_string:
        return (date_string[:4] + '-' + date_string[4:6] + '-' + date_string[6:])
    return None

def validate_fhir_json(json_data):
                """Validate that JSON follows basic FHIR resource format requirements."""
                if not isinstance(json_data, dict):
                    return False
                
                # Check required FHIR elements
                if 'resourceType' not in json_data:
                    return False
                    
                # Check entry array exists and contains resources
                if 'entry' not in json_data:
                    return False
                    
                entries = json_data.get('entry', [])
                if not isinstance(entries, list):
                    return False
                    
                # Validate each entry has resource and resourceType
                for entry in entries:
                    if not isinstance(entry, dict):
                        return False
                    if 'resource' not in entry:
                        return False
                    if 'resourceType' not in entry['resource']:
                        return False
                        
                return True

def safe_get(dictionary, keys, default=None):
    for key in keys:
        try:
            dictionary = dictionary[key]
        except (KeyError, IndexError, TypeError):
            return default
    return dictionary

def export_to_csv(dataframe, csv_path):
    """Export a DataFrame to a CSV file."""
    dataframe.to_csv(csv_path, index=False)


def extract_data_from_json(json_file_path):
    """Extract patient, medication, and encounter data from a FHIR JSON file."""
    print("processing: ", json_file_path)
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    patient_info = {}
    medication_requests = []
    encounter_requests = []

    for entry in data.get('entry', []):
        resource = entry.get('resource', {})
        resource_type = resource.get('resourceType')

        if resource_type == 'Patient':
            patient_info = {
                'id': resource.get('id'),
                'gender': resource.get('gender'),
                'birthDate': parse_date(resource.get('birthDate')),
                'name': resource.get('name', [{}])[0].get('text', '')
            }

        elif resource_type == 'MedicationRequest':
            medication_requests.append({
                'id': resource.get('id'),
                'patient_id': resource.get('subject', {}).get('reference', '').split('/')[-1],
                'status': resource.get('status'),
                'intent': resource.get('intent'),
                'medication': resource.get('medicationCodeableConcept', {}).get('text'),
                'code': resource.get('medicationCodeableConcept', {}).get('coding', [{}])[0].get('code'),
                'display_name': resource.get('medicationCodeableConcept', {}).get('coding', [{}])[0].get('display'),
                'reason': resource.get('reasonReference', [{}])[0].get('display'),
                'authoredOn': parse_date(resource.get('authoredOn'))
            })

        elif resource_type == 'Encounter':
            encounter_requests.append({
                'id': resource.get('id'),
                'patient_id': resource.get('subject', {}).get('reference', '').split('/')[-1],
                'status': resource.get('status'),
                'class': resource.get('class', {}).get('code'),
                'type': resource.get('type', [{}])[0].get('text', ''),
                # 'display': resource.get('type', [{}])[0].get('coding', [{}])[0].get('display'),
                'start': parse_date(resource.get('period', {}).get('start')),
                'end': parse_date(resource.get('period', {}).get('end'))
            })

    return patient_info, medication_requests, encounter_requests

def process_json_files(directory):
    """Process all JSON files in the given directory and extract patient, medication, and encounter data."""
    all_patients = []
    all_medication_requests = []
    all_encounter_requests = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_path = os.path.join(directory, filename)

            with open(json_path, encoding='utf-8') as f:
                print(f"checking: {filename}")
                json_data = json.load(f)

            if not validate_fhir_json(json_data):
                print(f"Invalid FHIR JSON format in file: {filename}")
                continue

            patient, medication_requests, encounters_requests = extract_data_from_json(json_path)

            if patient:
                all_patients.append(patient)
            all_medication_requests.extend(medication_requests)
            all_encounter_requests.extend(encounters_requests)

    return all_patients, all_medication_requests, all_encounter_requests


def search_fda_drugs(drug_code):
    url = f"https://api.fda.gov/drug/label.json?search={drug_code}"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        drug_data = response.json()
        return drug_data
    else:
        print(f"Error: {response.status_code}")

def extract_medication_data(result):

    return {
        'id': safe_get(result, ['results', 0, 'id'], None),
        'code': safe_get(result, ['results', 0, 'openfda', 'rxcui'], [None])[0],
        'effective_time': format_date(safe_get(result, ['results', 0, 'effective_time'], None)),
        'last_updated': safe_get(result, ['meta', 'last_updated'], None),

        'brand_name': safe_get(result, ['results', 0, 'openfda', 'brand_name'], [None])[0],
        'generic_name': safe_get(result, ['results', 0, 'openfda', 'generic_name'], [None])[0],
        'manufacturer_name': safe_get(result, ['results', 0, 'openfda', 'manufacturer_name'], [None])[0],
        'product_ndc': safe_get(result, ['results', 0, 'openfda', 'product_ndc'], [None]),#[0], # pass the list
        'package_ndc': safe_get(result, ['results', 0, 'openfda', 'package_ndc'], None),
        'product_type': safe_get(result, ['results', 0, 'openfda', 'product_type'], [None])[0],
        'route': safe_get(result, ['results', 0, 'openfda', 'route'], [None])[0],
        'substance_name': safe_get(result, ['results', 0, 'openfda', 'substance_name'], [None])[0],
        'rxcui': safe_get(result, ['results', 0, 'openfda', 'rxcui'], [None]),#[0], # pass the list
        'unii': safe_get(result, ['results', 0, 'openfda', 'unii'], None),

        'elements': safe_get(result, ['results', 0, 'spl_product_data_elements'], [None])[0],
        'indications_and_usage': safe_get(result, ['results', 0, 'indications_and_usage'], [None])[0],
        'dosage_and_administration': safe_get(result, ['results', 0, 'dosage_and_administration'], [None])[0],
        'description': safe_get(result, ['results', 0, 'description'], [None])[0],
        'warnings': safe_get(result, ['results', 0, 'warnings'], [None])[0]
    }

def generate_medication_df(fhir_product_codes):
    medications_list = []
    for code in fhir_product_codes:
        response = search_fda_drugs(code)
        medication = extract_medication_data(response)
        medications_list.append(medication)

    medications_df = pd.DataFrame(medications_list)
    return medications_df

def get_active_medications(medication_requests):
    active_statuses = ['active',]
    active_medications = medication_requests[medication_requests['status'].isin(active_statuses)]
    
    drug_codes = active_medications['code'].tolist()
    medications_df = generate_medication_df(drug_codes)
    return medications_df


patients, medications, encounters = process_json_files(DATA_DIRECTORY)

patients_df = pd.DataFrame(patients)
medication_requests_df = pd.DataFrame(medications)
encounters_df = pd.DataFrame(encounters)
active_medications_df = get_active_medications(medication_requests_df)

df_names = ['active_medications_df', 'medication_requests_df', 'patients_df', 'encounters_df']
df_list = [active_medications_df, medication_requests_df, patients_df, encounters_df]

for df_name, df in zip(df_names, df_list):
    file_name = OUT_DIRECTORY+ '\\' +df_name+'.csv'
    print('csv_path: ', file_name)
    export_to_csv(df, file_name)
