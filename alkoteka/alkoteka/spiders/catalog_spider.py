import scrapy
from alkoteka.config import settings
from scrapy.http import Response

CITY_UUID = settings.city_uuid
API_BASE_URL = "https://alkoteka.com/web-api/v1/product"


class AlkotekaSpider(scrapy.Spider):
    name = "alkoteka"

    async def start(self):
        urls = []
        for url in settings.start_urls:
            category = url.split("/")[-1]
            urls.append(
                f"{API_BASE_URL}?city_uuid={CITY_UUID}&page=1&per_page=20&root_category_slug={category}"
            )
            
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self._parse,
            )

    def _parse(self, response: Response):        
        json_response = response.json()
        
        per_page = json_response["meta"]["per_page"]
        current_page = json_response["meta"]["current_page"]
        
        remained = json_response["meta"]["total"] - per_page * current_page
        
        if remained > 0:
            category = response.url.split("&")[-1].split("=")[-1]
            url = (
                f"{API_BASE_URL}"
                f"?city_uuid={CITY_UUID}"
                f"&page={current_page + 1}&per_page={per_page}"
                f"&root_category_slug={category}"
            )
            yield scrapy.Request(
                url=url,
                callback=self._parse,
            )

        for product in json_response["results"]:
            product_url = product["product_url"]
            detail_url = (
                f"https://alkoteka.com/web-api/v1/product/" 
                f"{product_url.split('/')[-1]}"
                f"?city_uuid={CITY_UUID}"
            )

            request = scrapy.Request(
                url=detail_url,
                callback=self._parse_product,
            )
            request.cb_kwargs['product_catalog'] = product
            yield request

    def _parse_product(self, response: Response, product_catalog):
        product = response.json()
        full_product = {
            "product_catalog": product_catalog,
            "product": product
        }
        yield full_product