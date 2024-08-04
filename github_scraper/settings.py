# -*- coding: utf-8 -*-

BOT_NAME = 'github_scraper'


SPIDER_MODULES = ['github_scraper.spiders']
NEWSPIDER_MODULE = 'github_scraper.spiders'

# User-Agent and headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 10  # 2 seconds delay


# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Retry middleware settings
RETRY_ENABLED = True
RETRY_TIMES = 10  # Adjust based on tolerance for rate limiting
RETRY_HTTP_CODES = [429, 500, 502, 503, 504, 522, 524, 408, 403]

# Download timeout
DOWNLOAD_TIMEOUT = 30

# Rotating user agents middleware
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
# }

# Configure item pipelines (if needed)
# ITEM_PIPELINES = {
#    'github_scraper.pipelines.SomePipeline': 300,
# }

# Logging configuration
# LOG_LEVEL = 'INFO'