from api.database import Database

class DLBResults:

    def __init__(self, form):
        lot_id = form["lottery_id"]
        draw_no = form["draw_no"]
        numbers = form.getlist("numbers")

        # getting results for draw
        draw_results = Database().get_dlb(lot_id, draw_no)

        raw_draw_date = draw_results['draw_date']
        draw_day = raw_draw_date.strftime("%d")
        draw_month = raw_draw_date.strftime("%m")
        draw_year = raw_draw_date.strftime("%Y")
        draw_date = draw_day + "-" + draw_month + "-" + draw_year

        # instance variable to store result
        self.result_dict = {
            'id': int(lot_id),
            'draw': int(draw_no),
            'draw_date': draw_date,
            'is_type_nlb': False,
            'numbers': [],
            'matches': {
                'numbers': []
            }
        }

        # getting lottery data from sent post data
        if (lot_id == "2"):
            lottery = {
                "zodiac_sign": form["zodiac_sign"],
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

        elif (lot_id == "9"):
            lottery = {
                "letter": form["letter"],
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "fate_number": form["fate_number"]
            }

        else:
            lottery = {
                "letter": form["letter"],
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

        # finding results for given lottery
        if(lot_id == "9"):
            # Development Fortune
            self.__find_prizes_1(draw_results, lottery)
        else:
            if(lot_id == "1"):
                # Saturday Fortune
                prizes = ["Rs. 0", "Rs. 60", "Rs. 1,000", "Rs. 100,000",
                          "Rs. 30,000,000", "Rs. 20", "Rs. 100", "Rs. 2,000", "Rs. 1,000,000"]
            elif(lot_id == "2"):
                # Lagna Wasana
                prizes = ["Rs. 0", "Rs. 60", "Rs. 200", "Rs. 10,000", "Rs. 2,000,000",
                          "Rs. 20", "Rs. 100", "Rs. 1,000", "Rs. 500,000"]
            elif(lot_id == "3"):
                # Super Ball
                prizes = ["Rs. 0", "Rs. 40", "Rs. 1,000", "Rs. 100,000",
                          "Rs. 50,000,000", "Rs. 20", "Rs. 100", "Rs. 2,000", "Rs. 1,000,000"]
            elif(lot_id == "6"):
                # Jayoda
                prizes = ["Rs. 0", "Rs. 40", "Rs. 1,000", "Rs. 50,000", "Rs. 20,000,000",
                          "Rs. 20", "Rs. 100", "Rs. 2,000", "Rs. 1,000,000"]
            elif(lot_id == "8" or lot_id == "12"):
                # Kotipathi Shanida & Kotipathi Kapruka
                prizes = ["Rs. 0", "Rs. 60", "Rs. 1,000", "Rs. 100,000",
                          "Rs. 75,000,000", "Rs. 20", "Rs. 100", "Rs. 2,000", "Rs. 1,000,000"]
            elif(lot_id == "11"):
                # Ada Kotipathi
                prizes = ["Rs. 0", "Rs. 40", "Rs. 1,000", "Rs. 100,000",
                          "Rs. 50,000,000", "Rs. 20", "Rs. 100", "Rs. 1,000", "Rs. 1,000,000"]

            self.__find_prizes_2(draw_results, lottery, prizes)     

    def __find_prizes_1(self, draw_results, lottery):
        
        self.result_dict["letter"] = draw_results['letter']
        self.result_dict["fate_number"] = draw_results['fate_number']

        # find if letter and/or fate number matches and assign match status to result dict
        self.result_dict['matches']['letter'] = letter_match = draw_results["letter"] == lottery["letter"]
        self.result_dict['matches']['fate_number'] = fate_num_match = draw_results["fate_number"] == lottery["fate_number"]

        # find count of matching numbers
        number_match = 0
        for x in range(1, 4): 
            x_number = "number_" + str(x)

            # add each draw number to result dict
            self.result_dict['numbers'].append(draw_results[x_number])

            for i in range(1, 4):
                i_number = "number_" + str(i)
                if(draw_results[i_number] == lottery[x_number]):

                    # add number to matches in result dict
                    self.result_dict['matches']['numbers'].append(i - 1)

                    number_match += 1
                    break
        
        # find prize for any winnings
        prize = 0
        for x in reversed(range(1, 4)):
            if(number_match == x):
                if(letter_match and fate_num_match):
                    prize = (prize + 1) * x
                    break
                elif(letter_match or fate_num_match):
                    prize = ((prize + 1) * x) + \
                        3 if letter_match else ((prize + 1) * x) + 6
                    break

                prize = ((prize + 1) * x) + 9
                break

        # if no numbers matched, check for letter or fate number
        if (prize == 0 and (letter_match or fate_num_match)):
            prize = 10

        prizes = ["Rs. 0", "Rs. 200", "Rs. 10,000", "Rs. 10,000,000", "Rs. 100", "Rs. 500",
                  "Rs. 100,000", "Rs. 100", "Rs. 500", "Rs. 500,000", "Rs. 20", "Rs. 100", "Rs. 50,000"]

        self.result_dict['prize'] = prizes[prize]

    def __find_prizes_2(self, draw_results, lottery, prizes):
        
        # find if the letter or zodiac sign matches
        first_key = list(draw_results)[1]
        first_match = draw_results[first_key] == lottery[first_key]
        
        if (len(draw_results[first_key]) > 1) : 
            self.result_dict['zodiac'] = draw_results[first_key]
            self.result_dict['matches']['zodiac'] = first_match
        else :
            self.result_dict['letter'] = draw_results[first_key]
            self.result_dict['matches']['letter'] = first_match

        # find count of matching numbers
        number_match = 0
        for x in range(1, 5):
            x_number = "number_" + str(x)
            
            # adding draw numbers to result dict
            self.result_dict['numbers'].append(draw_results[x_number])
            
            for i in range(1, 5):
                i_number = "number_" + str(i)
                if(draw_results[i_number] == lottery[x_number]):

                    # add number to matches in result dict
                    self.result_dict['matches']['numbers'].append(i - 1)

                    number_match += 1
                    break
        
        # find prize for any winnings
        prize = 0
        for x in reversed(range(1, 5)):
            if(number_match == x):
                prize = (prize + 1) * \
                    x if first_match else ((prize + 1) * x) + 4
                break
        if (prize == 0 and first_match):
            prize = 5

        self.result_dict['prize'] = prizes[prize]

    def get_result(self) :
        return self.result_dict