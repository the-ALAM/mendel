
# import os
import time
import schedule
import processor
import loader
from tqdm import tqdm
from datetime import datetime, timedelta

def run_etl_with_progress():
    """Run the ETL process with progress bars.
    Returns:
        bool: True if the ETL process was successful, False otherwise.
    """
    print("Running ETL tasks...")
    try:
        # Overall progress bar
        with tqdm(total=3, desc="Overall ETL Progress") as pbar:
            print("\nStarting data processing...")
            processor.main()
            print("Data processing (extraction and transformation) completed successfully")
            pbar.update(1)

            print("\Cooldown between tasks...")
            for _ in tqdm(range(5), desc="Cooldown"):
                time.sleep(1)
            pbar.update(1)

            print("\nStarting data loading...")
            loader.main()
            print("Data loading completed successfully")
            pbar.update(1)

        return True
    except Exception as e:
        print(f"ETL process failed: {e}")
        return False

def run_etl():
    """Run the ETL process on a daily basis at an interval.
    Returns:
        bool: True if the ETL process was successful, False otherwise.
    """
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
    # schedule.every().day.at("03:47").do(run_etl)
    schedule.every().day.at("14:15").do(run_etl_with_progress)

    while True:
        schedule.run_pending()
        time.sleep(20)

if __name__ == "__main__":
    main()
