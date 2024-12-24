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

- To run the script, execute the following command:

    ```bash
    python enhanced_data_generator.py --output-dir <path_to_output_directory> --num-files <number_of_files> --file-format <file_format> --file-size-mb <file_size_in_MB> --num-records <number_of_records> --num-threads <number_of_threads>

## Example Commands

- **Generate 100 JSON files, each containing 500 records:**
  
  ```bash
  python enhanced_data_generator.py --file-format json --num-files 100 --num-records 500

- **Generate 50 CSV files and store them in a custom directory:**
  
  ```bash
  python enhanced_data_generator.py --file-format csv --num-files 50 --output-dir ./custom_dir

- **Generate 10 text files, each 50 MB in size:**
  
  ```bash
  python enhanced_data_generator.py --file-format text --num-files 10 --file-size-mb 50

- **Generate 200 text files, each 1 MB in size, using 10 threads:**
  
  ```bash
  python enhanced_data_generator.py --file-format text --num-files 200 --file-size-mb 1 --num-threads 10

## File Format Details

### Text Format

- **File Contents**:  
  The text format generates random alphanumeric text data. The size of each file is controlled by the `--file-size-mb` argument.

  **Example**:
  ```txt
  5h9W6aB0D5
  T7wG1X8K9z
  eL1vF6M3uP

### JSON Format

- **File Contents**:  
  The JSON format generates random structured data in the form of fake user profiles. The number of records is controlled by the `--num-records` argument.

  **Example JSON data**:
  ```json
  [
    {
      "name": "John Doe",
      "address": "123 Fake St, Faketown, FT 12345",
      "email": "johndoe@example.com",
      "phone_number": "+1234567890",
      "job": "Software Developer"
    },
  ]

### CSV Format

- **File Contents**:  
  The CSV format generates rows of tabular data with columns like `name`, `address`, `email`, `phone_number`, and `job`. The number of records is controlled by the `--num-records` argument.

  **Example CSV data**:
  ```csv
  name,address,email,phone_number,job
  John Doe,123 Fake St,johndoe@example.com,+1234567890,Software Developer
  Jane Smith,456 Real Ave,jane.smith@example.com,+1234567891,Data Analyst
  ...

## Logging

The script provides detailed logging to help track the file generation process and troubleshoot any issues.

### Log Levels

- **INFO**:  
  Displays progress information such as the creation of files and the number of records.

  **Example**:
    ```bash
    INFO - Writing data to ./test_data/test_file_0.txt in text format.
    INFO - File ./test_data/test_file_0.txt created.
    ```

- **DEBUG**:  
  Provides more detailed information about the data generation process, including the random data being generated.

  **Example**:
    ```bash
    DEBUG - Generating random text data for test_file_0.txt
    DEBUG - Writing text data to ./test_data/test_file_0.txt
    ```

- **ERROR**:  
  Logs any errors that occur during execution, such as file write failures or unsupported format issues.

## Performance Considerations

- **Multi-Threading**:  
  Use the `--num-threads` option to enable multi-threaded file generation, which speeds up the process when generating large datasets.

- **File Size**:  
  Adjust the `--file-size-mb` and `--num-records` options to meet your testing needs. Keep in mind that generating large files requires sufficient disk space.

  **Example YAML Configuration**:
  ```yaml
  ---
  num-threads: 10
  file-size-mb: 50
  num-records: 500

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/dhruvgarg31/malicious_scripts/blob/master/Python_data_generator/LICENSE) file for details.


