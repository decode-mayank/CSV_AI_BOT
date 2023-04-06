import time
import re

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Resmed(scrapy.Spider):
    name = "sec_resmed"
    start_urls = [
        "https://shop.resmed.com.au/",
    ]

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    def parse(self, response):
        links = response.css('.parent-menu::attr(href),.navPages-item:nth-child(7) a::attr(href)').getall()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_detail_page,
                dont_filter=True,
            )

    def parse_detail_page(self, response):
        self.driver.get(response.url)
        time.sleep(5)
        pagination = [response.url]
        while len(self.driver.find_elements(By.XPATH, '//a[contains(text(),"Next")]')) > 0:
            li = self.driver.find_element(By.XPATH,
                                          '//li[@class="pagination-item pagination-item--next"]/a').get_attribute(
                'href')
            dd = self.driver.find_element(By.XPATH, '//a[contains(text(),"Next")]')
            self.driver.execute_script("arguments[0].click();", dd)
            time.sleep(5)
            pagination.append(li)
        category = response.css('.page-heading::text').extract_first()

        for page in pagination:
            yield response.follow(
                page,
                callback=self.parse_info_page,
                meta={
                    'category': category,
                    'product_link': response.url,
                },
                dont_filter=True,
            )

    def parse_info_page(self, response):
        category = response.meta['category']
        products = response.css('.productCard')
        for product in products:
            urls = product.css('.card-body h3 a::attr(href)').extract()
            for url in urls:
                yield response.follow(
                    url,
                    callback=self.parse_product_page,
                    meta={
                        'category': category
                    },
                    dont_filter=True)

    def parse_product_page(self, response):
        category = response.meta['category']
        product = response.css('h1.productView-title::text').get()
        price = response.css('.productView-price .price--withTax::text').get()
        bc = response.css('.breadcrumb span::text').extract()
        breadcrumb = ' > '.join(bc)
        product_url = response.url
        money_back = response.css('article[class*="30-day"]').extract()
        meta_description = response.css(
            "article[class*=productView-description] p::text,article[class*=productView-description] strong::text").extract()
        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "div#trustpilotReviewsWidget iframe[title='Customer reviews powered by Trustpilot']")))
        try:
            rating = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                 "div.tp-widget-summary__information div.tp-widget-summary__rating > span.rating"))).text
        except:
            rating = 0
        try:
            reviews = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
            "div.tp-widget-summary__information div.tp-widget-summary__rating > span.tp-widget-summary__count > strong"))).text
        except:
            reviews = 0
        try:
            sku1 = response.css('.sku-label::text').get()
            sku2 = response.css('.productView-info-value::text').get()
            sku = sku1 + sku2
        except:
            sku = ''
        description = response.css('.custom-message-area p::text').get().replace('\n', '').replace('\r', '').strip()

        yield {
            'category': category,
            "sku": sku,
            "product": product,
            "description": f'{description}\n{"".join(meta_description) if len(meta_description) > 0 else ""}',
            "price": price.replace("$",""),
            "breadcrumb": breadcrumb,
            "product_url": product_url,
            "money_back": True if len(money_back) > 0 else False,
            "rating": rating,
            "total_reviews": reviews
        }

