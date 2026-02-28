# Google Ads LOCAL MCP Server

**100% LOCAL - NO CLOUD API CALLS**

A Model Context Protocol (MCP) server for querying locally stored Google Ads data using natural language. All data is stored in a local SQLite database and queried without any cloud API calls.

## Key Differences from Cloud Version

| Feature | Local Version | Cloud API Version |
|---------|--------------|-------------------|
| **Data Storage** | Local SQLite database | Google Cloud |
| **API Calls** | None (100% local) | Required for every query |
| **Setup Complexity** | Simple (no OAuth) | Complex (OAuth, tokens, etc.) |
| **Internet Required** | No (after data export) | Yes (always) |
| **Data Freshness** | Manual updates via CSV | Real-time |
| **Cost** | Free | API quota limits |
| **Privacy** | Complete control | Data on Google servers |
| **Speed** | Very fast | Network dependent |

## When to Use Local Version

✅ **Use Local Version if you:**
- Want complete privacy and data control
- Don't want to deal with OAuth setup
- Need to work offline
- Want faster query responses
- Don't need real-time data
- Prefer to export data periodically from Google Ads UI

❌ **Use Cloud API Version if you:**
- Need real-time data
- Want automatic data sync
- Don't want to manually export CSVs
- Need to query very recent data (today/yesterday)

## Setup (Simple!)

### Step 1: Install Dependencies

```bash
pip install -r requirements-local.txt
```

That's it! No OAuth, no API tokens, no complex setup.

### Step 2: Export Data from Google Ads

1. Go to https://ads.google.com
2. Navigate to Reports → Predefined Reports
3. Export the reports you need:
   - **Campaign Performance Report** (Campaigns → Export)
   - **Ad Group Performance Report** (Ad groups → Export)
   - **Keyword Performance Report** (Keywords → Export)
   - **Search Terms Report** (Search terms → Export)

4. Download as CSV files

### Step 3: Import Data

Run the import utility:

```bash
python import_google_ads_data.py
```

Follow the prompts to import your CSV files. The script will:
- Create the local SQLite database automatically
- Map CSV columns to database tables
- Import all your data
- Show statistics

### Step 4: Connect to Claude Desktop

Add to your Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "google-ads-local": {
      "command": "python",
      "args": ["/home/user/DataScienceWork/google_ads_local_mcp_server.py"]
    }
  }
}
```

Restart Claude Desktop and you're done!

## Usage

### Natural Language Queries

Ask questions just like the cloud version:

- "Show me campaign performance"
- "What are my top performing keywords?"
- "Give me search term data"
- "What's my daily performance trend?"

### Available Tools

#### 1. `query_local_ads_data`

Query your local Google Ads data using natural language or SQL.

**Natural language patterns:**
- `campaign performance` - Campaign metrics
- `ad group performance` - Ad group metrics
- `keyword performance` - Keyword metrics
- `search terms` - Search term data
- `account overview` - Account summary
- `top performing campaigns` - Best campaigns
- `daily performance` - Day-by-day trends
- `campaign summary` - Overall statistics

**Custom SQL:**
```sql
SELECT name, SUM(cost) as total_cost, SUM(conversions) as total_conversions
FROM campaigns
WHERE date >= '2024-01-01'
GROUP BY name
ORDER BY total_conversions DESC
```

#### 2. `import_csv_data`

Import new CSV data directly from queries.

#### 3. `get_database_stats`

View statistics about your local database (row counts, date ranges).

#### 4. `clear_database`

Clear all data (use with caution).

## Updating Your Data

Your local database is a snapshot. To update it:

1. Export fresh data from Google Ads
2. Run `python import_google_ads_data.py`
3. Import the new CSV files

**Tip**: Set a reminder to update weekly or monthly, depending on your needs.

## Database Structure

The local database (`google_ads_data.db`) has these tables:

- **campaigns** - Campaign performance data
- **ad_groups** - Ad group performance data
- **keywords** - Keyword performance data
- **search_terms** - Search term performance data
- **account_summary** - Account-level summary data

Each table includes:
- Performance metrics (impressions, clicks, cost, conversions)
- Date field for time-based analysis
- Status and metadata fields

## Example Workflows

### Weekly Performance Review

```bash
# Monday: Export last week's data from Google Ads
# Import into local database
python import_google_ads_data.py

