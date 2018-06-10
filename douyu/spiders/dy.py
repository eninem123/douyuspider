# -*- coding: utf-8 -*-
import scrapy
import json

from douyu.items import DouyuItem


class DySpider(scrapy.Spider):
    name = 'dy'
    allowed_domains = ['douyucdn.cn']
    # start_urls = ['http://douyucdn.cn/']
    global base_url
    base_url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=100&offset="
    offset = 0
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        data_list = json.loads(response.body.decode())["data"]
        # if len(data_list) == 0:
        #     return
        if not data_list:
            return
        for data in data_list:
            item = DouyuItem()
            item["room_link"] = "http://www.douyu.com/" + data['room_id']
            item["image_link"] = data['vertical_src']
            item["nick_name"] = data['nickname']
            item["anchor_city"] = data['anchor_city']
            yield item

        self.offset += 100
        yield scrapy.Request(base_url + str(self.offset), callback=self.parse)
