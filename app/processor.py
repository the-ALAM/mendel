import os
import json
import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm

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
    """The main function responsible for extracting patient, medication, and encounter data from a FHIR JSON file."""
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
                'birth_date': parse_date(resource.get('birthDate')),
                # 'name': resource.get('name', [{}])[0].get('text', ''),
                'name_prefix': safe_get(resource, ['name', 0, 'prefix'], [None])[0],
                'name_given': safe_get(resource, ['name', 0, 'given'], [None])[0], 
                'name_family': safe_get(resource, ['name', 0, 'family'], None),
                'marital_status': safe_get(resource, ['maritalStatus', 'text'], None),
                'multiple_birth_boolean': resource.get('multipleBirthBoolean', None),
                'communication_language': safe_get(resource, ['communication', 0, 'language', 'text'], None),
                # 'address': safe_get(resource, ['address', 0, 'text'], None),
                'address_line': safe_get(resource, ['address', 0, 'line'], [None])[0],
                'address_city': safe_get(resource, ['address', 0, 'city'], None),
                'address_state': safe_get(resource, ['address', 0, 'state'], None),
                'address_postalCode': safe_get(resource, ['address', 0, 'postalCode'], None),
                'address_country': safe_get(resource, ['address', 0, 'country'], None),
                'address_latitude': safe_get(resource, ['address', 0, 'extension', 0, 'extension', 0, 'valueDecimal'], None),
                'address_longitude': safe_get(resource, ['address', 0, 'extension', 0, 'extension', 1, 'valueDecimal'], None),
                'phone': safe_get(resource, ['telecom', 0, 'value'], None)
            }

        elif resource_type == 'MedicationRequest':
            medication_requests.append({
                'id': resource.get('id'),
                'patient_id': resource.get('subject', {}).get('reference', '').split('/')[-1][8:],
                'status': resource.get('status'),
                'intent': resource.get('intent'),
                'medication': resource.get('medicationCodeableConcept', {}).get('text'),
                'code': resource.get('medicationCodeableConcept', {}).get('coding', [{}])[0].get('code'),
                'display_name': resource.get('medicationCodeableConcept', {}).get('coding', [{}])[0].get('display'),
                'reason': resource.get('reasonReference', [{}])[0].get('display'),
                'authored_on': parse_date(resource.get('authoredOn'))
            })

        elif resource_type == 'Encounter':
            encounter_requests.append({
                'id': resource.get('id'),
                'patient_id': resource.get('subject', {}).get('reference', '').split('/')[-1][8:],
                'status': resource.get('status'),
                'class': resource.get('class', {}).get('code'),
                'class_code': safe_get(resource, ['class', 'code'], None),
                # 'class_system': safe_get(resource, ['class', 'system'], None),
                'type': resource.get('type', [{}])[0].get('text', ''),
                'type_code': safe_get(resource, ['type', 0, 'coding', 0, 'code'], None),
                # 'type_system': safe_get(resource, ['type', 0, 'coding', 0, 'system'], None),
                'type_text': safe_get(resource, ['type', 0, 'text'], None),
                'provider_id': resource.get('serviceProvider', {}).get('reference', '').split('/')[-1][7:],
                'reason_code': safe_get(resource, ['reasonCode', 0, 'coding', 0, 'code'], None),
                # 'reason_system': safe_get(resource, ['reasonCode', 0, 'coding', 0, 'system'], None),
                # 'reason_text': safe_get(resource, ['reasonCode', 0, 'text'], None),
                'hospitalization_admit_source': safe_get(resource, ['hospitalization', 'admitSource', 'coding', 0, 'code'], None),
                'hospitalization_discharge_disposition': safe_get(resource, ['hospitalization', 'dischargeDisposition', 'coding', 0, 'code'], None),
                'start': parse_date(safe_get(resource, ['period', 'start'], None)),
                'end': parse_date(safe_get(resource, ['period', 'end'], None))
            })

    return patient_info, medication_requests, encounter_requests

def process_json_files(directory):
    """Process all JSON files in the given directory and extract patient, medication, and encounter data."""
    all_patients = []
    all_medication_requests = []
    all_encounter_requests = []

    json_files = [filename for filename in os.listdir(directory) if filename.endswith('.json')]
    for filename in tqdm(json_files, desc="Reading JSON files"):
    # for filename in os.listdir(directory):
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
    # for code in fhir_product_codes:
    for code in tqdm(fhir_product_codes, desc="Requesting drug data"):
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


def main():
    """Main function.
    """
    patients, medications, encounters = process_json_files(DATA_DIRECTORY)

    patients_df = pd.DataFrame(patients)
    patients_df['full_name'] = patients_df['name_given'] + ' ' + patients_df['name_family']
    medication_requests_df = pd.DataFrame(medications)
    encounters_df = pd.DataFrame(encounters)
    active_medications_df = get_active_medications(medication_requests_df)

    df_names = ['src_tbl_active_medications', 'src_tbl_medication_requests', 'src_tbl_patients', 'src_tbl_encounters']
    df_list = [active_medications_df, medication_requests_df, patients_df, encounters_df]

    for df_name, df in tqdm(zip(df_names, df_list), desc="Exporting CSVs", total=len(df_names)):
        file_name = OUT_DIRECTORY+ '\\' +df_name+'.csv'
        print('csv_path: ', file_name)
        export_to_csv(df, file_name)

if __name__ == "__main__":
    main()
