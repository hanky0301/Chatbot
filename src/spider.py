import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

import re
from unidecode import unidecode

class ScriptSpider(CrawlSpider):
    name = 'script_spider'
    # start_urls = ['http://www.livesinabox.com/friends/scripts.shtml']
    # rules = (Rule(LinkExtractor(allow=('season', )), callback='parse_friends'), )
    start_urls = ['https://bigbangtrans.wordpress.com/series-1-episode-1-pilot-episode/']
    rules = (Rule(LinkExtractor(allow=('episode', )), callback='parse_bigbang'), )

    def parse_friends(self, response):
        self.logger.info('Script link: \"%s\"', response.url)
        bold_text = response.selector.xpath('//b/text()').extract()
        roles = {name for name in bold_text if name[-1] == ':'}
        lines = [line.replace('\n', ' ') for line in response.xpath('//text()').extract()]
        for i in range(len(lines)):
            if lines[i] in roles:
                next = i + 1
                while lines[next] == ' ':
                    next += 1
                yield {
                    'role': lines[i], 
                    'line': unidecode(re.sub(r"[\(\[].*?[\)\]]", "", lines[next]).strip())
                }
            elif lines[i].startswith('[Time Lapse') or lines[i].startswith('[Scene:'):
                yield { 'break': True }

    def parse_bigbang(self, response):
        self.logger.info('Script link: \"%s\"', response.url)
        script = response.selector.xpath('//span/text()').extract()
        lines = [line.replace('\n', ' ') for line in response.xpath('//text()').extract()]
        for i in range(len(lines)):
            if lines[i] in roles:
                next = i + 1
                while lines[next] == ' ':
                    next += 1
                yield {
                    'role': lines[i], 
                    'line': re.sub(r"[\(\[].*?[\)\]]", "", lines[next]).strip()
                }
            elif lines[i].startswith('[Time Lapse') or lines[i].startswith('[Scene:'):
                self.logger.info('===============================%s', lines[i])
                yield { 'break': True }
