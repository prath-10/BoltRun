
<h3>BoltRun<br>Redefining the future of reconnaissance!</h3>

<h4>What is BoltRun?</h4>
<p align="left">BoltRun is your go-to web application reconnaissance suite that's designed to simplify and streamline the reconnaissance process for penetration testers, and bug bounty hunters. BoltRun redefines how you gather critical information about your target web applications.

Traditional reconnaissance tools often fall short in terms of configurability and efficiency. BoltRun addresses these shortcomings and emerges as a excellent alternative to existing commercial tools.

BoltRun was created to address the limitations of traditional reconnaissance tools and provide a better alternative, even surpassing some commercial offerings. Whether you're a bug bounty hunter, a penetration tester, or a corporate security team, BoltRun is your go-to solution for automating and enhancing your information-gathering efforts.
</p>


### About BoltRun

BoltRun is not an ordinary reconnaissance suite; it's a game-changer! We've turbocharged the traditional workflow with groundbreaking features that is sure to ease your reconnaissance game. BoltRun redefines the art of reconnaissance with highly configurable scan engines, recon data continuous monitoring, etc.


🦾&nbsp;&nbsp; BoltRun has advanced reconnaissance capabilities, harnessing a range of open-source tools to deliver a comprehensive web application reconnaissance experience. With it's intuitive User Interface, it excels in subdomain discovery, pinpointing IP addresses and open ports, collecting endpoints, conducting directory and file fuzzing, and performing vulnerability scans. To summarize, it does end-to-end reconnaissance. 


### Workflow

<img src="">


### Features

* Reconnaissance:
  * Subdomain Discovery
  * IP and Open Ports Identification
  * Endpoints Discovery
  * Directory/Files fuzzing
  * Screenshot Gathering
  * Vulnerability Scan
    * Nuclei
    * Dalfox XSS Scanner
    * CRLFuzzer
  * WHOIS Identification
* OSINT Capabilities
  * Meta info Gathering
  * Employees Gathering
  * Email Address gathering
  * Google Dorking for sensitive info and urls
* Projects, create distinct project spaces, each tailored to a specific purpose, such as personal bug bounty hunting, or any other specialized recon task.
* Support for Subscans
* Recon Data visualization
* Recon Notes and Todos
* Identify Interesting Subdomains
* Custom GF patterns and custom Nuclei Templates
* Edit tool-related configuration files (Nuclei, Subfinder, Naabu, amass)
* Add external tools from Github/Go
* Find actionable insights such as Most Common Vulnerability, Most Common CVE ID, Most Vulnerable Target/Subdomain, etc.


### Scan Engine

