-- Add indexes
CREATE INDEX idx_patients_birth_date ON patients(birth_date);
CREATE INDEX idx_patients_address_state ON patients(address_state);

CREATE INDEX idx_encounters_patient_id ON encounters(patient_id);
CREATE INDEX idx_encounters_start ON encounters(start);
CREATE INDEX idx_encounters_end ON encounters(end);

CREATE INDEX idx_medication_requests_patient_id ON medication_requests(patient_id);
CREATE INDEX idx_medication_requests_authored_on ON medication_requests(authored_on);

CREATE INDEX idx_active_medications_code ON active_medications(code);
CREATE INDEX idx_active_medications_brand_name ON active_medications(brand_name);
CREATE INDEX idx_active_medications_generic_name ON active_medications(generic_name);
