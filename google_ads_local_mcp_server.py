#!/usr/bin/env python3
"""
Google Ads LOCAL MCP Server
Provides natural language querying capabilities for locally stored Google Ads data
NO CLOUD API CALLS - 100% LOCAL
"""

import os
import json
import sqlite3
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
import pandas as pd

# Initialize MCP server
app = Server("google-ads-local-mcp")

# Database path
DB_PATH = Path(__file__).parent / "google_ads_data.db"


def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the local SQLite database with schema"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Campaigns table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT,
            type TEXT,
            budget REAL,
            date TEXT,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            cost REAL DEFAULT 0,
            conversions REAL DEFAULT 0,
            ctr REAL DEFAULT 0,
            avg_cpc REAL DEFAULT 0,
            conversion_value REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Ad Groups table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ad_groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            campaign_id INTEGER,
            campaign_name TEXT,
            status TEXT,
            date TEXT,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            cost REAL DEFAULT 0,
            conversions REAL DEFAULT 0,
            ctr REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    """)

    # Keywords table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_text TEXT NOT NULL,
            match_type TEXT,
            ad_group_name TEXT,
            campaign_name TEXT,
            status TEXT,
            date TEXT,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            cost REAL DEFAULT 0,
            conversions REAL DEFAULT 0,
            ctr REAL DEFAULT 0,
            avg_cpc REAL DEFAULT 0,
            quality_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Search Terms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_term TEXT NOT NULL,
            status TEXT,
            match_type TEXT,
            keyword_text TEXT,
            campaign_name TEXT,
            ad_group_name TEXT,
            date TEXT,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            cost REAL DEFAULT 0,
            conversions REAL DEFAULT 0,
            ctr REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Account summary table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT,
            account_id TEXT,
            currency TEXT,
            timezone TEXT,
            date TEXT,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            cost REAL DEFAULT 0,
            conversions REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def execute_local_query(query: str) -> List[Dict[str, Any]]:
    """Execute SQL query on local database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        results = []

        for row in cursor.fetchall():
            result_dict = {}
            for i, col in enumerate(columns):
                result_dict[col] = row[i]
            results.append(result_dict)

        return results
    except Exception as e:
        raise Exception(f"Query execution failed: {str(e)}")
    finally:
        conn.close()


