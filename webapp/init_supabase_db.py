"""
Initialize Supabase Database with Tables
This script creates the necessary tables in your Supabase PostgreSQL database
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL not found in .env file")
    print("Please make sure your .env file has the DATABASE_URL set")
    exit(1)

print("[*] Initializing Supabase Database...")
print(f"[*] Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Supabase'}")
print()

try:
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Read and execute the SQL schema
    schema_file = os.path.join(os.path.dirname(__file__), 'supabase_schema.sql')

    if not os.path.exists(schema_file):
        print(f"[ERROR] Schema file not found: {schema_file}")
        exit(1)

    with open(schema_file, 'r', encoding='utf-8') as f:
        sql_commands = f.read()

    # Execute the SQL
    with engine.connect() as conn:
        # Split by semicolons and execute each statement
        statements = [s.strip() for s in sql_commands.split(';') if s.strip()]

        print("[*] Creating database schema...")
        for i, statement in enumerate(statements, 1):
            try:
                # Skip comments and empty statements
                if statement.startswith('--') or not statement:
                    continue

                conn.execute(text(statement))
                conn.commit()

                # Print progress every 5 statements
                if i % 5 == 0:
                    print(f"   [+] Executed {i}/{len(statements)} statements...")
            except Exception as e:
                # Some errors are okay (like "already exists")
                if "already exists" in str(e).lower():
                    continue
                else:
                    print(f"   [!] Warning on statement {i}: {str(e)[:100]}")
                    continue

        print()
        print("[SUCCESS] Database schema created successfully!")
        print()

        # Verify tables were created
        print("[*] Verifying tables...")
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """))

        tables = [row[0] for row in result]

        if tables:
            print("   Created tables:")
            for table in tables:
                print(f"   [+] {table}")
        else:
            print("   [!] No tables found")

        print()

        # Check if auth trigger was created
        print("[*] Verifying auth sync trigger...")
        trigger_result = conn.execute(text("""
            SELECT trigger_name
            FROM information_schema.triggers
            WHERE trigger_schema = 'public'
            AND event_object_table = 'users'
        """))

        triggers = [row[0] for row in trigger_result]
        if triggers:
            for trigger in triggers:
                print(f"   [+] {trigger}")

        print()
        print("=" * 60)
        print("[SUCCESS] Your Supabase database is ready!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Set up Google OAuth (see instructions below)")
        print("2. Run the Flask app: python app.py")
        print("3. Test authentication at http://localhost:5000/auth/login")
        print()

except Exception as e:
    print(f"[ERROR] {str(e)}")
    print()
    print("Troubleshooting:")
    print("1. Check your DATABASE_URL in .env file")
    print("2. Verify database password is correct")
    print("3. Ensure you can connect to Supabase from your network")
    print()
    exit(1)
