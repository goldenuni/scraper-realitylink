from typing import Any
from urllib.parse import urljoin

import scrapy
import json

from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By


class RealtyLinkSpider(scrapy.Spider):
    name = "realtylink"
    start_urls = [
        "https://realtylink.org/en/properties~for-rent/",
    ]
    BASE_URL = "https://realtylink.org/en/properties~for-rent/"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome()

    def parse(
        self, response: scrapy.http.Response, **kwargs
    ) -> scrapy.Request:
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)

        yield from self._parse_page(selector)

        next_button = self.driver.find_element(By.CSS_SELECTOR, "li.next a")
        for _ in range(5):
            if next_button:
                next_button.click()
                selector = Selector(text=self.driver.page_source)
                yield from self._parse_page(selector)

    def _parse_page(
        self,
        response: Selector,
    ) -> scrapy.Request:
        urls = response.css("div.shell a.a-more-detail::attr('href')").getall()

        for url in urls:
            yield scrapy.Request(
                url=urljoin(self.BASE_URL, url), callback=self._parse_item
            )

    def _parse_item(self, response: scrapy.http.Response) -> dict:
        link_on_ad = response.url
        title = response.css("span[data-id='PageTitle']::text").get()
        full_address = (
            response.css("h2[itemprop='address']::text").get().strip()
        )
        region = full_address.split(",", 1)[-1].strip()
        description = response.css("div[itemprop='description']::text").get()
        description_stripped = (
            description.strip() if description else "No provided description"
        )
        price = response.css(
            "div.price[itemprop='offers'] meta[itemprop='price']::attr(content)"
        ).get()
        floor_area = response.css("div.carac-value span::text").get().strip()
        image_links = json.loads(
            response.css("div.thumbnail.last-child.first-child script::text")
            .get()
            .strip()
            .replace("window.MosaicPhotoUrls = ", "")
            .replace(";", "")
        )
        bedrooms = response.css("div.row.teaser div.cac::text").get()
        num_of_rooms = int(bedrooms.strip().split()[0]) if bedrooms else 1
        return {
            "link_on_add": link_on_ad,
            "title": title,
            "region": region,
            "full_address": full_address,
            "description": description_stripped,
            "price": price,
            "floor_area": floor_area,
            "image_links": image_links,
            "num_of_rooms": num_of_rooms,
        }

    def close(self, spider, reason):
        self.driver.quit()
