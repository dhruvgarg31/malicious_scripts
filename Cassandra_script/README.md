# Cassandra Data Generation Script

This Python script is designed to generate fake data and insert it into a Cassandra database. It takes a configuration file `(config.json)` that specifies the number of entries, table details, column names, and data types, and then generates random data based on the provided schema. The script also supports batch insertion, logging, export to CSV or JSON, and error handling with retries.

## Features
- **Dynamic Data Generation:** Generate fake data based on various column types including `string`, `int`, `float`, `timestamp`, `boolean`, `uuid`, and `custom` (for custom functions).
- **Batch Insertions:** Insert data in batches for better performance with Cassandra.
- **Progress Tracking:** Displays a progress bar for data insertion and logs each step.
- **Column Validation:** Validates column types in the configuration file to ensure they are supported by Cassandra.
- **Custom Data Functions:** Generate data using custom functions, like generating random email addresses or dates.
- **Multiple Keyspace Support:** Connect to multiple Cassandra clusters or keyspaces.
- **Error Handling and Retries:** Automatically retries connection and insertion in case of failures.
- **Export Data:** Export generated data to JSON or CSV files before insertion into the database.

## Requirements
Install the required Python libraries:

- **Python 3.x**
- **Cassandra 3.x** or higher
- **Python dependencies**: `cassandra-driver`, `faker`, `tqdm `
    
    ```bash
    pip install -r requirements.txt

- You can install the required libraries using pip:
    ```bash
    pip install cassandra-driver faker tqdm

## Configuration File (config.json)
- The `config.json` file is used to specify the Cassandra connection details, table definitions, and column data types. Here's an example:
    ```json
    {
        "cassandra": [
            {
                "ip": "127.0.0.1",
                "port": 9042,
                "username": "cassandra",
                "password": "cassandra",
                "keyspace": "your_keyspace"
            }
        ],
        "number_of_entries": 10,
        "tables": [
            {
                "name": "event",
                "columns": {
                    "event_name": {"type": "string"},
                    "event_id": {"type": "int", "min": 1, "max": 1000},
                    "event_type": {"type": "string"},
                    "event_date": {"type": "timestamp"},
                    "location": {"type": "string"},
                    "organizer": {"type": "string"},
                    "duration": {"type": "int", "min": 30, "max": 300},
                    "attendees": {"type": "int", "min": 10, "max": 1000},
                    "event_description": {"type": "string"},
                    "ticket_price": {"type": "float", "min": 10, "max": 500}
                }
            }
        ]
    }

## Configuration Fields:
- **cassandra:** List of Cassandra cluster details. Each cluster should have the following fields:
    - `ip:` The IP address of the Cassandra node.
    - `port:` The port on which Cassandra is running (default is 9042).
    - `username:` The username for Cassandra authentication.
    - `password:` The password for Cassandra authentication.
    - `keyspace:` The keyspace in which data will be inserted.
- **number_of_entries:** The number of rows to be generated for each table.
- **tables:** A list of tables to generate data for. Each table should have:
    - `name:` The name of the table.
    - `columns:` A dictionary of column names and their corresponding data types.

## Column Types:
- **string:** Generates a random string.
- **int:** Generates a random integer within the specified range (`min` and `max`).
- **float:** Generates a random float within the specified range (`min` and `max`).
- **boolean:** Generates a random boolean (`True` or `False`).
- **timestamp:** Generates a random date or timestamp.
- **uuid:** Generates a random UUID.
- **custom:** Uses a custom function to generate the data. Example: `generate_email` or `generate_date`.

## Usage
### Step 1: Set up the configuration file
Modify the `config.json` file to specify your Cassandra connection details, the number of entries, and the table schema with column data types.

### Step 2: Run the script
- Run the `generate_cassandra_data.py` script:

    ``` bash
    python generate_cassandra_data.py

### Step 3: Monitor the process
- The script will log each step and show a progress bar while inserting data into Cassandra.
- If any errors occur (e.g., connection issues), the script will retry the operation up to 3 times by default.

### Step 4: Export Data (Optional)
The script will automatically export the generated data into a `JSON` or `CSV` file before inserting it into the database. You can specify the format (either json or csv) in the configuration or modify the script for custom export logic.

## Error Handling and Retries
The script includes error handling and a retry mechanism:
- If the connection to Cassandra fails, it will retry the connection up to 3 times.
- If an insertion fails, it will retry the insertion process for up to 3 attempts.

## Example Output
- After running the script, you should see logs similar to the following:
    ```vbnet
    INFO:root:Connected to Cassandra at 127.0.0.1:9042, keyspace: your_keyspace
    INFO:root:Starting data insertion into event
    100%|██████████| 10/10 [00:02<00:00, 4.25row/s]
    INFO:root:Data insertion into event completed
    INFO:root:Data exported to event.json

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/dhruvgarg31/malicious_scripts/blob/master/Cassandra_script/LICENSE) file for details.
