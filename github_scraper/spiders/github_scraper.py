import scrapy

class GithubSpider(scrapy.Spider):
    name = 'github_scraper'
    allowed_domains = ['github.com']

    def start_requests(self):
        with open('github_links.txt', 'r') as f:
            urls = f.readlines()
            for url in urls:
                yield scrapy.Request(url=url.strip(), callback=self.parse)

    def parse(self, response):
        
        yield {
            'username': response.xpath('//span[@class="p-name vcard-fullname d-block overflow-hidden"]/text()').get(default='').strip(),
            'nickname': response.xpath('//span[@class="p-nickname vcard-username d-block"]/text()').get(default='').strip(),
            'twitter': response.xpath('//a[contains(@href, "twitter.com")]/@href').get(default=''),
            'instagram': response.xpath('//a[contains(@href, "instagram.com")]/@href').get(default=''),
            'linkedin': response.xpath('//a[contains(@href, "linkedin.com")]/@href').get(default=''),
            'website': response.xpath('//a[@class="u-url"]/text()').get(default='').strip(),
            'email': response.xpath('//a[contains(@href, "mailto:")]/@href').get(default='').replace('mailto:', ''),
            'bio': response.xpath('//div[@class="p-note user-profile-bio mb-3 js-user-profile-bio f4"]/div/text()').get(default='').strip(),
            'location': response.xpath('//li[@itemprop="homeLocation"]/span/text()').get(default='').strip(),
            'public_repos': response.xpath('//span[@class="Counter"]/text()').extract()[0].strip() if response.xpath('//span[@class="Counter"]/text()').extract() else '0',
            'stars': response.xpath('//a[contains(@href, "?tab=stars")]/span[@class="Counter"]/text()').get(default='0').strip(),
            'organizations': len(response.xpath('//a[@data-hovercard-type="organization"]')),
            'followers': response.xpath('//a[contains(@href, "followers")]/span[@class="Counter"]/text()').get(default='0').strip(),
            'following': response.xpath('//a[contains(@href, "following")]/span[@class="Counter"]/text()').get(default='0').strip(),
        }
