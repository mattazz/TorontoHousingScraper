from typing import Iterable
import random
import scrapy
from ..utils import parser


class ZoloSpider(scrapy.Spider):
    name = "zolo_detailed"
    allowed_domains = ["zolo.ca"]

    def __init__(self, page_num=None, *args, **kwargs):
        super(ZoloSpider, self).__init__(*args, **kwargs)
        self.page_num = page_num  # Access the argument

    def start_requests(self):
        urls = parser.csv_to_list("links.csv")
        cookies = {
            "BID": "04431cd8-d662-11ee-92d1-bc764e102e1e",
            "BSID": "f949c591-d778-11ee-92d1-bc764e102e1e",
            "HREFR": "https%3A%2F%2Fwww.google.com%2F",
            "SOT": "2",
            "__cf_bm": "TbkMH10VvH0PrbWDNK0PanSamwUlN06pG04uNBhTrhE-1709263428-1.0-ASCVNcxJ3u+5Wb1tcYXnDVJUZ8lchAdJLUBtG+mo37aiGbYlSpcSQlO4F7ldvdY+yCEV5c+Q5fLloSSX/75maEs=",
            "__cfruid": "6034dc890e521219c885c8945716979cf8848fa5-1709262507",
            "_ga": "GA1.1.1166958093.1709142697",
            "_ga_SRQSX6WNCC": "GS1.1.1709262509.2.1.1709262583.0.0.0",
            "full-css": "true",
            "id-": "",
        }
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Referer": "https://www.zolo.ca/",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        }

        # proxies = [
        #     "http://45.181.123.201:999",
        #     "http://181.81.245.194:4128",
        #     "http://103.88.90.50:8080",
        #     "http://103.152.232.74:8181",
        #     "http://45.182.176.38:9947",
        #     "http://190.120.249.180:999",
        #     "http://103.141.180.254:80",
        #     "http://94.131.14.66:3128",
        #     "http://62.201.251.217:8585",
        # ]

        for url in urls:
            # proxy = random.choice(proxies)
            print("LAST SCRAPE: " + str(url))
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cookies=cookies,
                headers=headers,
                # meta={"proxy": proxy},
            )

    def parse(self, response):
        ## EXTRACT SCRIPT CODE###
        scripts = response.css("script::text").getall()
        script = scripts[1]
        ## This is a dict
        final_script_data = parser.parse_zolo_json(script)

        # Extracting the street address
        address = response.css("h1.address::text").get()  # done

        # Area divided into two elements [0] = city [1] = neighbourhood
        area = response.css(
            "section.listing-location div.area a.text-primary::text"
        ).getall()

        city = area[0]
        neighbourhood = area[1]
        province = response.css("span.province::text").get()

        # Extracting the price
        price_element = response.css("section.listing-price div::text").get()
        price = price_element.strip() if price_element else None

        # Extracting the bed, bath, sqft, and age details
        divs = response.css(
            "section.sm-mb3.sm-column-count-2.column-gap div.column-container.column-break-inside-avoid"
        )
        divGroup = divs.css("div.column")

        detailed_info = {}
        for div in divGroup:
            items = div.css("div")
            # Ex: Label = Sale
            for item in items:
                label = item.css("div.column-label::text").get()
                value = item.css("div.column-value span.priv::text").get()
                if label and value:
                    detailed_info[label] = value

        print(detailed_info)

        description = response.css(
            "div.section-listing-content-pad span.priv p::text"
        ).get()

        yield {
            "street_address": address.strip(),
            "city": city.strip(),
            "province": province.strip(),
            "neighbourhood": neighbourhood.strip(),
            "price": price.strip(),
            **detailed_info,
            "description": description.strip(),
            **final_script_data,
        }

        # # Find the next page URL

        # current_page_number = int(response.url.split("/")[-1].replace("page-", ""))
        # next_page_number = current_page_number + 1
        # next_page_url = (
        #     f"https://www.zolo.ca/toronto-real-estate/page-{next_page_number}"
        # )

        # # Check if the next page exists by ensuring it doesn't exceed a max page limit
        # # or by checking the presence of a 'Next' button or similar indicator (not shown here)
        # if next_page_number <= 10:  # Example max limit; adjust or remove as necessary
        #     yield scrapy.Request(url=next_page_url, callback=self.parse)
