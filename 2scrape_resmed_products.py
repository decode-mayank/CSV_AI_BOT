import scrapy
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path
                                      
class Resmed(scrapy.Spider):
    name = "resmed"
    start_urls = [
        "https://shop.resmed.com.au/",
    ]
   

    def parse(self,response):
        links = response.css('.parent-menu::attr(href),.navPages-item:nth-child(8) a::attr(href)').getall()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_detail_page,
                dont_filter=True,   
            )
    
    def parse_detail_page(self,response):
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(response.url)
            time.sleep(5)
            pagination = [response.url]
            while len(driver.find_elements(By.XPATH,'//a[contains(text(),"Next")]'))>0:
                li = driver.find_element(By.XPATH,'//li[@class="pagination-item pagination-item--next"]/a').get_attribute('href')
                dd = driver.find_element(By.XPATH,'//a[contains(text(),"Next")]')
                driver.execute_script("arguments[0].click();", dd)
                time.sleep(5)
                pagination.append(li)                
            type = response.css('.page-heading::text').extract_first()
           
            for page in pagination:
                yield response.follow(
                    page,
                    callback=self.parse_info_page,
                    meta = {
                        'type':type,
                        'product_link':response.url, 
                    },
                    dont_filter=True,   
                )

    def parse_info_page(self,response):
        type = response.meta['type']
        products = response.css('.productCard')
        completion = []
        for product in products:
            device  = product.css('.card-body h3 a::text').get()
            price = product.css('.card-body  span.price.price--withTax::text').get()
            device_url = product.css('.card-body h3 a::attr(href)').get()
            com = [device,price,device_url]
            completion.append(com)

        yield{
            'prompt':type,
            'completion':completion
        }

