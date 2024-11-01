
CREATE TABLE src_tbl_patients (
    id VARCHAR(36) PRIMARY KEY, -- TODO - change to UUID v4
    gender VARCHAR(10), -- binary? or leave it for "backward" compatibility
    birth_date DATE,
    name_prefix VARCHAR(10),
    name_given VARCHAR(50),
    name_family VARCHAR(50),
    marital_status VARCHAR(20),
    multiple_birth_boolean BOOLEAN,
    communication_language VARCHAR(50),
    address_line VARCHAR(100),
    address_city VARCHAR(50),
    address_state VARCHAR(2),
    address_postal_code VARCHAR(10),
    address_country VARCHAR(2),
    address_latitude DECIMAL(10, 8),
    address_longitude DECIMAL(11, 8),
    phone VARCHAR(20),
    full_name VARCHAR(100)
);

CREATE TABLE src_tbl_encounters (
    id VARCHAR(36) PRIMARY KEY, -- TODO - change to UUID v4
    patient_id VARCHAR(36),
    status VARCHAR(20),
    class VARCHAR(10),
    class_code VARCHAR(10),
    class_system VARCHAR(100),
    type VARCHAR(100),
    type_code VARCHAR(20),
    type_system VARCHAR(100),
    type_text VARCHAR(100),
    provider_id VARCHAR(100),
    reason_code VARCHAR(20),
    hospitalization_admit_source VARCHAR(10),
    hospitalization_discharge_disposition VARCHAR(10),
    start TIMESTAMP,
    end TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE src_tbl_medication_requests (
    id VARCHAR(36) PRIMARY KEY, -- TODO - change to UUID v4
    patient_id VARCHAR(36),
    status VARCHAR(20),
    intent VARCHAR(20),
    medication VARCHAR(100),
    code VARCHAR(20),
    display_name VARCHAR(100),
    reason VARCHAR(100),
    authored_on TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (code) REFERENCES src_tbl_active_medications(code)
);

CREATE TABLE src_tbl_active_medications (
    id VARCHAR(36) PRIMARY KEY, -- TODO - change to UUID v4
    code VARCHAR(20) UNIQUE,
    effective_time DATE,
    last_updated DATE,
    brand_name VARCHAR(100),
    generic_name VARCHAR(100),
    manufacturer_name VARCHAR(100),
    product_ndc VARCHAR(20),
    package_ndc VARCHAR(20),
    product_type VARCHAR(50),
    route VARCHAR(20),
    substance_name VARCHAR(100),
    rxcui VARCHAR(20),
    unii VARCHAR(20),
    elements TEXT,
    indications_and_usage TEXT,
    dosage_and_administration TEXT,
    description TEXT,
    warnings TEXT
);