def natural_language_to_sql(natural_query: str) -> str:
    """Convert natural language query to SQL"""
    query = natural_query.lower().strip()

    # Define common query patterns
    patterns = {
        "campaign performance": """
            SELECT
                name,
                status,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(cost) as total_cost,
                SUM(conversions) as total_conversions,
                AVG(ctr) as avg_ctr,
                AVG(avg_cpc) as avg_cpc
            FROM campaigns
            WHERE date >= date('now', '-30 days')
            GROUP BY name, status
            ORDER BY total_impressions DESC
        """,

        "ad group performance": """
            SELECT
                name,
                campaign_name,
                status,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(cost) as total_cost,
                SUM(conversions) as total_conversions,
                AVG(ctr) as avg_ctr
            FROM ad_groups
            WHERE date >= date('now', '-30 days')
            GROUP BY name, campaign_name, status
            ORDER BY total_impressions DESC
        """,

        "keyword performance": """
            SELECT
                keyword_text,
                match_type,
                campaign_name,
                ad_group_name,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(cost) as total_cost,
                SUM(conversions) as total_conversions,
                AVG(ctr) as avg_ctr,
                AVG(avg_cpc) as avg_cpc,
                AVG(quality_score) as avg_quality_score
            FROM keywords
            WHERE date >= date('now', '-30 days')
            GROUP BY keyword_text, match_type, campaign_name, ad_group_name
            ORDER BY total_impressions DESC
            LIMIT 100
        """,

        "search terms": """
            SELECT
                search_term,
                status,
                keyword_text,
                campaign_name,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(cost) as total_cost,
                SUM(conversions) as total_conversions,
                AVG(ctr) as avg_ctr
            FROM search_terms
            WHERE date >= date('now', '-30 days')
            GROUP BY search_term, status, keyword_text, campaign_name
            ORDER BY total_impressions DESC
            LIMIT 100
        """,

        "account overview": """
            SELECT
                account_name,
                account_id,
                currency,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(cost) as total_cost,
                SUM(conversions) as total_conversions
            FROM account_summary
            WHERE date >= date('now', '-30 days')
            GROUP BY account_name, account_id, currency
        """,

        "top performing campaigns": """
            SELECT
                name,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(cost) as total_cost,
                SUM(conversions) as total_conversions,
                AVG(ctr) as avg_ctr,
                SUM(conversion_value) as total_conversion_value
            FROM campaigns
            WHERE date >= date('now', '-30 days')
            AND status = 'ENABLED'
            GROUP BY name
            ORDER BY total_conversions DESC
            LIMIT 10
        """,

        "daily performance": """
            SELECT
                date,
                SUM(impressions) as impressions,
                SUM(clicks) as clicks,
                SUM(cost) as cost,
                SUM(conversions) as conversions,
                AVG(ctr) as ctr
            FROM campaigns
            WHERE date >= date('now', '-30 days')
            GROUP BY date
            ORDER BY date DESC
        """,

        "campaign summary": """
            SELECT
                COUNT(DISTINCT name) as total_campaigns,
                SUM(CASE WHEN status = 'ENABLED' THEN 1 ELSE 0 END) as active_campaigns,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(cost) as total_cost,
                SUM(conversions) as total_conversions
            FROM campaigns
            WHERE date >= date('now', '-30 days')
        """
    }

    # Match query to pattern
    for pattern_key, sql_query in patterns.items():
        if pattern_key in query:
            return sql_query.strip()

    # If no pattern matches, assume it's already SQL
    return natural_query


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for local Google Ads querying"""
    return [
        Tool(
            name="query_local_ads_data",
            description="""Query locally stored Google Ads data using natural language or SQL.

            This is a 100% LOCAL tool - no cloud API calls!

            Supported natural language queries:
            - "campaign performance" - Get performance metrics for all campaigns
            - "ad group performance" - Get performance metrics for all ad groups
            - "keyword performance" - Get performance metrics for keywords
            - "search terms" - Get search term performance data
            - "account overview" - Get overall account metrics
            - "top performing campaigns" - Get best performing campaigns
            - "daily performance" - Get day-by-day performance trends
            - "campaign summary" - Get summary statistics

            You can also provide custom SQL queries directly.

            Example queries:
            - "Show me campaign performance"
            - "What are my top performing keywords?"
            - "SELECT * FROM campaigns WHERE cost > 100 ORDER BY conversions DESC"
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query or SQL query string"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="import_csv_data",
            description="""Import Google Ads data from CSV files.

            Supports importing:
            - Campaign reports
            - Ad group reports
            - Keyword reports
            - Search term reports
            - Account summary reports

            The CSV should be exported from Google Ads UI.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "csv_path": {
                        "type": "string",
                        "description": "Path to the CSV file to import"
                    },
                    "data_type": {
                        "type": "string",
                        "description": "Type of data being imported",
                        "enum": ["campaigns", "ad_groups", "keywords", "search_terms", "account_summary"]
                    }
                },
                "required": ["csv_path", "data_type"]
            }
        ),
        Tool(
            name="get_database_stats",
            description="Get statistics about the local database (row counts, date ranges, etc.)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="clear_database",
            description="Clear all data from the local database (use with caution!)",
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be set to true to confirm deletion"
                    }
                },
                "required": ["confirm"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    # Initialize database if it doesn't exist
    if not DB_PATH.exists():
        init_database()

    try:
        if name == "query_local_ads_data":
            query_input = arguments.get("query", "")

            # Convert natural language to SQL if needed
            if not query_input.strip().upper().startswith("SELECT"):
                sql_query = natural_language_to_sql(query_input)
            else:
                sql_query = query_input

            results = execute_local_query(sql_query)

            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "query": sql_query,
                        "results": results,
                        "count": len(results)
                    }, indent=2, default=str)
                )
            ]

        elif name == "import_csv_data":
            csv_path = arguments.get("csv_path")
            data_type = arguments.get("data_type")

            # Read CSV
            df = pd.read_csv(csv_path)

            # Import to database
            conn = get_db_connection()

            # Clean column names (lowercase, replace spaces with underscores)
            df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('.', '')

            # Import based on type
            df.to_sql(data_type, conn, if_exists='append', index=False)

            conn.close()

            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "message": f"Successfully imported {len(df)} rows into {data_type} table",
                        "rows_imported": len(df),
                        "columns": list(df.columns)
                    }, indent=2)
                )
            ]

        elif name == "get_database_stats":
            conn = get_db_connection()
            cursor = conn.cursor()

            stats = {}

            tables = ['campaigns', 'ad_groups', 'keywords', 'search_terms', 'account_summary']

            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]

                cursor.execute(f"SELECT MIN(date), MAX(date) FROM {table}")
                date_range = cursor.fetchone()

                stats[table] = {
                    "row_count": count,
                    "date_range": {
                        "min": date_range[0],
                        "max": date_range[1]
                    } if date_range[0] else None
                }

            conn.close()

            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "database_path": str(DB_PATH),
                        "tables": stats,
                        "database_size_bytes": DB_PATH.stat().st_size if DB_PATH.exists() else 0
                    }, indent=2)
                )
            ]

        elif name == "clear_database":
            if not arguments.get("confirm", False):
                return [
                    TextContent(
                        type="text",
                        text="Error: Must set 'confirm' to true to clear database"
                    )
                ]

            conn = get_db_connection()
            cursor = conn.cursor()

            tables = ['campaigns', 'ad_groups', 'keywords', 'search_terms', 'account_summary']

            for table in tables:
                cursor.execute(f"DELETE FROM {table}")

            conn.commit()
            conn.close()

            return [
                TextContent(
                    type="text",
                    text="Database cleared successfully"
                )
            ]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        ]


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="googleads://local/stats",
            name="Local Database Statistics",
            mimeType="application/json",
            description="Statistics about locally stored Google Ads data"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content"""
    if uri == "googleads://local/stats":
        try:
            if not DB_PATH.exists():
                return json.dumps({"error": "No local database found. Import data first."})

            conn = get_db_connection()
            cursor = conn.cursor()

            stats = {}
            tables = ['campaigns', 'ad_groups', 'keywords', 'search_terms', 'account_summary']

            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]

            conn.close()

            return json.dumps(stats, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    raise ValueError(f"Unknown resource: {uri}")


async def main():
    """Main entry point for the MCP server"""
    from mcp.server.stdio import stdio_server

    # Initialize database on startup
    init_database()

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
