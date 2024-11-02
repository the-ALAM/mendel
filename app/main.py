
import os
import argparse
from scheduler import schedule_etl, run_etl_with_progress
# try:
#     from scheduler import schedule_etl, run_etl_with_progress
# except ImportError:
#     from app.scheduler import schedule_etl, run_etl_with_progress

def main():
    """Main entry point for the ETL pipeline.
    Parses command line arguments and schedules/runs the ETL process accordingly.
    """
    print("directory contents\n", os.system('dir'))
    parser = argparse.ArgumentParser(description='ETL Pipeline Runner')
    parser.add_argument('--interval', type=str, default='once',
                        choices=['daily', 'hourly', 'once'],
                        help='Run interval: daily, hourly, or once')
    parser.add_argument('--time', type=str, default='14:15',
                        help='Start time for daily jobs (HH:MM format)')

    args = parser.parse_args()

    print(f"Starting ETL pipeline with {args.interval} interval")
    if args.interval == 'once':
        print("Running single ETL job...")
        run_etl_with_progress()
    else:
        print(f"Scheduling ETL job to run {args.interval} at {args.time}")
        schedule_etl(interval=args.interval, 
                    start_time=args.time,
                    func=run_etl_with_progress)

if __name__ == "__main__":
    main()
