# Generate Data Script

This script is designed to generate large amounts of test data for **regression testing** in various formats, including **text**, **JSON**, and **CSV**. The user can specify the format, size, number of records, and more, while the script supports **multi-threading** for efficient file generation.

---

## Features

- **Multiple Data Formats**: Generate random **text**, **JSON**, and **CSV** files.
- **Customizable File Size and Record Count**: Control file size (for text) and number of records (for JSON/CSV).
- **Multi-Threaded Execution**: Speed up data generation with concurrent threads.
- **Logging**: Detailed logging for easy debugging and progress tracking.
- **Flexible Command-Line Arguments**: Easily configure the script using CLI options.

---

## Requirements

- **Python 3.x**
- Install the required `faker` library:
  
  ```bash
  pip install faker

## Command-Line Arguments

You can configure the script by passing the following command-line arguments:

- `--output-dir` (optional):  
  Path to the output directory where the generated files will be stored. Default is `./test_data`.

  **Example:**
  ```bash
  --output-dir ./generated_data

- `--num-files` (required):
  The number of files to generate. Default is 100.

  **Example:**
  ```bash
  --num-files 200

- `--file-format` (required):
  The format of the files to generate. Choose from:
  - **text:** Plain text files with random alphanumeric data.
  - **json:** JSON files with random structured profiles.
  - **csv:** CSV files with tabular data.
  
  **Example:**
  ```bash
  --file-format json

- `--file-size-mb` (optional):  
  The size of each text file in MB (only applicable for text format). The default is **1 MB**.

  **Example:**
  ```bash
  --file-size-mb 50

- `--num-records` (optional):  
  The number of records per file for JSON or CSV formats. The default is **100**.
  
  **Example:**
  ```bash
  --num-records 500

- `--num-threads` (optional):  
  The number of threads to use for concurrent generation. The default is **5**.
   
  **Example:**
  ```bash
  --num-threads 10

## Usage

To run the script, execute the following command:

```bash
python enhanced_data_generator.py --output-dir <path_to_output_directory> --num-files <number_of_files> --file-format <file_format> --file-size-mb <file_size_in_MB> --num-records <number_of_records> --num-threads <number_of_threads>
