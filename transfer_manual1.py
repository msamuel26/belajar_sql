import psycopg2

conn = psycopg2.connect(database="transfer_manually", user="postgres", password="postgres", host="localhost", port="5432")

cursor = conn.cursor()

conn.autocommit = False

try:
    cursor.execute("BEGIN")

    sql_insert_users = """INSERT INTO users (name, balance) values (%s, %s) RETURNING id"""
    users_values = ("Bapak", 1000)
    cursor.execute(sql_insert_users, users_values)
    user1_id = cursor.fetchone()[0]

    users_values1 = ("Adek", 1000)
    cursor.execute(sql_insert_users, users_values1)
    user2_id = cursor.fetchone()[0]

    update_users = """UPDATE users set balance = balance - (%s) where id = (%s)"""
    users_values2 = (1100, user1_id)
    cursor.execute(update_users, (1100, user1_id))

    update_users1 = """UPDATE users set balance = balance + (%s) where id = (%s)"""
    cursor.execute(update_users1, (1100, user2_id))

    select_bapak = """SELECT balance from users where id = (%s)"""
    cursor.execute(select_bapak, (user1_id,))
    result = cursor.fetchone()
    balance = result[0]
    if balance < 0:
        raise ValueError("SALDO NEGATIF")

    cursor.execute("COMMIT")
    print("Transaction committed successfully")

except psycopg2.DatabaseError as error:
    print("Failed to update records to database rollback {}".format(error))
    cursor.execute("ROLLBACK")

finally:
    if conn is not None:
        conn.close()
        cursor.close()
        print("PostgreSQL connection is closed")