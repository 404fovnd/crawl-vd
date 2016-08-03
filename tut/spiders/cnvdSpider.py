# -*- coding:utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
#from scrapy.spider.Spider.custom_settings
from scrapy.http.request import Request
from selenium import webdriver
from tut.items import cnvdItem

class cnvdSpider(Spider):
    name = 'cnvd'
    allowed_domains = ['cnvd.org.cn']
    start_urls = [
        #'http://www.cnvd.org.cn/flaw/list.htm',
        'http://www.cnvd.org.cn/flaw/list.htm?flag=true&max=20&offset=81600'
    ]
    custom_settings = {#不需要写middlewares
        'USER_AGENT':'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
    }

    baseurl = 'http://www.cnvd.org.cn'
    d = 1

    def start_requests(self):
        #cookie = None
        driver = webdriver.Firefox()
        #name = 'bdshare_firstime'
        #while (cookie is None):
        #    driver.get("http://www.cnvd.org.cn")
        #    cookie = driver.get_cookies(name) #始终报错：传入了两个参数，原因未知
        driver.set_window_size(0,0)
        driver.get('http://www.cnvd.org.cn')
        driver.refresh()


        cus_cookie = {}
        for cookie in driver.get_cookies():
            cus_cookie[cookie['name']] = cookie['value']

        driver.close()

        url = self.start_urls[0]
        yield Request(url, cookies = cus_cookie, callback = self.parse)

    def parse(self, response):
        #for sel in response.xpath('//tr/td[@width="45%"]'):
        '''for sel in response.xpath('//tr/td[1]'):
            vul_name = sel.xpath('a/@title').extract()
            vul_href = sel.xpath('a/@href').extract()
            print vul_name, vul_href
            '''
        sel = Selector(response)
        se = sel.xpath('//div[@id="flawList"]')
        #print se.extract()

        for s in se.xpath('.//tr'):
            #print s.extract()
            item = cnvdItem()
            item['title'] = s.xpath('./td[1]/a/@title').extract()[0]
            link = s.xpath('./td[1]/a/@href').extract()[0]
            item['cnvdid'] = link.split('/')[-1]
            #print item
            item['pub_date'] = s.xpath('./td[last()]/text()').extract()[0].strip()

            yield item

        if (self.d < 1):
            nextlink = sel.xpath("//a[@class='prevLink']/@href").extract()
            #print nextlink
            for l in nextlink:
                fulllink = self.baseurl + l
                print 'next page: %s' % fulllink
                self.d = self.d + 1
                yield Request(fulllink, callback = self.parse)
