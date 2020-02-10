# -*- coding: utf-8 -*-
# import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tv_series.items import TvSeriesItem


class RrmjSpider(CrawlSpider):
    name = 'rrmj'
    allowed_domains = ['rrmj.cc']
    start_urls = ['https://www.rrmj.cc/meiju/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/meiju/\d+/'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'/meiju/index\d+.html'), follow=True)
    )

    def parse_item(self, response):
        item = TvSeriesItem()
        item['tv_title'] = response.xpath(
            '//div[contains(@class, "detail_name mb_none ")]/span/text()'
        ).get()
        item['tv_img'] = response.urljoin(response.xpath(
            '//div[@class="detail_img"]/img/@src'
        ).get())
        # 该网站没有score
        item['tv_score'] = response.xpath(
            '//div[contains(@class, "starpf")]//strong/text()'
        ).get()

        info_dict = {}
        info = response.xpath('//div[@class="dlall"]/div/dl')
        for dl in info:
            name = dl.xpath('./dt/text()').get()
            info_dict[name] = ' '.join(dl.xpath('./dd/a/text()').extract())
            if not info_dict[name]:
                info_dict[name] = dl.xpath('./dd/text()').get()
        item['tv_info'] = info_dict
        item['tv_plot'] = response.xpath('//div[@class="des_xy"]/text()').get()
        # print(item)
        return item
