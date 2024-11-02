
-- test tables existence
select * 
from information_schema.tables 
where table_schema <> 'pg_catalog' and table_schema <> 'information_schema';

-- test indeces existence
select *
from pg_indexes
where schemaname <> 'pg_catalog' and schemaname <> 'information_schema';

-- count total patients
SELECT COUNT(*) as total_patients 
FROM src_tbl_patients;

-- count patients by gender
SELECT gender, COUNT(*) as patient_count
FROM src_tbl_patients
GROUP BY gender;

-- count patients by state
SELECT address_state, COUNT(*) as patient_count 
FROM src_tbl_patients
GROUP BY address_state
ORDER BY patient_count DESC;

-- count total encounters
SELECT COUNT(*) as total_encounters
FROM src_tbl_encounters;

-- encounters by type
SELECT type, COUNT(*) as encounter_count
FROM src_tbl_encounters
GROUP BY type
ORDER BY encounter_count DESC;

-- encounters by class
SELECT class, COUNT(*) as encounter_count 
FROM src_tbl_encounters
GROUP BY class
ORDER BY encounter_count DESC;

-- average encounter duration in days
SELECT AVG(EXTRACT(EPOCH FROM ("end" - "start"))/86400) as avg_duration_days
FROM src_tbl_encounters
WHERE "start" IS NOT NULL AND "end" IS NOT NULL;

-- count total medications
SELECT COUNT(*) as total_medications
FROM src_tbl_active_medications;

-- medications by route
SELECT route, COUNT(*) as med_count
FROM src_tbl_active_medications
GROUP BY route
ORDER BY med_count DESC;

-- count medication requests
SELECT COUNT(*) as total_med_requests
FROM src_tbl_medication_requests;

-- medication requests by status
SELECT status, COUNT(*) as request_count
FROM src_tbl_medication_requests
GROUP BY status
ORDER BY request_count DESC;

-- top 10 most prescribed medications
SELECT am.brand_name, COUNT(*) as prescription_count
FROM src_tbl_medication_requests mr
JOIN src_tbl_active_medications am ON mr.code = am.code
GROUP BY am.brand_name
ORDER BY prescription_count DESC
LIMIT 10;

-- test querying patients' meds
SELECT am.brand_name, mr.authored_on
FROM src_tbl_medication_requests mr
JOIN active_medications am ON mr.code = am.code
WHERE mr.patient_id = 'c16b9aea-2b5f-3866-22a1-01dea645c9e1';

-- test querying encounters
SELECT e.id, e.patient_id, e."start", e."end", p.full_name
FROM src_tbl_encounters e
JOIN src_tbl_patients p ON e.patient_id = p.id
WHERE e.start >= '2010-01-01' AND e.end <= '2020-01-01';
