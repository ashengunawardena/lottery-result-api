## Lottery Result API

### Overview

In Sri Lanka, lottery draws are held by [National Lotteries Board](https://nlb.lk) and [Development Lotteries Board](https://dlb.lk). The lottery results are published every night on the television channel [Rupavahini](http://www.rupavahini.lk/) and are published to their respective official websites thereafter. 

This application extracts lottery results published on the official websites of NLB and DLB, via web scraping using the [Scrapy](https://scrapy.org/) framework, and after saving them on a local NoSQL database, makes the results available for consumption via a publicily available REST API. Additionaly, this application provides the functionality of finding prizes for a given lottery via the REST API, and provides a JSON response containing winning lottery results and any prizes which have been won.

### API Endpoints

#### GET ''' /results? '''

### Technology Stack

#### Programming Languages

* Python - The language this API is built on.

#### Frameworks

* Scrapy - Used for web scraping of NLB (https://nlb.lk) and DLB (https://dlb.lk) websites.
* Flask - Used as the development WSGI server in which the REST API is hosted on.

#### External Libraries

* PyMongo - Used as the python driver for accessing the MongoDB database.

#### Database

* MongoDB - Used as the database to store scraped lottery data.