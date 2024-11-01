import requests

# Replace with the drug name or RxNorm code from FHIR MedicationRequest
drug_active_ingredient = "acetaminophen"  # Or, use the RxNorm code if available
mai_url = f"https://api.fda.gov/drug/label.json?search=active_ingredient:{drug_active_ingredient}"
FHIR_product_code = "1535362"  
pc_url = f"https://api.fda.gov/drug/label.json?search={FHIR_product_code}"

response = requests.get(pc_url, timeout=5)
if response.status_code == 200:
    drug_data = response.json()
    print(drug_data)
    # print('***********************************')
    # print(drug_data['meta'])
    # print('***********************************')
    # print(drug_data['results'][0])
else:
    print(f"Error: {response.status_code}")

# spl_product_data_elements
# indications_and_usage
# dosage_and_administration
# description
# warnings
# storage_and_handling
# spl_unclassified_section
# package_label_principal_display_panel

# brand_name
# generic_name
# manufacturer_name
# effective_time