```yaml
subdomain_discovery: {
  'uses_tools': [
    'subfinder',
    'ctfr',
    'sublist3r',
    'tlsx',
    'oneforall',
    'netlas'
  ],
  'enable_http_crawl': true,
  'threads': 30,
  'timeout': 5,
}
http_crawl: {}
port_scan: {
  'enable_http_crawl': true,
  'timeout': 5,
  # 'exclude_ports': [],
  # 'exclude_subdomains': true,
  'ports': ['top-100'],
  'rate_limit': 150,
  'threads': 30,
  'passive': false,
  # 'use_naabu_config': false,
  # 'enable_nmap': true,
  # 'nmap_cmd': '',
  # 'nmap_script': '',
  # 'nmap_script_args': ''
}
osint: {
  'discover': [
      'emails',
      'metainfo',
      'employees'
    ],
  'dorks': [
    'login_pages',
    'admin_panels',
    'dashboard_pages',
    'stackoverflow',
    'social_media',
    'project_management',
    'code_sharing',
    'config_files',
    'jenkins',
    'wordpress_files',
    'php_error',
    'exposed_documents',
    'db_files',
    'git_exposed'
  ],
  'custom_dorks': [
    {
      'lookup_site': 'google.com',
      'lookup_keywords': '/home/'
    },
    {
      'lookup_site': '_target_',
      'lookup_extensions': 'jpg,png'
    }
  ],
  'intensity': 'normal',
  'documents_limit': 50
}
dir_file_fuzz: {
  'auto_calibration': true,
  'enable_http_crawl': true,
  'rate_limit': 150,
  'extensions': ['html', 'php','git','yaml','conf','cnf','config','gz','env','log','db','mysql','bak','asp','aspx','txt','conf','sql','json','yml','pdf'],
  'follow_redirect': false,
  'max_time': 0,
  'match_http_status': [200, 204],
  'recursive_level': 2,
  'stop_on_error': false,
  'timeout': 5,
  'threads': 30,
  'wordlist_name': 'dicc'
}
fetch_url: {
  'uses_tools': [
    'gospider',
    'hakrawler',
    'waybackurls',
    'gospider',
    'katana'
  ],
  'remove_duplicate_endpoints': true,
  'duplicate_fields': [
    'content_length',
    'page_title'
  ],
  'enable_http_crawl': true,
  'gf_patterns': ['debug_logic', 'idor', 'interestingEXT', 'interestingparams', 'interestingsubs', 'lfi', 'rce', 'redirect', 'sqli', 'ssrf', 'ssti', 'xss'],
  'ignore_file_extensions': ['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mpeg', 'mp3']
  # 'exclude_subdomains': true
}
vulnerability_scan: {
  'run_nuclei': false,
  'run_dalfox': false,
  'run_crlfuzz': false,
  'run_s3scanner': true,
  'enable_http_crawl': true,
  'concurrency': 50,
  'intensity': 'normal',
  'rate_limit': 150,
  'retries': 1,
  'timeout': 5,
  'fetch_gpt_report': true,
  'nuclei': {
    'use_nuclei_config': false,
    'severities': [
      'unknown',
      'info',
      'low',
      'medium',
      'high',
      'critical'
    ],
    # 'tags': [],
    # 'templates': [],
    # 'custom_templates': [],
  },
  's3scanner': {
    'threads': 100,
    'providers': [
      'aws',
      'gcp',
      'digitalocean',
      'dreamhost',
      'linode'
    ]
  }
}
waf_detection: {}
screenshot: {
  'enable_http_crawl': true,
  'intensity': 'normal',
  'timeout': 10,
  'threads': 40
}

# custom_header: "Cookie: Test"
```


### Quick Installation

**Note:** Only Ubuntu/VPS

1. Clone this repo

    ```bash
    git clone https://github.com/prath-10/BoltRun.git && cd BoltRun
    ```

1. Edit the dotenv file, **please make sure to change the password for postgresql `POSTGRES_PASSWORD`!**

    ```bash
    nano .env
    ```

1. In the dotenv file, you may also modify the Scaling Configurations

    ```bash
    MAX_CONCURRENCY=80
    MIN_CONCURRENCY=10
    ```

    MAX_CONCURRENCY: This parameter specifies the maximum number of BoltRun's concurrent Celery worker processes that can be spawned. In this case, it's set to 80, meaning that the application can utilize up to 80 concurrent worker processes to execute tasks concurrently. This is useful for handling a high volume of scans or when you want to scale up processing power during periods of high demand. If you have more CPU cores, you will need to increase this for maximised performance.

    MIN_CONCURRENCY: On the other hand, MIN_CONCURRENCY specifies the minimum number of concurrent worker processes that should be maintained, even during periods of lower demand. In this example, it's set to 10, which means that even when there are fewer tasks to process, at least 10 worker processes will be kept running. This helps ensure that the application can respond promptly to incoming tasks without the overhead of repeatedly starting and stopping worker processes.

    These settings allow for dynamic scaling of Celery workers, ensuring that the application efficiently manages its workload by adjusting the number of concurrent workers based on the workload's size and complexity

1. Run the installation script, Please keep an eye for any prompt, you will also be asked for username and password for BoltRun.

    ```bash
    sudo ./install.sh
    ```

    If `install.sh` does not have install permission, please change it, `chmod +x install.sh`

**BoltRun can now be accessed from <https://127.0.0.1>

**Unless you are on development branch, please do not access BoltRun via any ports**
