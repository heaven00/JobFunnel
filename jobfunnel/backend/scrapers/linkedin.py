from jobfunnel.backend.scrapers.base import BaseCANEngScraper
from jobfunnel.backend.scrapers.jobspybase import BaseJobSpyScraper


class BaseLinkedInScraper(BaseJobSpyScraper):
    """Scrape jobs from Linkedin.X"""

    @property
    def site_name(self):
        return "linkedin"


class LinkedInScraperCANEng(BaseLinkedInScraper, BaseCANEngScraper):
    """Scrapes jobs from www.linkedin.ca"""
