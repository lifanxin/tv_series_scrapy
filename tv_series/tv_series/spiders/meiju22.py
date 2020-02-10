# -*- coding: utf-8 -*-
# import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tv_series.items import TvSeriesItem


class Meiju22CrawlSpider(CrawlSpider):
    name = 'meiju22'
    allowed_domains = ['meiju22.com']
    start_urls = ['https://www.meiju22.com/search.php?searchtype=5&tid=2']

    rules = (
        Rule(
            LinkExtractor(allow=r'/Meiju/M\d+.html'),
            callback='parse_item'
        ),
        Rule(
            LinkExtractor(allow=r'\?page=\d+&searchtype=5&tid=2'),
            follow=True
        )
    )

    def parse_item(self, response):
        item = TvSeriesItem()
        item['tv_title'] = response.xpath(
            '//dl[@class="content"]/dt/a/@title'
        ).get()
        item['tv_img'] = re.findall(
            r'url\((.*?)\)',
            response.xpath('//dl[@class="content"]/dt/a/@style').get()
        )[0]
        item['tv_score'] = response.xpath(
            '//dl[@class="content"]//div[@class="score"]//text()'
        ).get()

        info_dict = {}
        info = response.xpath('//dl[@class="content"]//ul/li')
        for li in info:
            name = li.xpath('./span[@class="text-muted"]/text()').get()
            info_dict[name] = ' '.join(li.xpath('./a/text()').extract())
            if not info_dict[name]:
                info_dict[name] = li.xpath('./text()').get()

        item['tv_info'] = info_dict
        item['tv_plot'] = response.xpath('//div[@class="plot"]/p/text()').get()

        links_list = []
        links = re.findall('var GvodUrls2 = "(.*?)"', response.body.decode())
        links = links[0].split('###') if len(links) > 0 else None
        if links:
            for link in links:
                links_list.append(link.split('$')[-1])
        item['tv_links'] = links_list
        return item
