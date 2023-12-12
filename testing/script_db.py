import mysql.connector
import json

# Connection to MySQL server (make sure the  MySQL server is running)
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # insert username
    password="",  # Insert password
    database="labint"
)

# Cursor creation
cursor = conn.cursor()

# Db creation
database_name = "labint"
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
print(f"Database '{database_name}' creato con successo.")

# Choosing the database
conn.database = database_name

# Creation of the capacity table 
table_creation_query_capacity = """
CREATE TABLE IF NOT EXISTS capacity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    posting_date DATE,
    entry_no INT,
    item_no INT,
    type VARCHAR(255),
    no VARCHAR(255),
    document_no VARCHAR(255),
    description VARCHAR(255),
    routing_no INT,
    routing_reference_no INT,
    operation_no INT,
    output_quantity INT,
    unit_of_measure_code VARCHAR(255),
    scrap_quantity INT,
    run_time INT,
    cap_unit_of_measure_code VARCHAR(255),
    order_type VARCHAR(255),
    order_line_no INT
)
"""

# Creation of the item table 
table_creation_query_item = """
CREATE TABLE IF NOT EXISTS item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_no INT,
    item_no INT,
    posting_date DATE,
    entry_type VARCHAR(255),
    source_no VARCHAR(255),
    document_no VARCHAR(255),
    quantity INT,
    unit_of_measure_code VARCHAR(255),
    document_line_no INT,
    order_type VARCHAR(255),
    order_no VARCHAR(255),
    order_line_no INT
)
"""

cursor.execute(table_creation_query_capacity)
cursor.execute(table_creation_query_item)



# Reading the Json file 
with open('testing/Capacity_Ledger_Entries.json', 'r', encoding='utf-8-sig') as json_file_capacity:
    data_capacity = json.load(json_file_capacity)

# Extract data from JSON and insert it into the 'capacity' table
for item in data_capacity.get("value", []):
    posting_date = item.get("posting_date", "")
    entry_no = item.get("entry_no", 0)
    item_no = item.get("item_no", "")
    type = item.get("type", "")
    no = item.get("no", "")
    document_no = item.get("document_no", "")
    description = item.get("description", "")
    routing_no = item.get("routing_no", "")
    routing_reference_no = item.get("routing_reference_no", 0)
    operation_no = item.get("operation_no", "")
    output_quantity = item.get("output_quantity", 0)
    unit_of_measure_code = item.get("unit_of_measure_code", "")
    scrap_quantity = item.get("scrap_quantity", 0)
    run_time = item.get("run_time", 0)
    cap_unit_of_measure_code = item.get("cap_unit_of_measure_code", "")
    order_type = item.get("order_type", "")
    order_line_no = item.get("order_line_no", 0)

    # Execute the insertion into the 'capacity' table
    cursor.execute('''
        INSERT INTO capacity (
            posting_date, entry_no, item_no, type,
            no, document_no, description, routing_no,
            routing_reference_no, operation_no, output_quantity,
            unit_of_measure_code, scrap_quantity, run_time,
            cap_unit_of_measure_code, order_type, order_line_no
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        posting_date, entry_no, item_no, type,
        no, document_no, description, routing_no,
        routing_reference_no, operation_no, output_quantity,
        unit_of_measure_code, scrap_quantity, run_time,
        cap_unit_of_measure_code, order_type, order_line_no
    ))

conn.commit()

# Reading the Json file 
with open('testing/Item_Ledger_Entries.json', 'r', encoding='utf-8-sig') as json_file_item:
    data_item = json.load(json_file_item)

# Extract data from JSON and insert it into the 'item' table
for item in data_item.get("value", []):
    entry_no = item.get("entry_no", 0)
    item_no = item.get("item_no", "")
    posting_date = item.get("posting_date", "")
    entry_type = item.get("entry_type", "")
    source_no = item.get("source_no", "")
    document_no = item.get("document_no", "")
    quantity = item.get("quantity", 0)
    unit_of_measure_code = item.get("unit_of_measure_code", "")
    document_line_no = item.get("document_line_no", 0)
    order_type = item.get("order_type", "")
    order_no = item.get("order_no", "")
    order_line_no = item.get("order_line_no", 0)

    # Execute the insertion into the 'item' table
    cursor.execute('''
        INSERT INTO item (entry_no, item_no, posting_date, entry_type,
            source_no, document_no, quantity, unit_of_measure_code,
            document_line_no, order_type, order_no, order_line_no
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        entry_no, item_no, posting_date, entry_type,
        source_no, document_no, quantity, unit_of_measure_code,
        document_line_no, order_type, order_no, order_line_no
    ))

conn.commit()

# Closing the connection
conn.close()

print("Script completed.")


"""
fallo su mysql
-- Abilita gli eventi se non sono già abilitati
SET GLOBAL event_scheduler = ON;

-- Crea un evento che si verifica ogni giorno alle 3:00 AM
CREATE EVENT my_event
  ON SCHEDULE
    EVERY 1 DAY
    STARTS (CURRENT_DATE + INTERVAL 3 HOUR) 
  DO
    -- La tua query da eseguire
    UPDATE tua_tabella SET tuo_campo = nuovo_valore WHERE tua_condizione;
    
[mysqld]
event_scheduler=ON

"""