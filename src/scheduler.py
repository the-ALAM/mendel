
import time
import processor
import loader
import schedule

def run_etl():
    # TODO: Implement your ETL logic here
    print("Running ETL tasks...")
    try:
        print("Starting data processing...")
        processor.main()
        print("Data processing (extraction and transformation) completed successfully")

        time.sleep(10)

        print("Starting data loading...")
        loader.main()
        print("Data loading completed successfully")

        return True
    except Exception as e:
        print(f"ETL process failed: {e}")
        return False

def main():
    """Main function.
    """
    schedule.every().day.at("02:00").do(run_etl)

    while True:
        schedule.run_pending()
        time.sleep(20)

if __name__ == "__main__":
    main()
