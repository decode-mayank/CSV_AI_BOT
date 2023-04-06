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
        try:
            head = response.css('.section-right-heading h1::text').extract_first()
            sub_head = response.css('.section-right-sub-heading h3::text').extract_first()
            sub_heading = sub_head if sub_head is not None else ''
            content_p = response.css(
                '.section-content-rt p::text, .section-content-rt ul li::text, .section-content-rt p a::text, .section-content-rt ol li strong::text, .section-content-rt p strong::text, .section-content-rt p strong span::text, .section-content-rt ol li::text, .section-content-rt p a::attr(href),'
                ' .section-content-rt ol li span::text, .section-content-rt ol li a::text, .section-content-rt ol li a::attr(href), .section-content-rt p em::text, .section-content-rt li strong::text, .section-content-rt li h4::text, .section-content-rt h4::text, .section-content-rt h3::text, .section-content-rt ul li a::text, .section-content-rt ul li a::attr(href), .section-content-rt span::text, .section-content-rt span::text, .section-content-rt a::text, .section-content-rt a::attr(href)').extract()
            content = "\n".join(content_p) if content_p != [] else ''
            completion = sub_heading+ '\n' + content
            product_dict = {
                'type': response.css('.brd-crm::text').extract_first(),
                'prompt': head,
                'completion': completion,
                'url': response.url
            }
            yield product_dict
        except:
            pass
