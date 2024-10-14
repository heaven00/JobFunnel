from abc import abstractmethod
from datetime import datetime
from typing import Dict, List

from jobspy import scrape_jobs

from jobfunnel.backend.job import Job
from jobfunnel.backend.scrapers.base import BaseScraper
from jobfunnel.resources.enums import JobField, JobStatus


class BaseJobSpyScraper(BaseScraper):
    """Base scraper based on jobspy library"""

    @property
    @abstractmethod
    def site_name(self) -> str:
        """
        set the site name to scrape
        """

    def scrape(self) -> Dict[str, Job]:
        query = " ".join(self.config.search_config.keywords)
        try:
            jobs = scrape_jobs(
                site_name=[self.site_name],
                search_term=query,
                location=self.config.search_config.province_or_state,
                distance=self.config.search_config.radius,
                hours_old=self.config.search_config.max_listing_days * 24,
                results_wanted=20,
                linkedin_fetch_description=True,
            )
        except Exception as err:
            self.logger.error("Unable to scrape from ", self.site_name)
            self.logger.error("Because: ", err.message)

        return self._rows_to_json(query, jobs)

    def _rows_to_json(self, query, jobs):
        jobs_dict = {}
        #   column list
        #   Index(['id', 'site', 'job_url', 'job_url_direct', 'title', 'company',
        #    'location', 'job_type', 'date_posted', 'salary_source', 'interval',
        #    'min_amount', 'max_amount', 'currency', 'is_remote', 'job_level',
        #    'job_function', 'company_industry', 'listing_type', 'emails',
        #    'description', 'company_url', 'company_url_direct', 'company_addresses',
        #    'company_num_employees', 'company_revenue', 'company_description',
        #    'logo_photo_url', 'banner_photo_url', 'ceo_name', 'ceo_photo_url'],
        #   dtype='object')

        for _, row in jobs.iterrows():
            try:
                key_id = "-".join([row["site"], row["id"]])
                job = Job(
                    title=row["title"],
                    company=row["company"],
                    location=row["location"],
                    description=row["description"],
                    url=row["job_url"],
                    provider=row["site"],
                    key_id=key_id,
                    locale=self.locale,
                    query=query,
                    status=JobStatus.NEW,
                    post_date=datetime.combine(row["date_posted"], datetime.min.time()),
                )
                jobs_dict[key_id] = job
            except Exception as err:
                self.logger.error("Failed to convert row to Job because ", err.message)
                self.logger.error("Row: ", row)
        return jobs_dict

    @property
    def job_get_fields(self) -> List[JobField]:
        return [
            JobField.TITLE,
            JobField.COMPANY,
            JobField.DESCRIPTION,
            JobField.LOCATION,
            JobField.KEY_ID,
            JobField.TAGS,
            JobField.POST_DATE,
            # JobField.REMOTENESS,
            JobField.WAGE,
        ]

    @property
    def job_set_fields(self) -> str:
        """Call self.set(...) for the JobFields in this list when scraping a Job

        NOTE: Since this passes the Job we are updating, the order of this list
        matters if set fields rely on each-other.

        Override this as needed.
        """
        return [JobField.URL, JobField.REMOTENESS]

    @property
    def delayed_get_set_fields(self) -> List[JobField]:
        return [JobField.RAW]

    @property
    def headers(self) -> Dict[str, str]:
        """Session header for indeed.X"""
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, sdch",
            "accept-language": "en-GB,en-US;q=0.8,en;q=0.6",
            "upgrade-insecure-requests": "1",
            "user-agent": self.user_agent,
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }

    def get_job_soups_from_search_result_listings():
        return []

    def get():
        pass

    def set():
        pass
