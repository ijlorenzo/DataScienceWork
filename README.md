# Customer Feedback Synthesis Tool

A web-based application that consolidates customer feedback from multiple sources (PMM, MSA, Support, Social Listening), uses dual-LLM categorization (OpenAI + Claude) to intelligently categorize items into a standardized 52-field output schema.

## Features

- **Upload PMM Excel/CSV files** - Auto-detect source type from columns
- **LLM-Powered Categorization** - Uses OpenAI GPT-4o (Claude Sonnet 4.5 support included)
- **Intelligent Mapping** - Maps columns to standardized output schema
- **Rich Output** - Exports to Excel with LLM reasoning fields and formatting
- **52-Field Schema** - Comprehensive categorization including Product Area, Vertical, Personas, Severity, etc.

## Tech Stack

- **Frontend:** React 18, Tailwind CSS, AG Grid, Recharts
- **Backend:** Python Flask
- **Database:** SQLite (for future phases)
- **LLMs:** OpenAI GPT-4o + Claude Sonnet 4.5
- **File Processing:** pandas, openpyxl

## Project Structure

```
/customer-feedback-tool
├── /frontend
│   ├── /src
│   │   ├── /components        # React components
│   │   ├── /utils            # API client utilities
│   │   ├── App.jsx           # Main app component
│   │   └── index.js          # Entry point
│   ├── package.json
│   └── tailwind.config.js
│
├── /backend
│   ├── /api                  # API route handlers (future)
│   ├── /models               # LLM client
│   ├── /parsers              # File parsers (PMM, MSA, etc.)
│   ├── /utils                # Excel generator, value translator
│   ├── requirements.txt
│   └── app.py                # Flask application
│
├── /config
│   ├── taxonomies.json       # Product categories, personas, verticals
│   └── llm_prompt.txt        # LLM categorization prompt template
│
└── /data
    ├── /uploads              # Uploaded files
    └── /exports              # Generated Excel files
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key
- Anthropic API key (optional, for Claude support)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # OPENAI_API_KEY=your_openai_key_here
   # ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

5. **Run the backend server:**
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will start on `http://localhost:3000`

## Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Upload a PMM Excel or CSV file** by clicking the upload area

3. **Click "Process File"** to start LLM categorization

4. **Wait for processing** (typically 2-3 minutes for 100 items)

5. **Download the categorized Excel file** with all LLM reasoning included

## Output Schema

The tool generates a 52-field output schema including:

### DESCRIBE
- Customer need
- Product/feature request
- Need description
- Request type

### PRODUCT
- Product Area (52 options)
- Product Category (7 categories)
- Customer-facing product category

### CUSTOMER IMPACT
- Vertical (18 industries)
- Number of customers
- Personas (17 types)
- UXR Needs Based Segmentation (6 archetypes)
- Sales Segment
- User Touchpoint

### PRIORITY
- Revenue [T-shirt Size]
- Reach [T-shirt Size]
- Severity [T-shirt Size]
- Revenue Sizing Needed flag

### TRACKING
- Roadmap Status
- Last Updated date
- ADO Link
- Unique ID

### SOURCE
- Listening Type
- Listening Source
- Date Created

### OWNERSHIP
- PMM
- PM
- GPM
- Business Planning

**Every categorization field includes an "LLM Reasoning" column** explaining the model's decision.

## Configuration

### Taxonomies (`config/taxonomies.json`)

Defines all valid values for categorization fields:
- 7 Product Categories
- 52 Product Areas
- 18 Verticals
- 17 Personas
- 6 UXR Segments
- And more...

### LLM Prompt (`config/llm_prompt.txt`)

The prompt template used for categorization. Customize this to adjust LLM behavior.

## API Endpoints

- `POST /api/upload` - Upload and parse file
- `POST /api/process` - Process file with LLM categorization
- `GET /api/export/<filename>` - Download categorized Excel file

## Future Phases

- **Phase 2:** Dual-LLM voting (OpenAI + Claude consensus)
- **Phase 3:** Learning mapping system (persistent disambiguation)
- **Phase 4:** Interactive review UI with AG Grid
- **Phase 5:** Analytics dashboard with Recharts
- **Phase 6:** Multi-source support (MSA, Support, Social)

## Troubleshooting

### Backend won't start
- Check that Python virtual environment is activated
- Verify all dependencies are installed: `pip list`
- Ensure `.env` file exists with valid API keys

### Frontend won't start
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`
- Check that backend is running on port 5000

### LLM categorization fails
- Verify API keys are correct in `.env`
- Check OpenAI/Anthropic API quota and billing
- Review error messages in browser console and backend logs

### Excel export fails
- Ensure `openpyxl` is installed: `pip install openpyxl`
- Check that `data/exports` directory exists and is writable

## Contributing

This is Phase 1 MVP. Future contributions will focus on:
- Adding dual-LLM voting mechanism
- Building learning mapping table
- Creating interactive review UI
- Supporting additional data sources

## License

MIT License

## Support

For issues or questions, please create a GitHub issue.
