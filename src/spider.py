import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

import re

class ScriptSpider(CrawlSpider):
    name = 'script_spider'
    start_urls = ['http://www.livesinabox.com/friends/scripts.shtml']
    rules = (Rule(LinkExtractor(allow=('season', )), callback='parse_script'), )

    def parse_script(self, response):
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
                    'line': re.sub(r"[\(\[].*?[\)\]]", "", lines[next]).strip()
                }
            elif lines[i].startswith('[Time Lapse') or lines[i].startswith('[Scene:'):
                # self.logger.info('===============================%s', lines[i])
                yield { 'break': True }
