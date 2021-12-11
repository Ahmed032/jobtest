import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import math

class LondonrelocationSpider(CrawlSpider):
    name = 'londonrelocation'
   # allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']


    rules = [
        Rule(LinkExtractor(allow=r'londonrelocation.com/our-properties-to-rent/properties/'), callback='parse', follow=False)
    ]

    def parse(self, response):
        item = {}
        row = response.css('div.row-flex')
        item["prop_link"] = row.css('h4').css('a::attr(href)').get()
        item["prop_name"] = row.css('h4').css('a::text').get()
        item["desc"] = row.css('div.contant.contant_limit').css('span::text').get()
        item["price"] = row.css('div.bottom-ic').css('h5::text').get()
        yield item
        current = None

        number_of_props = response.css('div.text-center.h2-space').css('h2::text').get()
        number_of_props = int(math.ceil(int(re.search(r"\d+", number_of_props)[0]) / 10))
        
        if "&pageset" not in response.url:
            url = response.url + "&pageset=2"
            current = 2
        else:
            if current < 3:         #would be number_of props normally
                current += 1
                url = response.url + "&pageset={}"
                yield(scrapy.Request(url=url,
                                    callback=self.parse))
        print("Page URL is {}".format(url))

        

        #url = response.url + "&pageset={}"
        #number_of_pages_available = response.css("div.pagination ul li a::attr(href)")[-1].get()

