import argparse
import boto3
import urllib.request
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-04.parquet"
FILENAME = "yellow_tripdata_2026-04.parquet"
TMP_PATH = f"/tmp/{FILENAME}"

parser = argparse.ArgumentParser()
parser.add_argument("--output_bucket", required=True, help="S3 bucket for the downloaded parquet file")
parser.add_argument("--output_prefix", default="yellow/2026/04", help="S3 key prefix (folder path)")
# Glue injects --JOB_NAME and other internal args; parse_known_args ignores them
args, _ = parser.parse_known_args()

logger.info(f"Downloading {DATA_URL}")
urllib.request.urlretrieve(DATA_URL, TMP_PATH)
file_size_mb = os.path.getsize(TMP_PATH) / (1024 * 1024)
logger.info(f"Downloaded {file_size_mb:.1f} MB to {TMP_PATH}")

s3 = boto3.client("s3")
s3_key = f"{args.output_prefix}/{FILENAME}"
logger.info(f"Uploading to s3://{args.output_bucket}/{s3_key}")
s3.upload_file(TMP_PATH, args.output_bucket, s3_key)
logger.info(f"Done — s3://{args.output_bucket}/{s3_key}")
