import scrapy

class ResmedSpider(scrapy.Spider):
    name = 'resmed'
    allowed_domains = ['www.resmed.com.au']
    start_urls = 'https://www.resmed.com.au/knowledge-hub'


    def start_requests(self):
        yield scrapy.http.Request(self.start_urls, callback=self.parse)


    def parse(self, response):
        links = response.css(".question-repeat ul li a::attr(href)").extract()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_answer_page,
                dont_filter=True,
            )


    def parse_answer_page(self, response):
        category=response.css(".brd-crm::text").extract_first()
        head = response.css('.section-right-heading h1::text').extract_first()
        sub_head = response.css('.section-right-sub-heading h3::text').extract_first()
        content = response.css('.section-content-rt p::text').extract()
        sub_con = response.css('.section-content-rt p a::text').extract_first()
        content_li = response.css('.section-content-rt ol li strong::text').extract()
        data = " ".join(content_li)
        ref = response.css('.section-content-rt ol li::text').extract()
        refrence = ' '.join(ref)
        completion = sub_head+ '\n' + "\n".join(content) + '\n' + sub_con +'\n' + data + '\n' + refrence
        product_dict = {
            'prompt': head,
            'completion': completion,
            'category': category
        }
        yield product_dict
