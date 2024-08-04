import scrapy
import requests

class GithubSpider(scrapy.Spider):
    name = 'github_scraper'
    allowed_domains = ['github.com']

    def start_requests(self):
        file_url = 'https://raw.githubusercontent.com/Illia-the-coder/github-scarp-bot/main/github_scraper/github_links.txt'
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            urls = response.text.splitlines()
            for url in urls:
                yield scrapy.Request(url=url.strip().replace('https://github.com/https://github.com/','https://github.com/'), callback=self.parse)
        except requests.RequestException as e:
            self.logger.error(f"Error fetching URLs: {e}")

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
            'public_repos': int(response.xpath('(//span[@class="Counter"])[1]/text()').get(default='0').strip()),
            'stars': response.xpath('//a[contains(@href, "?tab=stars")]/span[@class="Counter"]/text()').get(default='0').strip(),
            'organizations': len(response.xpath('//a[@data-hovercard-type="organization"]')),
            'followers': int(response.xpath('//a[contains(@href, "followers")]/svg/span/text()').get(default='0').strip()),
            'following': int(response.xpath('//a[contains(@href, "following")]/svg/span[@class="Counter"]/text()').get(default='0').strip()),
        }
