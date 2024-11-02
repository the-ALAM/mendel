-- Add indexes
CREATE INDEX idx_patients_birth_date ON src_tbl_patients(birth_date);
CREATE INDEX idx_patients_address_state ON src_tbl_patients(address_state);

CREATE INDEX idx_encounters_patient_id ON src_tbl_encounters(patient_id);
CREATE INDEX idx_encounters_start ON src_tbl_encounters("start");
CREATE INDEX idx_encounters_end ON src_tbl_encounters("end");

CREATE INDEX idx_medication_requests_patient_id ON src_tbl_medication_requests(patient_id);
CREATE INDEX idx_medication_requests_authored_on ON src_tbl_medication_requests(authored_on);

CREATE INDEX idx_active_medications_code ON src_tbl_active_medications(code);
CREATE INDEX idx_active_medications_brand_name ON src_tbl_active_medications(brand_name);
CREATE INDEX idx_active_medications_generic_name ON src_tbl_active_medications(generic_name);
