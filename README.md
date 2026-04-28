# ECB Press Conference Script Extractor

A Python tool to extract and parse ECB (European Central Bank) press conference scripts from their website.

## Features

- Extracts press conference content from ECB website
- Parses HTML to clean and structure text
- Saves extracted content in both JSON and text formats
- Handles metadata extraction
- Error handling for network requests

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml

## Installation

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from ecb_scraper import ECBScraper

# Create scraper instance
scraper = ECBScraper()

# Scrape a press conference
url = "https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2026/html/ecb.is260319~93b1cbad97.en.html"
data = scraper.scrape_press_conference(url)

# Save the data
scraper.save_to_file(data)  # Saves as JSON
scraper.save_to_text(data)  # Saves as plain text
```

### Command Line

Run the script directly to scrape the default URL:

```bash
python ecb_scraper.py
```

## Output

The scraper generates two types of output files in the `output` directory:

1. **JSON files**: Contains all extracted data including metadata
2. **Text files**: Contains formatted text content for easy reading

## Data Extracted

- **Title**: The main heading of the press conference
- **Content**: The full text content of the page
- **Metadata**: Meta tags, publication date, and other page information
- **URL**: The source URL
- **Timestamp**: When the data was fetched

## License

MIT
