import pymongo

from datetime import datetime


class Database:

    def __init__(self):
        self.__nlb_first_run = True
        self.__dlb_first_run = True

        self.__db_connect()

    def __db_connect(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["LotteryScanner"]

        self.nlb_col = db["nlb"]
        self.dlb_col = db["dlb"]

    # functions to insert lottery draws to collection

    def insert_nlb(self, lot_dict):
        if(self.__nlb_first_run):
            self.nlb_col.drop()
            self.__nlb_first_run = False

        self.nlb_col.insert_one(lot_dict)

    def insert_dlb(self, lot_dict):
        if(self.__dlb_first_run):
            self.dlb_col.drop()
            self.__dlb_first_run = False

        self.dlb_col.insert_one(lot_dict)

    # functions to get draw results from collections

    def get_nlb(self, lot_id, draw_no):
        query = {
            "lottery_id": lot_id,
            "draw_number": draw_no
        }

        return self.nlb_col.find_one(query, {"_id": 0, "lottery_id": 0, "draw_number": 0} )

    def get_dlb(self, lot_id, draw_no):
        query = {
            "lottery_id": lot_id,
            "draw_number": draw_no
        }

        return self.dlb_col.find_one(query, { "_id": 0, "lottery_id": 0, "draw_number": 0} )

    def get_results(self, year, month, day):
        query = {"draw_date": datetime(year, month, day)}

        results = {
            'nlb' : [],
            'dlb' : []
        }

        # results = {
        #     'nlb': [
        #         {
        #             "draw_number": "1011",
        #             "lottery_id": "2",
        #             "zodiac_sign" : "cancer",
        #             "number_1": "8",
        #             "number_2": "4",
        #             "number_3": "2",
        #             "number_4": "0"
        #         },
        #         {
        #             "draw_number": "2369",
        #             "letter": "Z",
        #             "lottery_id": "7",
        #             "number_1": "40",
        #             "number_2": "61",
        #             "number_3": "62",
        #             "number_4": "64"
        #         }
        #     ],
        #     'dlb': [
        #         {
        #             "draw_number": "1011",
        #             "lottery_id": "2",
        #             "number_1": "8",
        #             "number_2": "4",
        #             "number_3": "2",
        #             "number_4": "0",
        #             "zodiac_sign": "kanya"
        #         },
        #         {
        #             "draw_number": "2369",
        #             "letter": "Z",
        #             "lottery_id": "3",
        #             "number_1": "8",
        #             "number_2": "4",
        #             "number_3": "2",
        #             "number_4": "0",
        #             "number_5": "9",
        #             "number_6": "9"
        #         }
        #     ]
        # }

        filter = {
            "_id": 0,
            "draw_date": 0,
            "lottery_type": 0
        }

        for result in self.nlb_col.find(query, filter):
            result['numbers'] = []

            for i in range(1, 7) :
                number_key = "number_" + str(i)
                bonus_number_key = "bonus_number_" + str(i)
                special_number_key = "special_number_" + str(i)

                #add numbers to an array and remove single keys
                if(number_key in result) :
                    result['numbers'].append(result[number_key])
                    result.pop(number_key)
                
                #add bonus numbers to an array, if present, and remove single keys
                if(i < 3 and bonus_number_key in result) :
                    if not ('bonus_numbers' in result) :
                        result['bonus_numbers'] = []

                    result['bonus_numbers'].append(result[bonus_number_key])
                    result.pop(bonus_number_key)

                #add special numbers to an array, if present, and remove single keys
                if(i < 5 and special_number_key in result) :
                    if not ('special_numbers' in result) : 
                        result['special_numbers'] = []

                    result['special_numbers'].append(result[special_number_key])
                    result.pop(special_number_key)

            results['nlb'].append(result)


        for result in self.dlb_col.find(query, filter) :
            result['numbers'] = []

            for i in range(1, 5) :
                number_key = "number_" + str(i)

                #add numbers to an array and remove single keys
                if(number_key in result) :
                    result['numbers'].append(result[number_key])
                    result.pop(number_key)

            results['dlb'].append(result)

        return results


if __name__ == "__main__":
    db = Database()
    print("result")
    # print(db.get_nlb("3", "4119"))

    # for x in db.get_results() :
    #     print(x)
