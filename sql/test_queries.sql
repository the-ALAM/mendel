
-- test tables existence
select * 
from information_schema.tables 
where table_schema <> 'pg_catalog' and table_schema <> 'information_schema';

-- test indeces existence
select *
from pg_indexes
where schemaname <> 'pg_catalog' and schemaname <> 'information_schema';

-- test querying patients' meds
SELECT am.brand_name, mr.authoredon
FROM src_tbl_medication_requests mr
JOIN active_medications am ON mr.code = am.code
WHERE mr.patient_id = 'c16b9aea-2b5f-3866-22a1-01dea645c9e1';

-- test querying encounters
SELECT e.id, e.patient_id, e.start, e.end, p.full_name
FROM src_tbl_encounters e
JOIN src_tbl_patients p ON e.patient_id = p.id
WHERE e.start >= '2010-01-01' AND e.end <= '2020-01-01';

-- test querying patients and encounters

-- TODO 

-- test querying medications

-- TODO 
