# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ImagesPipeline在目录  /usr/local/lib/python3.5/dist-packages/scrapy/pipelines/images.pyedi

from scrapy.pipelines.images import ImagesPipeline
import scrapy
from douyu.settings import IMAGES_STORE
import os
import logging


class DouyuImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # return [Request(x) for x in item.get(self.images_urls_field, [])]
        yield scrapy.Request(item['image_link'])

    #     if isinstance(item, dict) or self.images_result_field in item.fields:
    #         item[self.images_result_field] = [x for ok, x in results if ok]
    #    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22',results)
    '''
    22 results=[(True, {'url': 'https://rpic.douyucdn.cn/live-cover/appCovers/2018/06/07/3300407_20180607143339_big.jpg',
    'path': 'full/0c4d46d231c486364c9bb9dcd350900335018114.jpg', 'checksum': '431e687dc0321deca01cc3eacafb2bb5'})]

    '''

    def item_completed(self, results, item, info):
        # 原始路径IMAGES_STORE到data，后面的full开始
        source_path = IMAGES_STORE + [x["path"] for ok, x in results if ok][0]
        # 想新设置的路径
        item["image_path"] = IMAGES_STORE +'full/'+ item["nick_name"] + ".jpg"
        try:
            os.rename(source_path, item['image_path'])
            print('@@@@@@@@@@@@source_path', source_path)
            print('@@@@@@@@@@@@item', item['image_path'])
        except Exception as e:
            logging.error("Images%s rename failed" % source_path)
            print(e)
        return item

        # class DouyuPipeline(object):
        #     def process_item(self, item, spider):

        # return item
