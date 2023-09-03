import psycopg2

# Establish a connection to the database
conn = psycopg2.connect(database="trans_manual", user="postgres", password="postgres", host="localhost", port="5432")

# Create a cursor object
cursor = conn.cursor()

# Set autocommit to False
conn.autocommit = False # bertujuan agar setiap eksekusi SQL tidak langsung disimpan di database

try:
    # Start the database transaction
    cursor.execute("BEGIN") 

    # Insert a new customer
    sql_insert_customer = """INSERT INTO customer (name, email) VALUES (%s, %s) RETURNING id"""
    customer_values = ('John', 'john@example.com')
    cursor.execute(sql_insert_customer, customer_values)
    customer_id = cursor.fetchone()[0] # untuk mengambil nilai RETURNING id

    # Insert a new mutation for the customer with id 1
    sql_insert_mutation = """INSERT INTO account_mutation (customer_id, amount) VALUES (%s, %s)"""
    mutation_values = (1, 100)
    cursor.execute(sql_insert_mutation, mutation_values)

    # Commit the transaction
    cursor.execute("COMMIT")
    print("Transaction committed successfully")

except psycopg2.DatabaseError as error:
    # Rollback the transaction if any error occurs
    print("Failed to update records to database rollback: {}".format(error))
    cursor.execute("ROLLBACK")

finally:
    # Close the cursor object and PostgreSQL database connection
    if conn is not None:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

# CREATE TABLE customer (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     email VARCHAR(255) NOT NULL
# );

# CREATE TABLE account_mutation (
#     id SERIAL PRIMARY KEY,
#     customer_id INTEGER NOT NULL,
#     amount NUMERIC(10, 2) NOT NULL,
#     FOREIGN KEY (customer_id) REFERENCES customer (id) -- > ini berarti nilai pada kolom "customer_id" pada tabel "account_mutation" mereferensi ke tabel "customer" dengan kolom "id", jika nilai customer_id di tabel "account_mutation" yang akan di-insert atau update tidak ada di tabel "customer" kolom "id", 
#                                                                 maka database akan me-raise Exception atau error:
#                                                                   Failed to update records to database rollback: insert or update on table "account_mutation" violates foreign key constraint "account_mutation_customer_id_fkey"
#                                                                       DETAIL:  Key (customer_id)=(1) is not present in table "customer".
# );


