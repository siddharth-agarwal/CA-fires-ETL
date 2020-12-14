The .py scripts in the `process` folder retrieve & extract historical data having to do with CA forest fires. 

The `live_fire_scraper.py` script retrieves data similarly formatted, but only for *live* (current) forest fires.

The `upload.sh` bash script uploads the extracted CSV files to a pre-specified S3 bucket (using the $S3_DOWNLOADS bucket PATH variable).

All data is sourced from CAL FIRE (https://www.fire.ca.gov).
