import json
import random
import time
import logging
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, BatchStatement
from faker import Faker
from tqdm import tqdm

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Custom data generation functions
def generate_email():
    fake = Faker()
    return fake.email()

def generate_date():
    fake = Faker()
    return fake.date_this_decade()

custom_functions = {
    "generate_email": generate_email,
    "generate_date": generate_date
}

# Connect to Cassandra with retry mechanism
def connect_to_cassandra(ip, port, username, password, keyspace, retries=3):
    cluster = Cluster([ip], port=port)
    session = cluster.connect()
    session.set_keyspace(keyspace)
    for attempt in range(retries):
        try:
            session.execute('SELECT now() FROM system.local')  # Simple query to check connection
            logger.info(f"Connected to Cassandra at {ip}:{port}, keyspace: {keyspace}")
            return session
        except Exception as e:
            if attempt < retries - 1:
                logger.warning(f"Connection failed, retrying... ({attempt + 1}/{retries})")
                time.sleep(5)
                continue
            else:
                raise e

# Validate the column types
def validate_columns(columns):
    valid_types = ['string', 'int', 'timestamp', 'float', 'boolean', 'uuid', 'custom']
    for col_name, col_info in columns.items():
        if col_info['type'] not in valid_types:
            raise ValueError(f"Invalid column type: {col_info['type']} for column {col_name}")

# Generate fake data based on column types
def generate_fake_data(columns, number_of_entries):
    fake = Faker()
    data = []
    for _ in range(number_of_entries):
        row = {}
        for col_name, col_info in columns.items():
            if col_info['type'] == 'custom':
                row[col_name] = custom_functions[col_info['function']]()
            elif col_info['type'] == 'string':
                row[col_name] = fake.word()
            elif col_info['type'] == 'int':
                row[col_name] = random.randint(1, 1000)
            elif col_info['type'] == 'float':
                row[col_name] = round(random.uniform(1.0, 1000.0), 2)
            elif col_info['type'] == 'boolean':
                row[col_name] = random.choice([True, False])
            elif col_info['type'] == 'timestamp':
                row[col_name] = fake.date_this_decade()
            elif col_info['type'] == 'uuid':
                row[col_name] = fake.uuid4()
        data.append(row)
    return data

# Batch insert data into Cassandra
def batch_insert(session, table_name, data, batch_size=50):
    batch = BatchStatement()
    for i, row in enumerate(data):
        columns = ', '.join(row.keys())
        placeholders = ', '.join(['%s'] * len(row))
        values = tuple(row.values())
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        batch.add(SimpleStatement(insert_query), values)
        if (i + 1) % batch_size == 0:
            session.execute(batch)
            batch.clear()
    if batch:
        session.execute(batch)

# Export generated data to JSON or CSV
def export_data(data, format='json', filename='generated_data'):
    if format == 'json':
        with open(f'{filename}.json', 'w') as file:
            json.dump(data, file, indent=4)
        logger.info(f"Data exported to {filename}.json")
    elif format == 'csv':
        import csv
        keys = data[0].keys()
        with open(f'{filename}.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"Data exported to {filename}.csv")

# Insert data into Cassandra with logging and progress bar
def insert_data(session, table_name, data):
    logger.info(f"Starting data insertion into {table_name}")
    for row in tqdm(data, desc=f"Inserting into {table_name}", unit="row"):
        columns = ', '.join(row.keys())
        placeholders = ', '.join(['%s'] * len(row))
        values = tuple(row.values())
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        session.execute(SimpleStatement(insert_query), values)
    logger.info(f"Data insertion into {table_name} completed")

# Main function to orchestrate the process
def main(config_file='config.json'):
    # Load configuration from the config file
    with open(config_file, 'r') as file:
        config = json.load(file)

    cassandra_config = config['cassandra'][0]
    ip = cassandra_config['ip']
    port = cassandra_config['port']
    username = cassandra_config['username']
    password = cassandra_config['password']
    keyspace = cassandra_config['keyspace']

    number_of_entries = config['number_of_entries']
    tables = config['tables']

    # Connect to Cassandra
    session = connect_to_cassandra(ip, port, username, password, keyspace)

    # Process each table
    for table in tables:
        table_name = table['name']
        columns = table['columns']

        # Validate columns
        validate_columns(columns)

        # Generate fake data
        data = generate_fake_data(columns, number_of_entries)

        # Export generated data (optional)
        export_data(data, format='json', filename=table_name)

        # Insert data into Cassandra
        batch_insert(session, table_name, data)

if __name__ == '__main__':
    main()
