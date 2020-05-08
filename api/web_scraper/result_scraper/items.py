# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# base class for lotteries with common properties
class Lottery(scrapy.Item) :

    lot_id = scrapy.Field()
    lot_type = scrapy.Field()
    draw_no = scrapy.Field()
    draw_date = scrapy.Field()
    numbers = scrapy.Field()

class LotteryType1(Lottery) :
    letter = scrapy.Field()
    super_number = scrapy.Field()

class LotteryType2(Lottery) :
    zodiac_sign = scrapy.Field()

class LotteryType3(Lottery) :
    letter = scrapy.Field()

class LotteryType4(Lottery) :
    super_bonus_numbers = scrapy.Field()

class LotteryType5(Lottery) :
    letter = scrapy.Field()
    special_numbers = scrapy.Field()

class LotteryType6(Lottery) :
    letter = scrapy.Field()
    fate_number = scrapy.Field()
