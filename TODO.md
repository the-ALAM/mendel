
# Mendel.AI Data Engineering Assessment

You are provided with the data of 100 dummy patients in JSON format adhering to the FHIR (Fast Healthcare Interoperability Resources) standard. Your task is to convert this data into structured tables in an SQL database by extracting relevant fields from the JSON files. Additionally, you are required to query the FDA Drug Label API to obtain medication information for all medications in the patient dataset and create a corresponding table in the SQL database.

Furthermore, you need to containerize your application in a reproducible manner and use a scheduler to automate the workflow of data extraction, transformation, and loading (ETL) into the SQL database.

---

## TODOs

### service

- [x] validate FHIR JSON files
- [x] (FDA Drug Label API interaction)
- [x] (handles data extraction from FHIR JSON files)
- [x] (data transformation logic)
- [x] extract relevant fields from the JSON files
- [x] more info on patients and encounters
- [ ] add main functions at each script
- [ ] (database loading functions)
- [ ] (orchestrates the entire ETL process)
- [ ] (scheduling logic)
- [ ] (configuration settings)
- [ ] (OPTIONAL) TQDM progress bar

### pgdb

- [ ] proper schema
- [ ] medications table

### scheduler

- [ ] dont over complicate it use a bash script with a cron job
- [ ] (OPTIONAL) use airflow - BEWARE undifferentiated heavy lifting

## WIP

- loading

## DONE

None

## FIXME/NOTE

- [ ] make a utilities module

---

## deliverables

```YML
input:
    data: 100 dummy patients in FHIR

process:
    - convert this data into structured tables in an SQL database by extracting relevant fields from the JSON files
    - query the FDA Drug Label API to obtain medication information for all medications in the patient dataset
    - create a corresponding table in the SQL database.

output:
    docker_container:
        pgdb:
            - extract relevant fields from the JSON files
            - medications table
        service:
            - does all the ETL in functional matter that can be called by the scheduler
            - query the FDA Drug Label API to obtain medication information for all medications in the patient dataset
        scheduler: 
            - extraction
            - transformation
            - loading
            - on an interval job
    documentation:
        - how to build and run the Docker container
        - Instructions on how to set up and run the scheduler
        - SQL schema for the structured tables
    queries:
        - to create the necessary tables in the database
        - to verify the data in the tables and basic functionalities
```

**(optional)** unit tests for all of them **WHEN YOU FINISH**
**(optional)** data management > governance and quality
