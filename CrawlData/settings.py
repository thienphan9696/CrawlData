BOT_NAME = 'CrawlData'

SPIDER_MODULES = ['CrawlData.spiders']
NEWSPIDER_MODULE = 'CrawlData.spiders'

DEPTH_LIMIT = 10
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy.extensions.closespider.CloseSpider': 1
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

FEED_EXPORT_FIELDS=['link','id_pro']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'CrawlData (https://staging.thegioididong.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#Bỏ qua lệnh Retry
RETRY_ENABLED = False

#Đặt Delay Request (s)
DOWNLOAD_DELAY = 1

#Số request tối đa được xảy ra đồng thời, nếu không khai báo, mặc định sẽ là 8
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'