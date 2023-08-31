import psycopg2

# Establish a connection to the database
conn = psycopg2.connect(database="trans_manual", user="postgres", password="postgres", host="localhost", port="5432")

# Create a cursor object
cursor = conn.cursor()

# Set autocommit to False
conn.autocommit = False

try:
    # Insert a new customer
    sql_insert_customer = """INSERT INTO customer (name, email) VALUES ('John', 'john@example.com') RETURNING id"""
    cursor.execute(sql_insert_customer)
    customer_id = cursor.fetchone()[0]

    # Insert a new mutation
    sql_insert_mutation = """INSERT INTO account_mutation (customer_id, amount) VALUES (%s, %s)"""
    cursor.execute(sql_insert_mutation, (customer_id, 100))

    # Commit the transaction
    conn.commit()
    print("Transaction committed successfully")

except psycopg2.DatabaseError as error:
    # Rollback the transaction if any error occurs
    print("Failed to update records to database rollback: {}".format(error))
    conn.rollback()

finally:
    # Close the cursor object and PostgreSQL database connection
    if conn is not None:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

# Dibawah ini adalah syntax untuk membuat tabel "customer" dan "account_mutation" di database postgres

# CREATE TABLE customer (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     email VARCHAR(255) NOT NULL
# );

# CREATE TABLE account_mutation (
#     id SERIAL PRIMARY KEY,
#     customer_id INTEGER NOT NULL,
#     amount NUMERIC(10, 2) NOT NULL,
#     FOREIGN KEY (customer_id) REFERENCES customer (id)
# );

