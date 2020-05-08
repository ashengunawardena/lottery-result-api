# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

from api.database import Database

# get date in python 'datetime' format from scraped date
def get_formatted_date(date, lot_type):
    if(lot_type == 0):
        nlb_months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]

        date = date.replace(",", "").split()
        month = date[1]
        day = int(date[2])
        year = int(date[3])

        for i in range(12):
            if(month == nlb_months[i]):
                month = i + 1
    else:
        dlb_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        date = date.replace("-", " ").split()
        year = int(date[0])
        month = date[1]
        day = int(date[2])

        for i in range(12):
            if(month == dlb_months[i]):
                month = i + 1

    return datetime(year, month, day)

class NLBScraperPipeline(object):

    def __init__(self):
        self.db = Database()

    def process_item(self, item, spider):
        
        # if lottery is DLB or item content is empty, return item
        if((spider.name == "dlb_spider") or (len(item["numbers"]) == 0)):
            return item

        lot_id = str(item["lot_id"])
        draw_no = item["draw_no"]
        
        # if draw number has a leading '0', remove it
        if(draw_no[0] == "0") :
            draw_no = draw_no[1: ]

        draw_date = get_formatted_date(item["draw_date"], 0)

        numbers = item["numbers"]

        # if lotteries other than Mahajana Sampatha and Jathika Sampatha have numbers with leading '0', remove it
        if (lot_id != "3" and lot_id != "4") :
            for i in range(len(numbers)) :
                if(numbers[i][0] == "0") :
                    numbers[i] = numbers[i][1: ]

        lot_type = str(item["lot_type"])

        # insert lottery draw to database 
        if (lot_type == "1"):
            letter = item["letter"]
            super_number = item["super_number"]

            # if lottery number has a leading '0', remove it
            if(super_number[0] == "0") :
                super_number = super_number[1: ]

            lot_dict = {
                "lottery_id": lot_id,
                "lottery_type" : lot_type,
                "draw_number": draw_no,
                "draw_date": draw_date,
                "letter": letter,
                "super_number": super_number,
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

        elif (lot_type == "2"):
            zodiac_sign = item["zodiac_sign"]

            lot_dict = {
                "lottery_id": lot_id,
                "lottery_type" : lot_type,
                "draw_number": draw_no,
                "draw_date": draw_date,
                "zodiac_sign": zodiac_sign,
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

        elif (lot_type == "3"):
            letter = item["letter"]

            # Mahajana Sampatha and Jathika Sampatha
            if(lot_id == "3" or lot_id == "4"):
                lot_dict = {
                    "lottery_id": lot_id,
                    "lottery_type" : lot_type,
                    "draw_number": draw_no,
                    "draw_date": draw_date,
                    "letter": letter,
                    "number_1": numbers[0],
                    "number_2": numbers[1],
                    "number_3": numbers[2],
                    "number_4": numbers[3],
                    "number_5": numbers[4],
                    "number_6": numbers[5]
                }

            else:
                lot_dict = {
                    "lottery_id": lot_id,
                    "lottery_type" : lot_type,
                    "draw_number": draw_no,
                    "draw_date": draw_date,
                    "letter": letter,
                    "number_1": numbers[0],
                    "number_2": numbers[1],
                    "number_3": numbers[2],
                    "number_4": numbers[3]
                }

        elif (lot_type == "4"):
            super_bonus_numbers = item["super_bonus_numbers"]
            
            # if super or bonus numbers have a leading '0', remove it
            for i in range(3) :
                if(super_bonus_numbers[i][0] == "0") :
                    super_bonus_numbers[i] = super_bonus_numbers[i][1: ]

            super_number = super_bonus_numbers[0]
            bonus_number1 = super_bonus_numbers[1]
            bonus_number2 = super_bonus_numbers[2]

            lot_dict = {
                "lottery_id": lot_id,
                "lottery_type" : lot_type,
                "draw_number": draw_no,
                "draw_date": draw_date,
                "super_number": super_number,
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3],
                "bonus_number_1": bonus_number1,
                "bonus_number_2": bonus_number2
            }

        elif (lot_type == "5"):
            letter = item["letter"]
            special_numbers = item["special_numbers"]
            
            lot_dict = {
                "lottery_id": lot_id,
                "lottery_type" : lot_type,
                "draw_number": draw_no,
                "draw_date": draw_date,
                "letter": letter,
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3],
                "special_number_1": special_numbers[0],
                "special_number_2": special_numbers[1],
                "special_number_3": special_numbers[2],
                "special_number_4": special_numbers[3],
            }

        self.db.insert_nlb(lot_dict)

        return item


class DLBScraperPipeline(object):
    def __init__(self):
        self.db = Database()

    def process_item(self, item, spider):

        # if lottery is NLB, return item
        if (spider.name == "nlb_spider") :
            return item

        lot_id = item["lot_id"]
        draw_no = item["draw_no"]
        
        # if lottery is Development Fortune and draw number is less than 151, stop processing
        if (lot_id == "9" and draw_no < "151") :
            return item

        draw_date = get_formatted_date(item["draw_date"], 1)
        numbers = item["numbers"]

        # insert lottery draw to database 
        if (lot_id == "2"):
            zodiac_sign = item["zodiac_sign"]

            lot_dict = {
                "lottery_id": lot_id,
                "draw_number": draw_no,
                "draw_date": draw_date,
                "zodiac_sign": zodiac_sign,
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

        else:
            letter = item["letter"]
            
            # Development Fortune
            if (lot_id == "9"):
                lot_dict = {
                    "lottery_id": lot_id,
                    "draw_number": draw_no,
                    "draw_date": draw_date,
                    "letter": letter,
                    "number_1": numbers[0],
                    "number_2": numbers[1],
                    "number_3": numbers[2],
                    "fate_number": numbers[3]
                }
                
            else:
                lot_dict = {
                    "lottery_id": lot_id,
                    "draw_number": draw_no,
                    "draw_date": draw_date,
                    "letter": letter,
                    "number_1": numbers[0],
                    "number_2": numbers[1],
                    "number_3": numbers[2],
                    "number_4": numbers[3]
                }

        self.db.insert_dlb(lot_dict)

        return item
