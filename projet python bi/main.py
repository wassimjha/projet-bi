import os
import subprocess
import time

def run_scraper():
    print("Running web scraper...")
    subprocess.run(["python", "scraper.py"])

def run_etl():
    print("Running ETL pipeline...")
    subprocess.run(["python", "etl.py"])

def run_dashboard():
    print("Launching dashboard...")
    subprocess.run(["python", "dashboard.py"])

def main():
    # Run Scraper
    run_scraper()

    # Wait before ETL
    time.sleep(2)
    run_etl()

    # Run Dashboard
    run_dashboard()

if __name__ == "__main__":
    main()
