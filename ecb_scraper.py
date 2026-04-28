"""
ECB Press Conference Script Extractor

This script extracts content from ECB press conference pages.
It parses the HTML and extracts the main text content.
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import json
from datetime import datetime


class ECBScraper:
    def __init__(self, output_dir="output"):
        """Initialize the ECB scraper with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        # Set a user agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_press_conference(self, url):
        """
        Scrape a single ECB press conference page.
        
        Args:
            url (str): The URL of the press conference page
            
        Returns:
            dict: Dictionary containing extracted data
        """
        print(f"Fetching: {url}")
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data
        data = {
            'url': url,
            'fetched_at': datetime.now().isoformat(),
            'title': self._extract_title(soup),
            'content': self._extract_content(soup),
            'metadata': self._extract_metadata(soup)
        }
        
        return data

    def _extract_title(self, soup):
        """Extract the page title."""
        # Try different selectors commonly used on ECB pages
        title_selectors = [
            'h1',
            'title',
            'meta[property="og:title"]',
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                if selector == 'meta[property="og:title"]':
                    return element.get('content', '')
                return element.get_text(strip=True)
        
        return "ECB Press Conference"

    def _extract_content(self, soup):
        """Extract main content from the page."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find main content area
        content_selectors = [
            'main',
            'article',
            '.content',
            '.main-content',
            '.article-content',
            '[role="main"]'
        ]
        
        content_area = None
        for selector in content_selectors:
            content_area = soup.select_one(selector)
            if content_area:
                break
        
        # If no content area found, use the whole body
        if not content_area:
            content_area = soup.body if soup.body else soup
        
        # Extract all paragraphs and text
        paragraphs = content_area.find_all(['p', 'h2', 'h3', 'h4'])
        
        content_lines = []
        for para in paragraphs:
            text = para.get_text(strip=True)
            if text and len(text) > 20:  # Filter out very short lines
                content_lines.append(text)
        
        return '\n\n'.join(content_lines)

    def _extract_metadata(self, soup):
        """Extract metadata from the page."""
        metadata = {}
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        # Extract date if available
        date_patterns = ['publish', 'date', 'published']
        for key, value in metadata.items():
            if any(pattern in key.lower() for pattern in date_patterns):
                metadata['publication_date'] = value
                break
        
        return metadata

    def save_to_file(self, data, filename=None):
        """
        Save extracted data to a file.
        
        Args:
            data (dict): The extracted data
            filename (str): Optional filename (defaults to timestamp-based name)
        """
        if not data:
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ecb_press_conference_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved to: {filepath}")
        return filepath

    def save_to_text(self, data, filename=None):
        """
        Save extracted content to a text file.
        
        Args:
            data (dict): The extracted data
            filename (str): Optional filename (defaults to timestamp-based name)
        """
        if not data:
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ecb_press_conference_{timestamp}.txt"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {data['title']}\n")
            f.write(f"URL: {data['url']}\n")
            f.write(f"Fetched: {data['fetched_at']}\n")
            f.write("\n" + "="*80 + "\n\n")
            f.write(data['content'])
        
        print(f"Saved text to: {filepath}")
        return filepath


def main():
    """Main function to demonstrate usage."""
    # URL from your request
    url = "https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2026/html/ecb.is260319~93b1cbad97.en.html"
    
    scraper = ECBScraper()
    data = scraper.scrape_press_conference(url)
    
    if data:
        # Save as JSON
        scraper.save_to_file(data)
        # Save as plain text
        scraper.save_to_text(data)
        
        print("\nExtracted Title:", data['title'])
        print("\nContent Preview (first 500 characters):")
        print(data['content'][:500])
    else:
        print("Failed to scrape the press conference.")


if __name__ == "__main__":
    main()
