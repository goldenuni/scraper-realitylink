import scrapy
import json


class RealtyLinkSpider(scrapy.Spider):
    name = "realtylink"
    start_urls = [
        "https://realtylink.org/en/properties~for-rent/",
    ]

    def parse(
        self, response: scrapy.http.Response, **kwargs
    ) -> scrapy.Request:
        pass

    def _parse_page(
        self, response: scrapy.http.Response, **kwargs
    ) -> scrapy.Request:
        pass

    def _parse_item(self, response: scrapy.http.Response, **kwargs) -> dict:
        # TODO 1: Find the date published or updated
        # TODO 2: Add the link, which refer to the ad
        # link_on_ad = kwargs.get("href")
        title = response.css("span[data-id='PageTitle']::text").get()
        full_address = (
            response.css("h2[itemprop='address']::text").get().strip()
        )
        region = full_address.split(",", 1)[-1].strip()
        description = (
            response.css("div[itemprop='description']::text").get().strip()
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
            "title": title,
            "region": region,
            "full_address": full_address,
            "description": description,
            "price": price,
            "floor_area": floor_area,
            "image_links": image_links,
            "num_of_rooms": num_of_rooms,
        }
