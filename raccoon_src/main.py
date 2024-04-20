import time
import asyncio
import threading
import click
import os

from raccoon_src.generate_html import generate  # Import the generate function

from raccoon_src.utils.coloring import COLOR, COLORED_COMBOS
from raccoon_src.utils.exceptions import RaccoonException, HostHandlerException
from raccoon_src.utils.request_handler import RequestHandler
from raccoon_src.utils.logger import SystemOutLogger
from raccoon_src.utils.help_utils import HelpUtilities
from raccoon_src.lib.fuzzer import URLFuzzer
from raccoon_src.lib.host import Host
from raccoon_src.lib.scanner import Scanner, NmapScan, NmapVulnersScan, VulnersScanner
from raccoon_src.lib.sub_domain import SubDomainEnumerator
from raccoon_src.lib.dns_handler import DNSHandler
from raccoon_src.lib.waf import WAF
from raccoon_src.lib.tls import TLSHandler
from raccoon_src.lib.web_app import WebApplicationScanner

# Set path for relative access to builtin files.
MY_PATH = os.path.abspath(os.path.dirname(__file__))


def intro(logger):
    logger.info("""{}
______       _ _  ______            
| ___ \     | | | | ___ \           
| |_/ / ___ | | |_| |_/ /   _ _ __  
| ___ \/ _ \| | __|    / | | | '_ \ 
| |_/ / (_) | | |_| |\ \ |_| | | | |
\____/ \___/|_|\__\_| \_\__,_|_| |_|
                                   
{}

4841434b414c4c5448455448494e4753

https://github.com/evyatarmeged/Raccoon
-------------------------------------------------------------------
    """.format(COLOR.GRAY, COLOR.RESET))


@click.command()
@click.version_option("0.8.5")
@click.argument("target")
@click.option("-d", "--dns-records", default="A,MX,NS,CNAME,SOA,TXT",
              help="Comma separated DNS records to query. Defaults to: A,MX,NS,CNAME,SOA,TXT")
@click.option("--tor-routing", is_flag=True, help="Route HTTP traffic through Tor (uses port 9050)."
                                                  " Slows total runtime significantly")
@click.option("--proxy-list", help="Path to proxy list file that would be used for routing HTTP traffic."
                                   " A proxy from the list will be chosen at random for each request."
                                   " Slows total runtime")
@click.option("-c", "--cookies", help="Comma separated cookies to add to the requests. "
                                      "Should be in the form of key:value\n"
                                      "Example: PHPSESSID:12345,isMobile:false")
@click.option("--proxy", help="Proxy address to route HTTP traffic through. Slows total runtime")
@click.option("-w", "--wordlist", default=os.path.join(MY_PATH, "wordlists/fuzzlist"),
              help="Path to wordlist that would be used for URL fuzzing")
@click.option("-T", "--threads", default=25,
              help="Number of threads to use for URL Fuzzing/Subdomain enumeration. Default: 25")
@click.option("--ignored-response-codes", default="302,400,401,402,403,404,503,504",
              help="Comma separated list of HTTP status code to ignore for fuzzing."
                   " Defaults to: 302,400,401,402,403,404,503,504")
@click.option("--subdomain-list", default=os.path.join(MY_PATH, "wordlists/subdomains"),
              help="Path to subdomain list file that would be used for enumeration")
@click.option("-sc", "--scripts", is_flag=True, help="Run Nmap scan with -sC flag")
@click.option("-sv", "--services", is_flag=True, help="Run Nmap scan with -sV flag")
@click.option("-f", "--full-scan", is_flag=True, help="Run Nmap scan with both -sV and -sC")
@click.option("-p", "--port", help="Use this port range for Nmap scan instead of the default")
@click.option("--vulners-nmap-scan", is_flag=True, help="Perform an NmapVulners scan. "
                                                        "Runs instead of the regular Nmap scan and is longer.")
@click.option("--vulners-path", default=os.path.join(MY_PATH, "utils/misc/vulners.nse"),
              help="Path to the custom nmap_vulners.nse script."
                   "If not used, Raccoon uses the built-in script it ships with.")
@click.option("-fr", "--follow-redirects", is_flag=True, default=False,
              help="Follow redirects when fuzzing. Default: False (will not follow redirects)")
@click.option("--tls-port", default=443, help="Use this port for TLS queries. Default: 443")
@click.option("--skip-health-check", is_flag=True, help="Do not test for target host availability")
@click.option("--no-url-fuzzing", is_flag=True, help="Do not fuzz URLs")
@click.option("--no-sub-enum", is_flag=True, help="Do not bruteforce subdomains")
@click.option("--skip-nmap-scan", is_flag=True, help="Do not perform an Nmap scan")
@click.option("-o", "--outdir", default="raccoon_scan_results",
              help="Directory destination for scan output")
def main(target,
         tor_routing,
         proxy_list,
         proxy,
         cookies,
         dns_records,
         wordlist,
         threads,
         ignored_response_codes,
         subdomain_list,
         full_scan,
         scripts,
         services,
         port,
         vulners_nmap_scan,
         vulners_path,
