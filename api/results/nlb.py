from api.database import Database


class NLBResults:

    def __init__(self, form):
        lot_id = form["lottery_id"]
        draw_no = form["draw_no"]
        numbers = form.getlist("numbers")

        draw_results = Database().get_nlb(lot_id, draw_no)

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
            'is_type_nlb': True,
            'numbers': [],
            'matches': {
                'numbers': []
            }
        }

        lot_type = draw_results["lottery_type"]

        if(lot_type == "1"):
            # Mega Power
            lottery = {
                "letter": form["letter"],
                "super_number": form["super_number"],
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

            self.__find_prizes_1(draw_results, lottery)

        # neeroga
        elif(lot_id == "2"):
            lottery = {
                "zodiac_sign": form["zodiac_sign"],
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

            prizes = ["Rs. 0", "Rs. 60", "Rs. 200", "Rs. 10,000",
                "Rs. 10,000,000", "Rs. 20", "Rs. 100", "Rs. 2,000", "Rs. 1,000,000"]

            self.__find_prizes_2(draw_results, lottery, prizes)

        # Mahajana Sampatha or Jathika Sampatha
        elif(lot_id == "3" or lot_id == "4"):
                lottery = {
                    "letter": form["letter"],
                    "number_1": numbers[0],
                    "number_2": numbers[1],
                    "number_3": numbers[2],
                    "number_4": numbers[3],
                    "number_5": numbers[4],
                    "number_6": numbers[5]
                }

                self.__find_prizes_3(draw_results, lottery)

        elif(lot_type == "3" or lot_type == "5"):

            lottery = {
                "letter": form["letter"],
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

            if(lot_id == "5"):
                # Dhana Nidhanaya
                prizes = ["Rs. 0", "Rs. 60", "Rs. 1,000", "Rs. 100,000",
                    "Rs. 80,000,000", "Rs. 20", "Rs. 100", "Rs. 3,000", "Rs. 1,000,000"]
            elif(lot_id == "6"):
                # Vasana Sampatha
                prizes = ["Rs. 0", "Rs. 60", "Rs. 500", "Rs. 100,000",
                    "Rs. 10,000,000", "Rs. 20", "Rs. 100", "Rs. 2,000", "Rs. 1,000,000"]
            elif(lot_id == "7"):
                # Govi Setha
                prizes = ["Rs. 0", "Rs. 40", "Rs. 1000", "Rs. 100,000",
                    "Rs. 60,000,000", "Rs. 20", "Rs. 100", "Rs. 2,000", "Rs. 1,000,000"]
            elif(lot_id == "8"):
                # Sevana
                prizes = ["Rs. 0", "Rs. 50", "Rs. 200", "Rs. 100,000",
                    "Rs. 14,000,000", "Rs. 20", "Rs. 100", "Rs. 1,000", "Rs. 1,000,000"]
            elif(lot_id == "10"):
                # Daru Diri Sampatha
                prizes = ["Rs. 0", "Rs. 40", "Rs. 500", "Rs. 50,000",
                "Rs. 5,000,000", "Rs. 20", "Rs. 100", "Rs. 1,000", "Rs. 1,000,000"]

            self.__find_prizes_2(draw_results, lottery, prizes)

        elif(lot_type == "4"):
            # Supiri Vasana
            lottery = {
                "super_number": form["super_number"],
                "number_1": numbers[0],
                "number_2": numbers[1],
                "number_3": numbers[2],
                "number_4": numbers[3]
            }

            self.__find_prizes_4(draw_results, lottery)

    def __find_prizes_1(self, draw_results, lottery):
        self.result_dict['matches']['letter'] = letter_match = draw_results["letter"] == lottery["letter"]

        # if super number has a leading '0', remove it
        if(lottery["super_number"][0] == "0") :
            lottery["super_number"] = lottery["super_number"][1: ]

        self.result_dict['matches']['super_number'] = super_num_match = draw_results["super_number"] == lottery["super_number"]

        self.result_dict['letter'] = draw_results["letter"] 
        self.result_dict['super_number'] = draw_results["super_number"]

        number_match = 0
        for x in range(1, 5):
            x_number = "number_" + str(x)
            lottery_number = lottery[x_number]
            
            # add each draw number to result dict
            self.result_dict['numbers'].append(draw_results[x_number])

            # if lottery number has a leading '0', remove it
            if(lottery_number[0] == "0") :
                lottery_number = lottery_number[1: ]

            for i in range(1, 5):
                i_number = "number_" + str(i)
                if(draw_results[i_number] == lottery_number):
                    
                    # add number to matches in result dict
                    self.result_dict['matches']['numbers'].append(i - 1)

                    number_match += 1
                    break

        prize = 0
        for x in reversed(range(1, 5)):
            if(number_match == x):
                if(x == 4):
                    if(letter_match and super_num_match):
                        prize = 9
                        break
                    elif(super_num_match):
                        prize = 4
                        break

                prize = (prize + 1) * \
                    x if letter_match else ((prize + 1) * x) + 4
                break

        if (prize == 0 and letter_match):
            prize = 5

        prizes = ["Rs. 0", "Rs. 40", "Rs. 500", "Rs. 100,000", "Rs. 10,000,000",
                  "Rs. 20", "Rs. 100", "Rs. 1,000", "Rs. 1,000,000", "Rs. 50,000,000"]

        self.result_dict['prize'] = prizes[prize]

    def __find_prizes_2(self, draw_results, lottery, prizes):

        # find if the letter or zodiac sign matches
        first_key = list(lottery)[0]
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

            # add each draw number to result dict
            self.result_dict['numbers'].append(draw_results[x_number])

            lottery_number = lottery[x_number]

            # if lottery number has a leading '0', remove it
            if(lottery_number[0] == "0") :
                lottery_number = lottery_number[1: ]

            for i in range(1, 5):
                i_number = "number_" + str(i)
                if(draw_results[i_number] == lottery_number):

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



    # fix error of two possibilities
    def __find_prizes_3(self, draw_results, lottery) :

        self.result_dict['letter'] = draw_results["letter"]

        # find if letter matches
        self.result_dict['matches']['letter'] = letter_match = draw_results["letter"] == lottery["letter"]

        # add each draw number to result dict
        for x in range(1, 7) :
            x_number = "number_" + str(x)
            self.result_dict['numbers'].append(draw_results[x_number])

        # finding count of matching last numbers
        last_numbers_match = 0
        for i in range(1, 7) :
            match = True
            for x in range(i, 7) :
                x_number = "number_" + str(x)
                if not (draw_results[x_number] == lottery[x_number]) :
                    match = False
                    break
                n = 7 - i
            
            if(match) :
                last_numbers_match = n
                break
                
        prize = 0

        # find first number matches if no last number matches were found
        if(last_numbers_match == 0) :
            first_numbers_match = 0
            for i in reversed(range(3, 7)) :
                match = True
                for x in reversed(range(1, i)) :
                    x_number = "number_" + str(x)
                    if not (draw_results[x_number] == lottery[x_number]) :
                        match = False
                        break
                    n = i - 1

                if(match) :
                    first_numbers_match = n
                    break

            # find prize if first numbers match
            if(first_numbers_match > 0) :
                for i in reversed(range(2, 6)) :
                    if(first_numbers_match == i) :
                        
                        # add number to matches in result dict
                        for y in range(1, 6) :
                            self.result_dict['matches']['numbers'].append(y - 1)

                        prize = i + 5
                        break

        # find prize if last numbers match
        else :
            for i in reversed(range(1, 7)) :
                if(last_numbers_match == i) :

                    # add matching numbers in result dict
                    for y in range((7 - i), 7) :
                        self.result_dict['matches']['numbers'].append(y - 1)

                    if(i == 6 and letter_match) :
                        prize = 11
                        break
                    prize = i
                    break

        if(prize == 0 and letter_match) :
            prize = 1 

        prizes = ["Rs. 0", "Rs. 20", "Rs. 50", "Rs. 1000", "Rs. 10,000", "Rs. 100,000", "Rs. 2,000,000", "Rs. 50", "Rs. 100", "Rs.1,000", "Rs.10,000", "Rs. 10,000,000"]

        self.result_dict['prize'] = prizes[prize]

    def __find_prizes_4(self, draw_results, lottery):
        
        # if super number has a leading '0', remove it
        if(lottery["super_number"][0] == "0") :
            lottery["super_number"] = lottery["super_number"][1: ]

        self.result_dict['super_number'] = draw_results['super_number']
        self.result_dict['bonus_numbers'] = [draw_results['bonus_number_1'], draw_results['bonus_number_2']]

        # find if super number matches
        self.result_dict['matches']['super_number'] = super_number_match = draw_results["super_number"] == lottery["super_number"]

        number_match = 0
        bonus_number_match = [False, False]

        # find count of matching numbers and matching bonus numbers
        for x in range(1, 5): 
            x_number = "number_" + str(x)

            # add each draw number to result dict
            self.result_dict['numbers'].append(draw_results[x_number])

            lottery_number = lottery[x_number]
            
            # if lottery number has a leading '0', remove it
            if(lottery_number[0] == "0") :
                lottery_number = lottery_number[1: ]

            # checking for matching numbers
            for i in range(1, 5):
                i_number = "number_" + str(i)
                if(lottery_number == draw_results[i_number]) :
                    
                    # add number to matches in result dict
                    self.result_dict['matches']['numbers'].append(i - 1)

                    number_match += 1
                    break
            
            # checking for matching bonus numbers
            for i in range(1, 3):
                if not bonus_number_match[i - 1] :
                    i_number = "bonus_number_" + str(i)
                    if(draw_results[i_number] == lottery_number) :
                        bonus_number_match[i - 1] = True
        
        self.result_dict['matches']['bonus_numbers'] = bonus_number_match

        # find prize for any winnings
        prize = 0
        for x in reversed(range(1, 5)):
            if(number_match == x):
                if(x == 4 and super_number_match) :
                    prize = 7
                    break
                    
                # if either of the bonus numbers match
                if(x == 3 and (bonus_number_match[0] or bonus_number_match[1])) :
                    prize = 1 if bonus_number_match[0] else 2

                else :
                    prize = ((prize + 1) * x) + 2
                    break

        # if no numbers or bonus numbers matched, check for super number
        if (prize == 0 and super_number_match) :
            prize = 3

        prizes = ["Rs. 0", "Rs. 100,000", "Rs. 50,000", "Rs. 20", "Rs. 100", "Rs. 2,000", "Rs. 1,000,000", "Rs.10,000,000"]

        self.result_dict['prize'] = prizes[prize]

    def get_result(self) :
        return self.result_dict
