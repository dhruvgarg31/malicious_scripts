import os
import random
import string
import json
import csv
import gzip
import shutil
import boto3
from faker import Faker
from concurrent.futures import ThreadPoolExecutor
import argparse
import logging
from tqdm import tqdm
import time

# Initialize Faker
faker = Faker()

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_text_data(size_mb):
    """Generate random text data."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size_mb * 1024 * 1024))

def generate_json_data(num_records):
    """Generate random JSON data."""
    return [faker.profile() for _ in range(num_records)]

def generate_csv_data(num_records):
    """Generate random CSV data."""
    header = ['name', 'address', 'email', 'phone_number', 'job']
    rows = [
        [faker.name(), faker.address(), faker.email(), faker.phone_number(), faker.job()]
        for _ in range(num_records)
    ]
    return header, rows

def write_file(file_path, data, file_format):
    """Write data to a file in the specified format."""
    if file_format == "text":
        with open(file_path, 'w') as file:
            file.write(data)
    elif file_format == "json":
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    elif file_format == "csv":
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data[0])  # Write header
            writer.writerows(data[1])  # Write rows

def compress_file(file_path):
    """Compress a file using gzip."""
    compressed_path = f"{file_path}.gz"
    with open(file_path, 'rb') as f_in, gzip.open(compressed_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(file_path)  # Remove original file
    return compressed_path

def upload_to_s3(file_path, bucket_name, s3_key):
    """Upload file to S3."""
    try:
        s3 = boto3.client('s3')
        s3.upload_file(file_path, bucket_name, s3_key)
        logging.info(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        logging.error(f"Failed to upload {file_path} to S3: {e}")

def retry_on_failure(func, max_retries=3, delay=2):
    """Retry a function on failure."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                logging.critical("Max retries reached. Skipping this task.")

def create_file(file_id, output_dir, file_format, size_mb, num_records, bucket_name=None):
    """Create a single file with the specified parameters."""
    file_name = f"test_file_{file_id}.{file_format}"
    file_path = os.path.join(output_dir, file_name)

    # Generate data based on format
    if file_format == "text":
        data = generate_text_data(size_mb)
    elif file_format == "json":
        data = generate_json_data(num_records)
    elif file_format == "csv":
        data = generate_csv_data(num_records)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")

    # Write file with retry logic
    retry_on_failure(lambda: write_file(file_path, data, file_format))

    # Compress file
    compressed_path = compress_file(file_path)

    # Upload to S3 if bucket is specified
    if bucket_name:
        s3_key = os.path.basename(compressed_path)
        retry_on_failure(lambda: upload_to_s3(compressed_path, bucket_name, s3_key))

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Generate test data for regression testing.")
    parser.add_argument("--output-dir", type=str, default="./test_data", help="Output directory for generated files.")
    parser.add_argument("--num-files", type=int, default=100, help="Number of files to generate.")
    parser.add_argument("--file-format", type=str, choices=["text", "json", "csv"], default="text", help="Format of the generated files.")
    parser.add_argument("--file-size-mb", type=int, default=1, help="Size of each file in MB (for text format).")
    parser.add_argument("--num-records", type=int, default=100, help="Number of records per file (for JSON/CSV formats).")
    parser.add_argument("--num-threads", type=int, default=5, help="Number of threads for parallel generation.")
    parser.add_argument("--bucket-name", type=str, help="S3 bucket name for uploading files.")
    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Use tqdm for progress tracking
    with ThreadPoolExecutor(max_workers=args.num_threads) as executor:
        for i in tqdm(range(args.num_files), desc="Generating files"):
            executor.submit(
                create_file,
                i,
                args.output_dir,
                args.file_format,
                args.file_size_mb,
                args.num_records,
                args.bucket_name
            )

    logging.info(f"Generated {args.num_files} files in {args.output_dir}.")

if __name__ == "__main__":
    main()
