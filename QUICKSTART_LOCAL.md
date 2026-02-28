# Quick Start - Local Version (5 Minutes)

Get querying your Google Ads data in 5 minutes with ZERO API setup!

## Step 1: Install Dependencies (1 minute)

```bash
cd /home/user/DataScienceWork
pip install -r requirements-local.txt
```

## Step 2: Export Data from Google Ads (2 minutes)

1. Go to https://ads.google.com
2. Click **Reports** in left menu
3. Click **Predefined reports** → **Campaign performance**
4. Set date range (e.g., "Last 30 days")
5. Click **Download** icon → Choose **CSV**
6. Save the file (e.g., `campaigns.csv`)

## Step 3: Import Your Data (1 minute)

```bash
python import_google_ads_data.py
```

- Choose option **1** (Campaign Performance Report)
- Enter the path to your CSV file
- Done! Data is now in local database

## Step 4: Configure Claude Desktop (1 minute)

Edit your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Linux**: `~/.config/Claude/claude_desktop_config.json`

Add:

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

**Important**: Update the path to match where you cloned this repo!

Restart Claude Desktop.

## Step 5: Start Querying! (now)

In Claude Desktop, try:

- "Show me my campaign performance"
- "What are my top performing campaigns?"
- "Show me campaigns by cost"
- "Give me a summary of my campaign data"

That's it! You're querying Google Ads data locally.

---

## What's Next?

### Import More Data Types

Run the import script again to add:
- Keywords
- Ad groups
- Search terms
- Account summaries

```bash
python import_google_ads_data.py
```

### Update Your Data Weekly

Google Ads data gets stale. Update it:

1. Export fresh CSV from Google Ads (same as Step 2)
2. Import again (same as Step 3)
3. Query updated data

Set a calendar reminder to do this weekly or monthly!

### Advanced Queries

Try custom SQL queries:

```
Query my data: "SELECT name, SUM(cost) FROM campaigns WHERE conversions > 0 GROUP BY name"
```

### View Database Stats

```
Show me database statistics
```

---

## Troubleshooting

### "No module named 'mcp'"

Run: `pip install -r requirements-local.txt`

### "No data in results"

You need to import CSV data first. Run `python import_google_ads_data.py`

### "File not found" when importing

Check the path to your CSV file. Use absolute path like `/Users/you/Downloads/campaigns.csv`

### MCP server not connecting

1. Check the path in `claude_desktop_config.json` is correct (absolute path!)
2. Try running manually first: `python google_ads_local_mcp_server.py`
3. Check Claude Desktop logs for errors

---

## Pro Tips

💡 **Tip 1**: Export 90 days of data for better trend analysis

💡 **Tip 2**: Import multiple data types (campaigns, keywords, search terms) for richer analysis

💡 **Tip 3**: Keep your CSV files organized in a folder like `~/google-ads-exports/`

💡 **Tip 4**: Backup your database: `cp google_ads_data.db google_ads_data.db.backup`

💡 **Tip 5**: Use custom SQL for complex analysis - you have full SQL power!

---

## Example Queries to Try

Once you have data imported:

- "Show me campaigns sorted by conversions"
- "What's my average cost per click?"
- "Which campaigns spent the most money?"
- "Show me daily performance trends"
- "What's my total spend and conversions?"
- "Compare campaigns by ROI"

---

## Full Documentation

- **Complete Guide**: [README_LOCAL.md](README_LOCAL.md)
- **Choosing a Version**: [WHICH_VERSION.md](WHICH_VERSION.md)
- **Cloud Version**: [README.md](README.md)

Enjoy fast, local Google Ads queries! 🚀
