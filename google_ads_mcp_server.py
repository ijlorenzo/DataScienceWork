#!/usr/bin/env python3
"""
Google Ads MCP Server
Provides natural language querying capabilities for Google Ads data
"""

import os
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from mcp.server import Server
from mcp.types import Tool, TextContent, Resource, ResourceTemplate
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MCP server
app = Server("google-ads-mcp")

# Initialize Google Ads client
def get_google_ads_client():
    """Initialize and return Google Ads client"""
    try:
        credentials = {
            "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
            "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
            "use_proto_plus": True
        }

        return GoogleAdsClient.load_from_dict(credentials)
    except Exception as e:
        raise Exception(f"Failed to initialize Google Ads client: {str(e)}")


def execute_query(client: GoogleAdsClient, customer_id: str, query: str) -> List[Dict[str, Any]]:
    """Execute a Google Ads Query Language (GAQL) query"""
    try:
        ga_service = client.get_service("GoogleAdsService")
        stream = ga_service.search_stream(customer_id=customer_id, query=query)

        results = []
        for batch in stream:
            for row in batch.results:
                # Convert row to dictionary
                result_dict = {}
                for field in row._pb.DESCRIPTOR.fields:
                    field_name = field.name
                    if hasattr(row, field_name):
                        value = getattr(row, field_name)
                        # Handle nested messages and enums
                        if hasattr(value, '_pb'):
                            result_dict[field_name] = str(value)
                        else:
                            result_dict[field_name] = value
                results.append(result_dict)

        return results
    except GoogleAdsException as ex:
        error_msg = f"Google Ads API error: {ex.error.message}"
        for error in ex.failure.errors:
            error_msg += f"\n  - {error.message}"
        raise Exception(error_msg)
    except Exception as e:
        raise Exception(f"Query execution failed: {str(e)}")


def natural_language_to_gaql(natural_query: str) -> str:
    """
    Convert natural language query to GAQL
    This is a simple mapping - in production, you'd want to use an LLM for this
    """
    query = natural_query.lower().strip()

    # Define common query patterns
    patterns = {
        "campaign performance": """
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM campaign
            WHERE segments.date DURING LAST_30_DAYS
            ORDER BY metrics.impressions DESC
        """,

        "ad group performance": """
            SELECT
                ad_group.id,
                ad_group.name,
                ad_group.status,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr
            FROM ad_group
            WHERE segments.date DURING LAST_30_DAYS
            ORDER BY metrics.impressions DESC
        """,

        "keyword performance": """
            SELECT
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                ad_group.name,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM keyword_view
            WHERE segments.date DURING LAST_30_DAYS
            ORDER BY metrics.impressions DESC
            LIMIT 100
        """,

        "search terms": """
            SELECT
                search_term_view.search_term,
                search_term_view.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr
            FROM search_term_view
            WHERE segments.date DURING LAST_30_DAYS
            ORDER BY metrics.impressions DESC
            LIMIT 100
        """,

        "account overview": """
            SELECT
                customer.id,
                customer.descriptive_name,
                customer.currency_code,
                customer.time_zone,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr
            FROM customer
            WHERE segments.date DURING LAST_30_DAYS
        """,

        "top performing campaigns": """
            SELECT
                campaign.id,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.conversions,
                metrics.cost_micros,
                metrics.ctr,
                metrics.conversions_value
            FROM campaign
            WHERE segments.date DURING LAST_30_DAYS
            AND campaign.status = 'ENABLED'
            ORDER BY metrics.conversions DESC
            LIMIT 10
        """
    }

    # Match query to pattern
    for pattern_key, gaql_query in patterns.items():
        if pattern_key in query:
            return gaql_query.strip()

    # If no pattern matches, return the query as-is (assuming it's already GAQL)
    return natural_query


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for Google Ads querying"""
    return [
        Tool(
            name="query_google_ads",
            description="""Query Google Ads data using natural language or GAQL (Google Ads Query Language).

            Supported natural language queries:
            - "campaign performance" - Get performance metrics for all campaigns
            - "ad group performance" - Get performance metrics for all ad groups
            - "keyword performance" - Get performance metrics for keywords
            - "search terms" - Get search term performance data
            - "account overview" - Get overall account metrics
            - "top performing campaigns" - Get best performing campaigns by conversions

            You can also provide custom GAQL queries directly.

            Example queries:
            - "Show me campaign performance for the last 30 days"
            - "What are my top performing campaigns?"
            - "SELECT campaign.name, metrics.impressions FROM campaign WHERE segments.date DURING LAST_7_DAYS"
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query or GAQL query string"
                    },
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID (optional, uses default from .env if not provided)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_account_info",
            description="Get basic information about the Google Ads account",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID (optional, uses default from .env if not provided)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="list_campaigns",
            description="List all campaigns in the account with basic information",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID (optional, uses default from .env if not provided)"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by campaign status (ENABLED, PAUSED, REMOVED)",
                        "enum": ["ENABLED", "PAUSED", "REMOVED", "ALL"]
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    try:
        client = get_google_ads_client()
        customer_id = arguments.get("customer_id", os.getenv("GOOGLE_ADS_CUSTOMER_ID"))

        # Remove hyphens from customer ID if present
        if customer_id:
            customer_id = customer_id.replace("-", "")

        if name == "query_google_ads":
            query_input = arguments.get("query", "")

            # Convert natural language to GAQL if needed
            if not query_input.strip().upper().startswith("SELECT"):
                gaql_query = natural_language_to_gaql(query_input)
            else:
                gaql_query = query_input

            results = execute_query(client, customer_id, gaql_query)

            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "query": gaql_query,
                        "results": results,
                        "count": len(results)
                    }, indent=2, default=str)
                )
            ]

        elif name == "get_account_info":
            query = """
                SELECT
                    customer.id,
                    customer.descriptive_name,
                    customer.currency_code,
                    customer.time_zone,
                    customer.status
                FROM customer
            """
            results = execute_query(client, customer_id, query)

            return [
                TextContent(
                    type="text",
                    text=json.dumps(results, indent=2, default=str)
                )
            ]

        elif name == "list_campaigns":
            status_filter = arguments.get("status", "ALL")

            query = """
                SELECT
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    campaign.advertising_channel_type,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros
                FROM campaign
                WHERE segments.date DURING LAST_30_DAYS
            """

            if status_filter != "ALL":
                query += f" AND campaign.status = '{status_filter}'"

            query += " ORDER BY campaign.name"

            results = execute_query(client, customer_id, query)

            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "campaigns": results,
                        "count": len(results)
                    }, indent=2, default=str)
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
            uri="googleads://account/info",
            name="Account Information",
            mimeType="application/json",
            description="Current Google Ads account information"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content"""
    if uri == "googleads://account/info":
        try:
            client = get_google_ads_client()
            customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "")

            query = """
                SELECT
                    customer.id,
                    customer.descriptive_name,
                    customer.currency_code,
                    customer.time_zone
                FROM customer
            """
            results = execute_query(client, customer_id, query)
            return json.dumps(results, indent=2, default=str)
        except Exception as e:
            return json.dumps({"error": str(e)})

    raise ValueError(f"Unknown resource: {uri}")


async def main():
    """Main entry point for the MCP server"""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
