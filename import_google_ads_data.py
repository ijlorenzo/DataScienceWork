#!/usr/bin/env python3
"""
Helper script to import Google Ads CSV exports into local database
"""

import sys
import sqlite3
from pathlib import Path
import pandas as pd


DB_PATH = Path(__file__).parent / "google_ads_data.db"


def import_csv_to_db(csv_path: str, table_name: str, column_mapping: dict = None):
    """Import CSV file to SQLite database"""

    print(f"\nImporting {csv_path} to {table_name} table...")

    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"  Loaded {len(df)} rows from CSV")
    print(f"  Columns found: {list(df.columns)}")

    # Apply column mapping if provided
    if column_mapping:
        df = df.rename(columns=column_mapping)
        print(f"  Mapped columns: {list(df.columns)}")

    # Clean column names
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('.', '').str.replace('(', '').str.replace(')', '')

    # Connect to database
    conn = sqlite3.connect(DB_PATH)

    # Import data
    df.to_sql(table_name, conn, if_exists='append', index=False)

    conn.close()

    print(f"  ✓ Successfully imported {len(df)} rows")


def show_stats():
    """Show database statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n" + "=" * 70)
    print("Database Statistics")
    print("=" * 70)

    tables = ['campaigns', 'ad_groups', 'keywords', 'search_terms', 'account_summary']

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute(f"SELECT MIN(date), MAX(date) FROM {table}")
            date_range = cursor.fetchone()
            print(f"\n{table.upper()}:")
            print(f"  Rows: {count:,}")
            print(f"  Date Range: {date_range[0]} to {date_range[1]}")
        else:
            print(f"\n{table.upper()}: No data")

    conn.close()
    print("\n" + "=" * 70)


def main():
    """Main import function"""

    print("=" * 70)
    print("Google Ads Data Import Utility")
    print("=" * 70)
    print()
    print("This script helps you import Google Ads CSV exports into the local database.")
    print()

    # Check if database exists
    if not DB_PATH.exists():
        print("Database not found. Creating new database...")
        from google_ads_local_mcp_server import init_database
        init_database()
        print("✓ Database initialized")

    # Interactive import
    print("\nWhat type of data do you want to import?")
    print()
    print("1. Campaign Performance Report")
    print("2. Ad Group Performance Report")
    print("3. Keyword Performance Report")
    print("4. Search Terms Report")
    print("5. Account Summary Report")
    print("6. Show database statistics")
    print("7. Exit")
    print()

    choice = input("Enter choice (1-7): ").strip()

    if choice == "1":
        csv_path = input("Enter path to campaign CSV file: ").strip()
        column_mapping = {
            'Campaign': 'name',
            'Campaign ID': 'id',
            'Campaign status': 'status',
            'Campaign type': 'type',
            'Budget': 'budget',
            'Day': 'date',
            'Impressions': 'impressions',
            'Clicks': 'clicks',
            'Cost': 'cost',
            'Conversions': 'conversions',
            'CTR': 'ctr',
            'Avg. CPC': 'avg_cpc',
            'Conv. value': 'conversion_value'
        }
        import_csv_to_db(csv_path, 'campaigns', column_mapping)

    elif choice == "2":
        csv_path = input("Enter path to ad group CSV file: ").strip()
        column_mapping = {
            'Ad group': 'name',
            'Ad group ID': 'id',
            'Campaign': 'campaign_name',
            'Campaign ID': 'campaign_id',
            'Ad group status': 'status',
            'Day': 'date',
            'Impressions': 'impressions',
            'Clicks': 'clicks',
            'Cost': 'cost',
            'Conversions': 'conversions',
            'CTR': 'ctr'
        }
        import_csv_to_db(csv_path, 'ad_groups', column_mapping)

    elif choice == "3":
        csv_path = input("Enter path to keyword CSV file: ").strip()
        column_mapping = {
            'Keyword': 'keyword_text',
            'Match type': 'match_type',
            'Ad group': 'ad_group_name',
            'Campaign': 'campaign_name',
            'Keyword status': 'status',
            'Day': 'date',
            'Impressions': 'impressions',
            'Clicks': 'clicks',
            'Cost': 'cost',
            'Conversions': 'conversions',
            'CTR': 'ctr',
            'Avg. CPC': 'avg_cpc',
            'Quality score': 'quality_score'
        }
        import_csv_to_db(csv_path, 'keywords', column_mapping)

    elif choice == "4":
        csv_path = input("Enter path to search terms CSV file: ").strip()
        column_mapping = {
            'Search term': 'search_term',
            'Search term match type': 'status',
            'Match type': 'match_type',
            'Keyword': 'keyword_text',
            'Campaign': 'campaign_name',
            'Ad group': 'ad_group_name',
            'Day': 'date',
            'Impressions': 'impressions',
            'Clicks': 'clicks',
            'Cost': 'cost',
            'Conversions': 'conversions',
            'CTR': 'ctr'
        }
        import_csv_to_db(csv_path, 'search_terms', column_mapping)

    elif choice == "5":
        csv_path = input("Enter path to account summary CSV file: ").strip()
        column_mapping = {
            'Account': 'account_name',
            'Customer ID': 'account_id',
            'Currency code': 'currency',
            'Time zone': 'timezone',
            'Day': 'date',
            'Impressions': 'impressions',
            'Clicks': 'clicks',
            'Cost': 'cost',
            'Conversions': 'conversions'
        }
        import_csv_to_db(csv_path, 'account_summary', column_mapping)

    elif choice == "6":
        show_stats()
        return

    elif choice == "7":
        print("\nGoodbye!")
        return

    else:
        print("\nInvalid choice. Please try again.")
        return

    # Show stats after import
    show_stats()

    # Ask if user wants to import more
    again = input("\nImport more data? (y/n): ").strip().lower()
    if again == 'y':
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nImport cancelled by user.")
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"\n\n❌ File not found: {e}")
        print("Please check the file path and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        sys.exit(1)
