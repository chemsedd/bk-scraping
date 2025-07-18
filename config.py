URL = "https://www.booking.com/searchresults.html?ss=Paris%2C+France&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaE2IAQGYATG4ARjIAQ_YAQHoAQH4AQKIAgGoAgS4ArX548MGwAIB0gIkYzFiYjVjNWUtZTNiOC00YmUxLTlmNDAtZmRkOWMxMTAyY2Jm2AIF4AIB&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=-1456928&dest_type=city&group_adults=2&no_rooms=1&group_children=0"

# Settings for the spider
SPIDER_SETTINGS = {
    "USER_AGENT": "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "ROBOTSTXT_OBEY": False,
    "DOWNLOAD_DELAY": 0,
    "CONCURRENT_REQUESTS": 1,
    "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
    "COOKIES_ENABLED": True,
    "TELNETCONSOLE_ENABLED": False,
    "LOG_LEVEL": "INFO",
}
