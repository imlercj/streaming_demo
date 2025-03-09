import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection parameters from docker-compose.yml
CONNECTION = 'host=postgres port=5432 dbname=mydb user=user password=password'

def count_table_rows():
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(CONNECTION)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get all tables including continuous aggregates
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        """)
        
        tables = cur.fetchall()
        
        print("\nTable Row Counts:")
        print("-----------------")
        
        for table in tables:
            table_name = table['table_name']
            try:
                cur.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                result = cur.fetchone()
                count = result['count']
                print(f"{table_name}: {count:,} rows")
            except Exception as e:
                print(f"{table_name}: Error counting rows - {str(e)}")
        
    except Exception as e:
        print(f"Database connection error: {str(e)}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    count_table_rows()
