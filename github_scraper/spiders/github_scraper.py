import scrapy
import requests

def text_to_int(text):
    # Clean the input by removing spaces and other non-numeric characters (except for '.', 'k', 'M', etc.)
    clean_text = text.strip().lower().replace('+', '').replace(',', '')

    # Mapping suffixes to their respective multipliers
    suffixes = {'k': 10**3, 'm': 10**6, 'b': 10**9}

    try:
        # If the text can be directly converted to an integer, do so
        return int(clean_text)
    except ValueError:
        # If there is a suffix, handle it
        for suffix, multiplier in suffixes.items():
            if clean_text.endswith(suffix):
                try:
                    # Convert the part before the suffix to a float, multiply by the appropriate value
                    return int(float(clean_text[:-1]) * multiplier)
                except ValueError:
                    return 0  # In case of any error during conversion

        # If it doesn't match any expected format, return 0
        return 0



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
            'public_repos':   text_to_int(response.xpath('(//span[@class="Counter"])[1]/text()').get(default='0')),
            'stars':  text_to_int(response.xpath('//a[contains(@href, "?tab=stars")]/span[@class="Counter"]/text()').get(default='0')),
            'organizations': len(response.xpath('//a[@data-hovercard-type="organization"]')),
            'followers': text_to_int(response.xpath('//a[contains(@href, "?tab=followers")]/span/text()').get(default='0')),
            'following':  text_to_int(response.xpath('//a[contains(@href, "?tab=following")]/span/text()').get(default='0')),
        }