from scrapy import Spider
from scrapy.http import FormRequest

from scrapy_splash import SplashRequest

from api.web_scraper.result_scraper.items import * # pylint: disable=unused-wildcard-import

class DlbSpider(Spider):

    # scrapy spider properties
    name = "dlb_spider"
    start_url = "https://www.dlb.lk/result/en"

    def start_requests(self):

        yield SplashRequest(self.start_url, self.parse,
                                endpoint="render.html",
                                args={'wait': 0.5}
                                )

    def parse(self, response):

        lottery_ids = [11, 1, -1, 2, 3, 8, 12, 9, 6]

        for i in range(len(lottery_ids)):
            
            # avoid scraping Niyatha Jaya results
            if(i == 2) : continue

            lottery_id = lottery_ids[i]
            result_id = response.css(
                "#resultID" + str(lottery_id) + "::attr(value)")

            # get results for each lottery via dlb api
            page_count = len(response.css(
                "#lottery" + str(i) + " .pagination a::text").extract()) - 2
            for x in range(page_count):
                page_id = x

                yield FormRequest(
                    "https://www.dlb.lk/result/pagination_re",
                    formdata={
                        "pageId": str(page_id),
                        "resultID": str(result_id),
                        "lotteryID": str(lottery_id),
                        "lastsegment": "en"
                    },
                    callback=self.__parse_page,
                    meta={
                        "lottery_id": str(lottery_id),
                        "page_no": str(page_id)
                    }
                )

    def __parse_page(self, response):
        lottery_id = response.meta.get("lottery_id")

        rows = response.css("tr")
        for row in rows:
            draw_no_date = row.css("td::text").get().split("  |  ")

            draw_no = draw_no_date[0]
            draw_date = draw_no_date[1]

            numbers = row.css(".res_number::text").extract()

            if (lottery_id == "2"):
                zodiac_sign = row.css("img::attr(src)").get()[
                    39:].split(".")[0]
                yield LotteryType2(lot_id=lottery_id, draw_no=draw_no, draw_date=draw_date, numbers=numbers, zodiac_sign=zodiac_sign)
            else:
                letter = row.css(".res_eng_letter::text").get()
                yield LotteryType3(lot_id=lottery_id, draw_no=draw_no, draw_date=draw_date, numbers=numbers, letter=letter)




# docker run -p 8050:8050 scrapinghub/splash     
