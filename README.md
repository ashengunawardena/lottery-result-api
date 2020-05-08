## Lottery Result API

### Overview

In Sri Lanka, lottery draws are held by [National Lotteries Board](https://nlb.lk) and [Development Lotteries Board](https://dlb.lk). The lottery results are published every night on the television channel [Rupavahini](http://www.rupavahini.lk/) and are published to their respective official websites thereafter. 

This application extracts lottery results published on the official websites of NLB and DLB, via web scraping using the [Scrapy](https://scrapy.org/) framework, and after saving them on a local NoSQL database, makes the results available for consumption via a publicily available REST API. Additionaly, this application provides the functionality of finding prizes for a given lottery via the REST API, and provides a JSON response containing winning lottery results and any prizes which have been won.

### API Endpoints

#### **GET** <code>/results?year={year}&month={month}&day={day}</code>

This endpoint is used to fetch all lottery results on a given date.

**Query Parameters,**

* ***year*** : The year of the date (numeric).
* ***month*** : The month of the date (numberic).
* ***day*** : The month of the date (numeric).

**Sample Usage,**

Request URL: <code>http://0.0.0.0:5000/results?year=2020&month=3&day=5</code>

JSON Response,

    {
        "dlb": [
            {
                "draw_number": "1653",
                "letter": "T",
                "lottery_id": "6",
                "numbers": [
                    "03",
                    "13",
                    "38",
                    "46"
                ]
            },
            {
                "draw_number": "2789",
                "lottery_id": "2",
                "numbers": [
                    "34",
                    "40",
                    "47",
                    "55"
                ],
                "zodiac_sign": "thula"
            }
        ],
        "nlb": [
            {
                "draw_number": "671",
                "lottery_id": "2",
                "numbers": [
                    "3",
                    "14",
                    "24",
                    "64"
                ],
                "zodiac_sign": "CAPRICORN"
            }
        ]   
    }

#### **POST** <code>/nlb</code>

This endpoint is used to find results and prizes for a nlb lottery.

**Form Data,**

* ***lottery_id*** : The ID of the lottery.
* ***draw_no*** : The draw number of the lottery.
* ***numbers*** : The number fields of the lottery.
* ***letter*** : The letter field of the lottery (optional).
* ***super_number*** : The super number field of the lottery (optional).
* ***zodiac_sign*** : The zodiac sign field of the lottery (optional).

**Sample Usage,**

Request URL: <code>http://0.0.0.0:5000/nlb</code>

Form Data,

![Supiri Vasana - Form Data](https://user-images.githubusercontent.com/58177462/81444479-d2708c00-9194-11ea-9715-1dbef23ff388.png)

JSON Response,

    {
        "bonus_numbers": [
            "5",
            "55"
        ],
        "draw": 1504,
        "draw_date": "15-02-2020",
        "id": 9,
        "is_type_nlb": true,
        "matches": {
            "bonus_numbers": [
                false,
                true
            ],
            "numbers": [
                0,
                1,
                2
            ],
            "super_number": false
        },
        "numbers": [
            "6",
            "13",
            "56",
            "61"
        ],
        "prize": "Rs. 50,000",
        "super_number": "8"
    }

#### **POST** <code>/dlb</code>

This endpoint is used to find results and prizes for a dlb lottery.

**Form Data,**

* ***lottery_id*** : The ID of the lottery.
* ***draw_no*** : The draw number of the lottery.
* ***numbers*** : The number fields of the lottery.
* ***letter*** : The letter field of the lottery (optional).
* ***fate_number*** : The fate number field of the lottery (optional).
* ***zodiac_sign*** : The zodiac sign field of the lottery (optional).

**Sample Usage,**

Request URL: <code>http://0.0.0.0:5000/dlb</code>

Form Data, 

![Development Fortune - Form Data](https://user-images.githubusercontent.com/58177462/81444470-d00e3200-9194-11ea-8ca2-648a52bad86e.png)

JSON Response,

    {
        "draw": 320,
        "draw_date": "05-02-2020",
        "fate_number": "09",
        "id": 9,
        "is_type_nlb": false,
        "letter": "E",
        "matches": {
            "fate_number": true,
            "letter": true,
            "numbers": [
            0,
            1,
            2
            ]
        },
        "numbers": [
            "02",
            "08",
            "63"
        ],
        "prize": "Rs. 10,000,000"
    }


### Technology Stack

#### Programming Languages

* Python - The language this API is built on.

#### Frameworks

* Scrapy - Used for web scraping of [NLB](https://nlb.lk) and [DLB](https://dlb.lk) websites.
* Flask - Used as the development WSGI server in which the REST API is hosted on.

#### External Libraries

* PyMongo - Used as the python driver for accessing the MongoDB database.

#### Database

* MongoDB - Used as the database to store scraped lottery data.

### Future Work

* Deploying of the application onto a production server.
* Integration of OAuth authorization framework into the application, for securing and authorizing the use of the API.

## THE END