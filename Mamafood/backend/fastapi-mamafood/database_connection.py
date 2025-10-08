import pymysql

def connect_to_db():
    try:
        # Attempt to connect to the database with the correct password
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='mamafood',  # Make sure this is correct
            database='mamafood'
        )
        print("Connection successful!")
        # Perform database operations here if needed

    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("Connection closed.")

connect_to_db()