# Then in Claude Desktop:
# "Show me last week's campaign performance"
# "What were my top converting keywords?"
# "Compare this week to last week"
```

### Monthly Analysis

```bash
# Export monthly data
# Import to database
# Query trends and patterns without API limits
```

## Advanced SQL Queries

Since you have direct SQL access, you can do powerful queries:

```sql
-- Top keywords by ROI
SELECT
    keyword_text,
    campaign_name,
    SUM(conversions) as total_conversions,
    SUM(cost) as total_cost,
    SUM(conversions) / SUM(cost) as roi
FROM keywords
WHERE date >= date('now', '-30 days')
GROUP BY keyword_text, campaign_name
HAVING total_cost > 0
ORDER BY roi DESC
LIMIT 20;
```

```sql
-- Campaign performance by day of week
SELECT
    strftime('%w', date) as day_of_week,
    CASE strftime('%w', date)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END as day_name,
    AVG(clicks) as avg_clicks,
    AVG(conversions) as avg_conversions,
    AVG(ctr) as avg_ctr
FROM campaigns
GROUP BY day_of_week
ORDER BY day_of_week;
```

```sql
-- Month-over-month comparison
SELECT
    strftime('%Y-%m', date) as month,
    COUNT(DISTINCT name) as active_campaigns,
    SUM(impressions) as impressions,
    SUM(clicks) as clicks,
    SUM(cost) as cost,
    SUM(conversions) as conversions
FROM campaigns
GROUP BY month
ORDER BY month DESC;
```

## Exporting Data from Google Ads UI

### Detailed Export Instructions

1. **Login** to https://ads.google.com
2. **Click "Reports"** in the left menu
3. **Select the report type** you want (Campaigns, Keywords, etc.)
4. **Set date range** (e.g., Last 30 days, Last 90 days)
5. **Click Download icon** (⬇️)
6. **Choose "CSV"** format
7. **Save the file**

### Recommended Exports

**For comprehensive analysis, export:**
1. Campaign performance report (last 90 days)
2. Keyword performance report (last 90 days)
3. Search terms report (last 30 days)
4. Ad group performance report (last 90 days)

### Column Names

The import script automatically maps common Google Ads column names:
- Campaign → name
- Impressions → impressions
- Clicks → clicks
- Cost → cost
- Conversions → conversions
- etc.

If your CSV has different column names, the script will show you what it found.

## Troubleshooting

### "No such column" Error

Your CSV columns don't match expected names. Check:
1. Is the CSV from Google Ads UI?
2. Are column headers in English?
3. Try inspecting the CSV in a text editor

### "Table not found" Error

Database not initialized. Run:
```bash
python google_ads_local_mcp_server.py
```
This will create the database.

### "Permission denied" Error

Check file permissions:
```bash
chmod +x google_ads_local_mcp_server.py
chmod +x import_google_ads_data.py
```

### No Data in Results

Check database stats:
```python
# In Claude Desktop, ask:
"Show me database statistics"
```

If tables are empty, import CSV data first.

## Backup Your Data

Your database is stored in `google_ads_data.db`. To backup:

```bash
cp google_ads_data.db google_ads_data.db.backup
```

Or use git to version control it (though the file may get large).

## Comparing with Cloud Version

You can use both!

- Use **local version** for historical analysis and fast queries
- Use **cloud version** (the other server) for real-time data

Run both MCP servers:

```json
{
  "mcpServers": {
    "google-ads-local": {
      "command": "python",
      "args": ["/path/to/google_ads_local_mcp_server.py"]
    },
    "google-ads-cloud": {
      "command": "python",
      "args": ["/path/to/google_ads_mcp_server.py"],
      "cwd": "/path/to/DataScienceWork"
    }
  }
}
```

Then you can choose which to query!

## Performance

The local version is **much faster** than API calls:
- No network latency
- No API rate limits
- No authentication overhead
- Direct SQL queries on local data

Complex queries that might take seconds with the API complete in milliseconds locally.

## Privacy & Security

✅ **Benefits:**
- All data stored locally on your machine
- No data sent to Google servers during queries
- Complete control over your data
- No OAuth tokens to secure
- No API credentials to manage

⚠️ **Considerations:**
- Database file contains your ad data (don't commit to public repos!)
- Add `google_ads_data.db` to `.gitignore`

## Resources

- [Google Ads Reports Guide](https://support.google.com/google-ads/answer/2375483)
- [Exporting Data from Google Ads](https://support.google.com/google-ads/answer/3022229)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [MCP Documentation](https://modelcontextprotocol.io/)

## License

MIT License - Feel free to modify and use as needed.
