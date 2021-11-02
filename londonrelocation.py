import scrapy
import json
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin


class LondonrelocationSpider(scrapy.Spider):

    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com/properties-to-rent/','londonrelocation.com','londonrelocation.com/our-properties-to-rent/properties/']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)
        rules=(
         Rule(LinkExtractor(allow=['properties-to-rent','our-properties-to-rent/properties/?keyword='],deny=['mailto','about-london-relocation']),callback='parse_area_pages'),
    )

    def parse_area_pages(self, response):
          yield{
            "Title":response.css('div.h4-space a::text').get().strip(),
           # 'Link':urljoin(self.start_urls,response.css('div.h4-space a').attrib['href']),
              "Price":response.css('div.bottom-ic h5::text').get(),
                

        }