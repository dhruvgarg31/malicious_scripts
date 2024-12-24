# Cassandra Data Generation Script

This Python script is designed to generate fake data and insert it into a Cassandra database. It takes a configuration file (config.json) that specifies the number of entries, table details, column names, and data types, and then generates random data based on the provided schema. The script also supports batch insertion, logging, export to CSV or JSON, and error handling with retries.

## Features
- Dynamic Data Generation: Generate fake data based on various column types including string, int, float, timestamp, boolean, uuid, and custom (for custom functions).
- Batch Insertions: Insert data in batches for better performance with Cassandra.
- Progress Tracking: Displays a progress bar for data insertion and logs each step.
- Column Validation: Validates column types in the configuration file to ensure they are supported by Cassandra.
- Custom Data Functions: Generate data using custom functions, like generating random email addresses or dates.
- Multiple Keyspace Support: Connect to multiple Cassandra clusters or keyspaces.
- Error Handling and Retries: Automatically retries connection and insertion in case of failures.
- Export Data: Export generated data to JSON or CSV files before insertion into the database.

## Requirements
Install the required Python libraries:

- **Python 3.x**
- **Cassandra 3.x** or higher
- **Python dependencies**: `cassandra-driver`, `faker`, `tqdm `
    
    ```bash
    pip install -r requirements.txt

You can install the required libraries using pip:
    ```bash
    pip install cassandra-driver faker tqdm

## Configuration File (config.json)





