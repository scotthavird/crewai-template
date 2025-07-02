import logging
import time
from typing import Optional, Type

import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class WebScraperInput(BaseModel):
    """Input schema for WebScraperTool."""
    url: str = Field(..., description="The URL to scrape content from")
    max_content_length: Optional[int] = Field(
        default=5000,
        description="Maximum content length to return (default: 5000 characters)"
    )
    extract_links: Optional[bool] = Field(
        default=False,
        description="Whether to extract and return links from the page"
    )

class WebScraperTool(BaseTool):
    name: str = "Web Content Scraper"
    description: str = (
        "Scrapes and extracts clean text content from web pages. "
        "Perfect for gathering information from websites, articles, and documentation. "
        "Can optionally extract links for further research."
    )
    args_schema: Type[BaseModel] = WebScraperInput

    def _run(self, url: str, max_content_length: int = 5000, extract_links: bool = False) -> str:
        """
        Scrape content from a web page and return clean text.

        Args:
            url: The URL to scrape
            max_content_length: Maximum length of content to return
            extract_links: Whether to extract links from the page

        Returns:
            Formatted string with scraped content and optionally links
        """
        try:
            # Add delay to be respectful to servers
            time.sleep(1)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            logger.info(f"Scraping content from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            # Get text content
            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            # Truncate if necessary
            if len(text) > max_content_length:
                text = text[:max_content_length] + "..."

            result = f"Content from {url}:\n\n{text}"

            # Extract links if requested
            if extract_links:
                links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    link_text = link.get_text().strip()
                    if href.startswith('http') and link_text:
                        links.append(f"- {link_text}: {href}")

                if links:
                    result += f"\n\nFound {len(links)} links:\n" + "\n".join(links[:10])
                    if len(links) > 10:
                        result += f"\n... and {len(links) - 10} more links"

            logger.info(f"Successfully scraped {len(text)} characters from {url}")
            return result

        except requests.RequestException as e:
            error_msg = f"Failed to scrape {url}: {str(e)}"
            logger.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error processing content from {url}: {str(e)}"
            logger.error(error_msg)
            return error_msg
