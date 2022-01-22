# -*- coding: utf-8 -*-
import scrapy


class AutosOffersSpider(scrapy.Spider):
    name = 'autos_offers'
    allowed_domains = ['autos.mercadolibre.com.ar']

    def start_requests(self):
        yield scrapy.Request(
            url='https://autos.mercadolibre.com.ar/chevrolet/40000-a-120000-km/bsas-gba-oeste/2009-2014/_Desde_97_PriceRange_350000ARS-650000ARS_NoIndex_True', 
            callback=self.parse,
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        )

    def parse(self, response):
        for item in response.xpath('//li[@class="ui-search-layout__item"]'):
            yield {
                'price': item.xpath('.//span[@class="price-tag-fraction"]/text()').get(),
                'year': item.xpath('.//li[@class="ui-search-card-attributes__attribute"][1]/text()').get(),
                'kilometers': item.xpath('.//li[@class="ui-search-card-attributes__attribute"][2]/text()').get()
            }

        next_page = response.xpath('//li[@class="andes-pagination__button"][1]/a/@href').get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)