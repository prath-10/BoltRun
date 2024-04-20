import os
import xmltodict
from raccoon_src.utils.request_handler import RequestHandler
from raccoon_src.utils.exceptions import RaccoonException, RequestHandlerException
from raccoon_src.utils.coloring import COLORED_COMBOS, COLOR
from raccoon_src.generate_html import generate  # Import the HTML generation function

# Set path for relative access to builtin files.
MY_PATH = os.path.abspath(os.path.dirname(__file__))
HTTP = "http://"
HTTPS = "https://"
BASE_S3_URL = "s3.amazonaws.com"

# Existing code from the file...


class StorageExplorer(AmazonS3Handler, GoogleStorageHandler, AzureStorageHandler):
    """
    Find and test privileges of target cloud storage and look for sensitive files in it.
    Can lead to finding .git/.DS_Store/etc files with tokens, passwords and more.
    """

    def __init__(self, host, logger):
        super().__init__(host, logger)
        self.host = host
        self.logger = logger  # Uses the logger from web_app module
        self.buckets_found = set()
        self.html_output = []  # List to store HTML output

    # Existing methods from the class...

    def _add_to_found_storage(self, storage_url):
        """
        Will first normalize the img src and then check if this bucket was discovered before
        If it is in storage_urls_found, the function returns
        Else, it send a GET for the original URL (normalized image src) and will look for "AmazonS3" in
        the "Server" response header.
        If found, will add to URL with the resource stripped

        :param storage_url: img src scraped from page
        """
        storage_url = self._normalize_url(storage_url)
        bucket = S3Bucket(storage_url)
        if bucket.url not in self.storage_urls_found:
            try:
                res = self.request_handler.send("GET", url=storage_url)
                if self._is_amazon_s3_bucket(res):
                    self.storage_urls_found.add(bucket.url)
                    self.s3_buckets.add(bucket)
                    self.html_output.append(f"Discovered S3 bucket: {bucket.url}")  # Add to HTML output
            except RequestHandlerException:
                # Cannot connect to storage, move on
                pass

    def run(self, soup):
        img_srcs = self._get_image_sources_from_html(soup)
        # First validation
        urls = {src for src in img_srcs if self._is_s3_url(src)}
        for url in urls:
            self._add_to_found_storage(url)
        if self.s3_buckets:
            self.logger.info("{} S3 buckets discovered. Testing for permissions".format(COLORED_COMBOS.NOTIFY))
            for bucket in self.s3_buckets:
                if bucket.no_scheme_url in self.storage_urls_found:
                    continue
                else:
                    self._test_s3_bucket_permissions(bucket)

            if self.num_files_found > 0:
                self.logger.info(
                    "{} Found {}{}{} sensitive files in S3 buckets. inspect web scan logs for more information.".format(
                        COLORED_COMBOS.GOOD, COLOR.GREEN, self.num_files_found, COLOR.RESET))
                self.html_output.append(f"Found {self.num_files_found} sensitive files in S3 buckets.")  # Add to HTML output
            elif any(b.vulnerable for b in self.s3_buckets):
                self.logger.info("{} No sensitive files found in target's cloud storage".format(COLORED_COMBOS.BAD))
            else:
                self.logger.info("{} Could not access target's cloud storage."
                                 " All permissions are set properly".format(COLORED_COMBOS.BAD))
            # After completion, generate HTML
            generate(self.html_output)
