
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

def schedule_etl(interval='daily', start_time='14:15', func=run_etl_with_progress):
    """Schedule ETL job to run at specified interval and time
    Args:
        interval (str): 'daily', 'hourly', or 'once'
        start_time (str): Time to run in HH:MM format for daily/once jobs
        func (callable): ETL function to run
    """
    if interval == 'daily':
        schedule.every().day.at(start_time).do(func)
    elif interval == 'hourly':
        schedule.every().hour.at(":00").do(func)
    elif interval == 'once':
        schedule.every().day.at(start_time).do(func).tag('once')
        while True:
            schedule.run_pending()
            if not schedule.get_jobs('once'):
                break
            time.sleep(1)
    else:
        raise ValueError("Interval must be 'daily', 'hourly', or 'once'")


def main():
    """Main function.
    """

    schedule_etl()

    while True:
        schedule.run_pending()
        time.sleep(20)

if __name__ == "__main__":
    main()
