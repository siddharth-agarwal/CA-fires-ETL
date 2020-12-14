

aws s3 cp result.zip "$S3_ARCHIVE" --quiet

gzip *.csv

aws s3 cp . "$S3_DOWNLOADS" --recursive --exclude "*" --include "*.csv.gz" --quiet
