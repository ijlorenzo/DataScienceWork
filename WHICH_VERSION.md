# Which Version Should I Use?

This repository contains **TWO** Google Ads MCP servers:

## 🏠 Local Version (Recommended for Most Users)

**File:** `google_ads_local_mcp_server.py`

**Pros:**
- ✅ **Simple setup** - No OAuth, no API tokens
- ✅ **100% local** - No cloud API calls
- ✅ **Works offline** - No internet needed after data export
- ✅ **Fast** - Local queries are instant
- ✅ **Private** - Your data never leaves your machine
- ✅ **Free** - No API quotas or limits
- ✅ **Beginner friendly** - Easy to understand

**Cons:**
- ❌ Manual data updates (export CSV from Google Ads periodically)
- ❌ Not real-time (data is a snapshot)
- ❌ Requires CSV exports from Google Ads UI

**Best for:**
- Learning and experimentation
- Historical data analysis
- Privacy-conscious users
- Offline work
- Users who don't need real-time data
- Avoiding OAuth complexity

**Setup time:** ~5 minutes

---

## ☁️ Cloud API Version (Advanced Users)

**File:** `google_ads_mcp_server.py`

**Pros:**
- ✅ **Real-time data** - Always up to date
- ✅ **Automatic** - No manual CSV exports
- ✅ **Live queries** - Get today's data
- ✅ **Full API access** - All Google Ads features

**Cons:**
- ❌ Complex setup (OAuth2, developer token, refresh token)
- ❌ Requires internet connection
- ❌ API rate limits and quotas
- ❌ Data stored on Google servers
- ❌ Slower (network latency)
- ❌ Google API approval may be needed for production

**Best for:**
- Production applications
- Real-time monitoring
- Users who need current data
- Automated reporting
- Users comfortable with API authentication

**Setup time:** ~30 minutes

---

## Quick Comparison Table

| Feature | Local Version | Cloud API Version |
|---------|--------------|-------------------|
| **Setup Difficulty** | 🟢 Easy | 🔴 Hard |
| **Internet Required** | 🟢 No* | 🔴 Yes |
| **Data Freshness** | 🟡 Manual updates | 🟢 Real-time |
| **Speed** | 🟢 Very fast | 🟡 Network dependent |
| **Privacy** | 🟢 Complete | 🟡 Data on Google |
| **Cost** | 🟢 Free | 🟡 API limits |
| **Maintenance** | 🟡 Manual exports | 🟢 Automatic |
| **Offline Work** | 🟢 Yes | 🔴 No |

*Internet needed only to export CSV from Google Ads UI initially

---

## Decision Guide

### Choose **LOCAL** if:
- ✅ You're just getting started
- ✅ You want simple setup
- ✅ You export data from Google Ads UI anyway
- ✅ You analyze data weekly/monthly (not daily)
- ✅ You want complete privacy
- ✅ You don't want to deal with OAuth

### Choose **CLOUD API** if:
- ✅ You need real-time data
- ✅ You want automatic updates
- ✅ You're building a production tool
- ✅ You need today's/yesterday's data
- ✅ You're comfortable with API setup
- ✅ You want programmatic access

---

## Can I Use Both?

**Yes!** You can run both servers simultaneously:

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

Then use:
- **Local version** for historical analysis and fast queries
- **Cloud version** for checking today's performance

---

## Recommended: Start Local, Upgrade If Needed

1. **Start with local version** (5 min setup)
2. Export some CSV data from Google Ads
3. Try querying and analyzing
4. If you need real-time data later, set up cloud version

This approach lets you:
- Get started quickly
- Learn the system with simple setup
- Decide if you need real-time data
- Avoid wasting time on OAuth if local is enough

---

## Setup Guides

- **Local Version**: See [README_LOCAL.md](README_LOCAL.md)
- **Cloud API Version**: See [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)

---

## Still Unsure?

Ask yourself: **"Do I need data from today/yesterday?"**

- **No** → Use local version
- **Yes** → Use cloud API version

Most users doing weekly/monthly analysis will be fine with the local version and manual CSV exports.
