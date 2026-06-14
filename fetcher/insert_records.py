import psycopg2
from fetcher.api_client import fetch_data

def connect_to_db():
    print("Connecting to the database....")
    try:
        conn = psycopg2.connect(
            host="db",
            user="db_user",
            password="db_password",
            database="weather",
            port="5432"
        )
        print("Database connected successfully.")
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")

def create_table(conn):
    print("Creating table 'weather' if it doesn't exist...")
    cursor=None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_description TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
        """)
        conn.commit()
        print("Table 'raw_weather_data' created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()

def insert_data(conn, data):
    print("Inserting data into 'raw_weather_data' table...")
    cursor=None
    try:
        weather= data['current']
        location= data['location']
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dev.raw_weather_data (
                city,
                temperature,
                weather_description,
                wind_speed,
                time,
                inserted_at,
                utc_offset
            )
            VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        """, (
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            location['localtime'],
            location['utc_offset']
        ))
        conn.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if cursor:
            cursor.close()


def main():
    conn=None
    try:
        data=fetch_data()
        conn=connect_to_db()
        create_table(conn)
        insert_data(conn, data)
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()