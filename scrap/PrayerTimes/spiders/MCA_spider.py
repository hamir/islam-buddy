import scrapy
from PrayerTimes.items import PrayertimesItem

class PrayerSpider(scrapy.Spider):
    name = "PrayerTimes"
    start_urls = [
        'http://www.mcabayarea.org'
    ]

    def parse(self, response):
        prayerCSS='td.Prayer01::text'
        prayerTimeCSS='td.Prayer02::text'
        prayerTable=response.css('div.box-3.deepest.with-header')
        item = PrayertimesItem()
        #for idx, val in enumerate(prayerTable.css(prayerCSS).extract()):
        item['Prayer'] = prayerTable.css(prayerCSS).extract()
	item['IqamaTime'] = prayerTable.css(prayerTimeCSS).re(r'\d+:\d+')
        return item
