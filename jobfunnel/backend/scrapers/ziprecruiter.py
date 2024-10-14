from jobfunnel.backend.scrapers.base import BaseCANEngScraper
from jobfunnel.backend.scrapers.jobspybase import BaseJobSpyScraper


class BaseZipRecruiterScraper(BaseJobSpyScraper):
    """Scrape jobs from Ziprecruiter.X"""

    @property
    def site_name(self):
        return "zip_recruiter"


class ZipRecruiterScraperCANEng(BaseZipRecruiterScraper, BaseCANEngScraper):
    """Scrapes jobs from www.Ziprecruiter.ca"""
