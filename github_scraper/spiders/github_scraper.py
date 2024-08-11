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
        nickname = response.xpath('//span[@class="p-nickname vcard-username d-block"]/text()').get(default='').strip()
        
        vcard_details = response.xpath('//ul[@class="vcard-details"]')
        mails = [x for x in vcard_details.xpath('//a/@href').getall() if x.startswith('mailto:')]
        
        def extract_int(xpath):
            value = response.xpath(xpath).get(default='0').strip().replace(',', '')
            return int(value) if value.isdigit() else 0
        
        yield {
            'username': response.xpath('//span[@class="p-name vcard-fullname d-block overflow-hidden"]/text()').get(default='').strip(),
            'nickname': nickname,
            'twitter': vcard_details.xpath('//a[contains(@href, "twitter.com") or contains(@href, "x.com") or contains(@href, "https://x.com") or contains(@href, "https://twitter.com") or contains(@href, "www.twitter.com")]/@href').get(default=''),
            'instagram': vcard_details.xpath('//a[contains(@href, "instagram.com")]/@href').get(default=''),
            'linkedin': vcard_details.xpath('//a[contains(@href, "linkedin.com")]/@href').get(default=''),
            'website': vcard_details.xpath('//li[@itemprop="url"]/a/text()').getall(),
            'e-mail': mails[0] if len(mails) else '',
            'bio': response.xpath('//div[@class="p-note user-profile-bio mb-3 js-user-profile-bio f4"]/div/text()').get(default='').strip(),
            'location': vcard_details.xpath('//li[@itemprop="homeLocation"]/span/text()').get(default='').strip(),
            'public_repos': extract_int('(//span[@class="Counter"])[1]/text()'),
            'stars': extract_int('//a[contains(@href, "?tab=stars")]/span[@class="Counter"]/text()'),
            'organizations': int(float(response.xpath('count(//a[@data-hovercard-type="organization"])').get(default='0'))),
            'followers': extract_int('//a[contains(@href, "?tab=followers")]/span/text()'),
            'following': extract_int('//a[contains(@href, "?tab=following")]/span/text()'),
        }
