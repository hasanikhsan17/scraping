import scrapy

from ..items import TokopediaItem


class TokpedSpider(scrapy.Spider):
    name = 'tokped'
    allowed_domains = ['tokopedia.com']
    start_urls = ['https://www.tokopedia.com/search?st=product&q=macbook%20pro']
    number_page = 2

    def parse(self, response):
        all_item = response.css('div.css-1g20a2m')

        items = TokopediaItem()

        for item in all_item:
            name = item.css('.css-18c4yhp').css('::text').extract()
            price = item.css('.css-rhd610').css('::text').extract()
            image = item.css('.fade').css('::attr(src)').extract()

            items['name'] = name
            items['price'] = price
            items['image'] = image

            yield items

        # next_page = response.css('').get()
        # if next_page is not None :
        #     yield response.follow(next_page, callback=self.parse)

        next_page = 'https://www.tokopedia.com/search?page=' + str(self.number_page) + '&q=macbook%20pro&st=product'
        if self.number_page <= 5:
            self.number_page += 1
            yield response.follow(next_page, callback=self.parse)
