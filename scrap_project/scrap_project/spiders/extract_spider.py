import scrapy
from ..items import ScrapProjectItem


class name_spider(scrapy.Spider):
    name = 'sites'
    start_urls = [
        'https://talentedge.com/iit-delhi/operations-management-and-analytics-course',
        'https://talentedge.com/xlri-jamshedpur/financial-management-course',
        'https://talentedge.com/xlri-jamshedpur/human-resource-management-course',
        'https://talentedge.com/iim-kozhikode/professional-certificate-program-marketing-sales-management-iim-kozhikode',
        'https://talentedge.com/iim-kozhikode/professional-certificate-programme-in-hr-management-and-analytics'
    ]

    def parse(self, response, **kwargs):

        items = ScrapProjectItem()

        title = response.xpath("//title/text()").extract()
        description = response.xpath("//div[@class = 'pl-aboutus']").xpath("//div[@class = 'desc']//p/text()").extract()
        key_skills = response.xpath("//div[@class = 'key-skills-sec']//ul//li/text()").extract()
        prerequisites = response.xpath("//h4//div[@class = 'eligible-right-top-list']//ul//li/text() | //div[@class = "
                                       "'eligible-right-top-list']//ul//li/text() | //div[@class = "
                                       "'eligible-right-top-list']//p/text()").extract()

        content_texts = []
        for k in range(1, 26):
            content_syllabus = response.xpath("//div[@id = 'dsyllabus']//div[@class='col-12 d-md-none']//div["
                                              "@id='headinggl-" + str(k) + "']//h2//button/text() | //div[@id = "
                                                                           "'dsyllabus']//div[@class='col-12 "
                                                                           "d-md-none']//div[@id='collapsegl-" + str(
                k) + "']//ul//li/text() | //div[@id = 'dsyllabus']//div[@class='col-12 d-md-none']//div[@id "
                     "='collapsegl-" + str(k) +"']//div[@class = 'card-body ul-desc']//p/text()").extract()

            content_texts.append([content_syllabus])

        site_content = [x for x in content_texts if x != [[]]]
        syllabus_content = [z for y in site_content for z in y]

        syllabus_contents = []
        for i in syllabus_content:
            out = []
            for j in i:
                j = j.strip()
                out.append(j)
            syllabus_contents.append(out)

        syllabus_heading = []
        syllabus_list = []
        for i in syllabus_contents:
            syllabus_heading.append(i[0])
            syllabus_list.append(i[1:])

        syllabus = dict(zip(syllabus_heading, syllabus_list))

        price = response.xpath("//div[@class='program-details-total-pay-amt d-flex align-items-center "
                               "justify-content-between ruppes']//div[@class = "
                               "'program-details-total-pay-amt-right']/text()").extract_first()
        price_new = ' '.join(price.split())

        price_final = []
        for i in price_new:
            i = i.replace('+', '').replace('G', '').replace('S', '').replace('T', '').replace(' ', '')
            price_final.append(i)

        prices = ''.join(price_final)
        prices = prices.replace('INR', 'INR ')

        skills = ' | '

        items['title'] = title
        items['description'] = description
        items['key_skills'] = skills.join(key_skills)
        items['prerequisites'] = prerequisites
        items['syllabus'] = syllabus
        items['prices'] = prices

        yield items

