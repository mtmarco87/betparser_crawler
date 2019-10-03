# -*- coding: utf-8 -*-

# Scrapy settings for bet_parser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
from pathlib import Path
from numpy import genfromtxt

BOT_PATH = str(Path(os.path.dirname(os.path.realpath(__file__))).parent)
BOT_NAME = 'bet_parser'
SPIDER_MODULES = ['bet_parser.spiders']
NEWSPIDER_MODULE = 'bet_parser.spiders'

# Splash config
SPLASH_URL = 'http://127.0.0.1:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# Selenium config
SELENIUM_DRIVER_CHROME = BOT_PATH + '/libs/selenium_drivers/chromedriver.exe'
SELENIUM_DRIVER_FIREFOX = BOT_PATH + '/libs/selenium_drivers/geckodriver.exe'

# Firebase config
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyBEL7WYzgT4UdvS4GaOtj_wKfnRDHQgxO4",
    "authDomain": "parser-b8114.firebaseapp.com",
    "databaseURL": "https://parser-b8114.firebaseio.com",
    "storageBucket": ""
}
FIREBASE_DEFAULT_DB_ROOT = 'parsed_bets'

# Machine Learning config
TEAM_NAMES = BOT_PATH + "/libs/ml_data/team_names.csv"
TEAM_NAMES_DATASET = genfromtxt(TEAM_NAMES, dtype=str, delimiter=',')    # Dataset for Team Names word similarity
TEAM_NAMES_DATASET_SOURCE = TEAM_NAMES_DATASET[:, 0]
TEAM_NAMES_DATASET_TARGET = TEAM_NAMES_DATASET[:, 1]
TEAM_NAMES_SANITIZE_ARRAY = [
    'fc', 'ac', 'ssc', 'cf', 'sc', 'rb'
]
TEAM_NAMES_VALIDATION_PATH = BOT_PATH + "/libs/ml_data"  # Output validation path (for training)
TEAM_NAMES_VALIDATION_FILE = 'to_validate'
SANITIZED_TEAM_NAMES_VALIDATION_FILE = None
ORIGINAL_TEAM_NAMES_VALIDATION_FILE = None

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bet_parser (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/77.0.3865.75 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    # 'bet_parser.middlewares.BetParserSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'bet_parser.middlewares.SeleniumDownloaderMiddleware': 900
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'bet_parser.pipelines.BetParserPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'