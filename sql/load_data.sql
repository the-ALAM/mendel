COPY patients FROM 'C:\locr\mendel\out\patients_df.csv' WITH CSV HEADER;
COPY encounters FROM 'C:\locr\mendel\out\encounters_df.csv' WITH CSV HEADER;
COPY medication_requests FROM 'C:\locr\mendel\out\medication_requests_df.csv' WITH CSV HEADER;
COPY active_medications FROM 'C:\locr\mendel\out\active_medications_df.csv' WITH CSV HEADER;