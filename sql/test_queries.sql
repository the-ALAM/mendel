
-- test querying patients
SELECT am.brand_name, mr.authored_on
FROM medication_requests mr
JOIN active_medications am ON mr.code = am.code
WHERE mr.patient_id = 'c16b9aea-2b5f-3866-22a1-01dea645c9e1';

-- test querying encounters
SELECT e.id, e.patient_id, e.start, e.end, p.full_name
FROM encounters e
JOIN patients p ON e.patient_id = p.id
WHERE e.start >= '2010-01-01' AND e.end <= '2020-01-01';

-- test querying patients and encounters

-- TODO 

-- test querying medications

-- TODO 
