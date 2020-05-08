from scrapy import Spider, Request
from api.web_scraper.result_scraper.items import * # pylint: disable=unused-wildcard-import

class NlbSpider(Spider) :

    def __init__(self) :

        # sort lotteries according to format

        lottery_type1 = ["mega"]
        lottery_type2 = ["neeroga"]
        lottery_type3 = ["mahajana", "jathika", "dhana", "vasana", "govisetha", "sevana"]
        lottery_type4 = ["supiri"]
        lottery_type5 = ["daru"]

        self.lottery_types = []
        self.lottery_types.append(lottery_type1)
        self.lottery_types.append(lottery_type2)
        self.lottery_types.append(lottery_type3)
        self.lottery_types.append(lottery_type4)
        self.lottery_types.append(lottery_type5)

    name = "nlb_spider"
    start_urls = [
        "https://nlb.lk/English/lotteries"
    ]

    def parse(self, response) :
        paths = response.css("br+ a").xpath("@href").extract()

        for path in paths :
            url = "https://www.nlb.lk/" + path
            yield Request(url, callback = self.__parse_type)

    # find type of lottery in response
    def __parse_type(self, response) :
        name = response.css("h1::text").get().split()[0].lower()
        
        type_no = 1
        lottery_id = 1
        stop = False
        for lottery_type in self.lottery_types :
            for lottery in lottery_type :
                if (lottery == name) :
                    if (type_no == 1) :
                        for lottery in self.__parse_lottery(response, LotteryType1(lot_id = lottery_id, lot_type = type_no)) :
                            yield lottery
                    elif (type_no == 2) :
                        for lottery in self.__parse_lottery(response, LotteryType2(lot_id = lottery_id, lot_type = type_no)) :
                            yield lottery
                    elif (type_no == 3) :
                        for lottery in self.__parse_lottery(response, LotteryType3(lot_id = lottery_id, lot_type = type_no)) :
                            yield lottery
                    elif (type_no == 4) :
                        for lottery in self.__parse_lottery(response, LotteryType4(lot_id = lottery_id, lot_type = type_no)) :
                            yield lottery
                    elif (type_no == 5) :
                        for lottery in self.__parse_lottery(response, LotteryType5(lot_id = lottery_id, lot_type = type_no)) :
                            yield lottery
                    
                    stop = True
                    break

                lottery_id += 1

            if(stop) : break
            type_no += 1
    
    # parse lottery according to type
    def __parse_lottery(self, response, lottery) :
        results = response.css("tbody tr")
        for result in results :
            lottery["draw_no"] = result.css("b::text").get()
            lottery["draw_date"] = result.css("td::text").get()
            lottery["numbers"] = result.css(".Yellow::text").extract() 
             
            if( isinstance(lottery, LotteryType1) ) :
                lottery["letter"] = result.css(".Blue::text").get()
                lottery["super_number"] = result.css(".Red::text").get()
            elif( isinstance(lottery, LotteryType2) ) :
                lottery["zodiac_sign"] = result.css(".Blue::text").get()
            elif( isinstance(lottery, LotteryType3) ) :
                lottery["letter"] = result.css(".Blue::text").get()
            elif( isinstance(lottery, LotteryType4) ) :
                lottery["super_bonus_numbers"] = result.css(".Red::text").extract() 
            elif( isinstance(lottery, LotteryType5) ) :
                lottery["letter"] = result.css(".Blue::text").get()
                lottery["special_numbers"] = result.css(".Red::text").extract()

            yield lottery




















    # def parse_lottery_type1(self, response, name) :
    #     lottery = LotteryType1()

    #     results = response.css("tbody tr")
    #     for result in results :
    #         lottery["name"] = name
    #         lottery["draw_no"] = result.css("b::text").get()
    #         lottery["draw_date"] = result.css("td::text").get()
    #         lottery["numbers"] = result.css(".Yellow::text").extract() 

    #         lottery["letter"] = result.css(".Blue::text").get()
    #         lottery["super_number"] = result.css(".Red::text").get()

    #         yield lottery

    # def parse_lottery_type2(self, response, name) :
    #     lottery = LotteryType2()

    #     results = response.css("tbody tr")
    #     for result in results :
    #         lottery["name"] = name
    #         lottery["draw_no"] = result.css("b::text").get()
    #         lottery["draw_date"] = result.css("td::text").get() 
    #         lottery["numbers"] = result.css(".Yellow::text").extract() 

    #         lottery["zodiac_sign"] = result.css(".Blue::text").get()

    #         yield lottery

    # def parse_lottery_type3(self, response, name) :
    #     lottery = LotteryType3()

    #     results = response.css("tbody tr")
    #     for result in results :
    #         lottery["name"] = name
    #         lottery["draw_no"] = result.css("b::text").get()
    #         lottery["draw_date"] = result.css("td::text").get()
    #         lottery["numbers"] = result.css(".Yellow::text").extract() 

    #         lottery["letter"] = result.css(".Blue::text").get()

    #         yield lottery

    # def parse_lottery_type4(self, response, name) :
    #     lottery = LotteryType4()

    #     results = response.css("tbody tr")
    #     for result in results :
    #         lottery["name"] = name
    #         lottery["draw_no"] = result.css("b::text").get()
    #         lottery["draw_date"] = result.css("td::text").get()
    #         lottery["numbers"] = result.css(".Yellow::text").extract() 

    #         lottery["super_bonus_numbers"] = result.css(".Red::text").extract() 

    #         yield lottery

    # def parse_lottery_type5(self, response, name) :
    #     lottery = LotteryType5()

    #     results = response.css("tbody tr")
    #     for result in results :
    #         lottery["name"] = name
    #         lottery["draw_no"] = result.css("b::text").get()
    #         lottery["draw_date"] = result.css("td::text").get()
    #         lottery["numbers"] = result.css(".Yellow::text").extract() 
            
    #         lottery["letter"] = result.css(".Blue::text").get()
    #         lottery["special_numbers"] = result.css(".Red::text").extract()

    #         yield lottery