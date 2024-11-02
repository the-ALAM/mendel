
# import os
import time
from datetime import datetime
import schedule
import processor as processor
import loader as loader

# try:
#     import processor
# except ImportError:
#     import app.processor as processor

# try:
#     import loader
# except ImportError:
#     import app.loader as loader

from tqdm import tqdm

def run_etl_with_progress():
    """Run the ETL process with progress bars.
    Returns:
        bool: True if the ETL process was successful, False otherwise.
    """
    print("Running ETL tasks...")
    try:
        with tqdm(total=3, desc="Overall ETL Progress") as pbar:

            print("\nStarting data processing...")
            processor.main()
            print("Data processing (extraction and transformation) completed successfully")
            pbar.update(1)

            print("\nCooldown between tasks...")
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


def parse_cron_expression(expression):
    """Parse a cron-like expression and return a tuple of (minute, hour, day, month, weekday).
    Args:
        expression (str): Cron-like expression (e.g., "0 0 * * *")
    Returns:
        tuple: (minute, hour, day, month, weekday)
    """
    parts = expression.split()
    if len(parts) != 5:
        raise ValueError("Invalid cron expression")
    return tuple(parts)

def should_run(cron_expression):
    """Check if the current time matches the cron expression.
    Args:
        cron_expression (str): Cron-like expression (e.g., "0 0 * * *")
    Returns:
        bool: True if the current time matches the cron expression, False otherwise.
    """
    minute, hour, day, month, weekday = parse_cron_expression(cron_expression)
    now = datetime.now()
    
    if (minute == '*' or int(minute) == now.minute) and \
       (hour == '*' or int(hour) == now.hour) and \
       (day == '*' or int(day) == now.day) and \
       (month == '*' or int(month) == now.month) and \
       (weekday == '*' or int(weekday) == now.weekday()):
        return True
    
    return False


def main():
    """Main function.
    """

    # package-based scheduling
    schedule_etl(interval='once', start_time='14:15', func=run_etl_with_progress)
    while True:
        schedule.run_pending()
        time.sleep(60)

    # cron-based scheduling
    # cron_expression = "*0 14 * * 0"
    # while True:
    #     if should_run(cron_expression):
    #         run_etl_with_progress()
    #     time.sleep(60)

if __name__ == "__main__":
    main()
