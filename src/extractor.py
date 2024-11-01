
# TODO - (handles data extraction from FHIR JSON files)

import os
import json
import pandas as pd
from datetime import datetime

# TODO - validate FHIR JSON files

JSON_DIRECTORY = 'C:\\locr\\mendel\\data\\'

def parse_date(date_string):
    """Parse an ISO 8601 formatted date string to a datetime object."""
    if date_string:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    return None

def extract_data_from_json(file_path):
    """Extract patient, medication, and encounter data from a FHIR JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
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
            file_path = os.path.join(directory, filename)
            patient, medication_requests, encounters_requests = extract_data_from_json(file_path)

            if patient:
                all_patients.append(patient)
            all_medication_requests.extend(medication_requests)
            all_encounter_requests.extend(encounters_requests)

    return all_patients, all_medication_requests, all_encounter_requests


patients, medications, encounters = process_json_files(JSON_DIRECTORY)

df_patients = pd.DataFrame(patients)
df_medication_requests = pd.DataFrame(medications)
df_encounters = pd.DataFrame(encounters)

print("Patients:")
print(df_patients.head())
print("\nMedication Requests:")
print(df_medication_requests.head())
print("\nEncounters:")
print(df_encounters.head())

df_patients.to_csv('patients.csv', index=False)
df_medication_requests.to_csv('medication_requests.csv', index=False)
df_encounters.to_csv('encounters.csv', index=False)
