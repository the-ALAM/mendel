COPY src_tbl_patients FROM 'C:\locr\mendel\out\patients_df.csv' WITH CSV HEADER;
COPY src_tbl_encounters FROM 'C:\locr\mendel\out\encounters_df.csv' WITH CSV HEADER;
COPY src_tbl_medication_requests FROM 'C:\locr\mendel\out\medication_requests_df.csv' WITH CSV HEADER;
COPY src_tbl_active_medications FROM 'C:\locr\mendel\out\active_medications_df.csv' WITH CSV HEADER;