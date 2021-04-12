import scrapy
from io import open
import os
import pathlib
import datetime as date
import requests
import json
class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    BASE_DIR = str(pathlib.Path().absolute())
    BASE_FILE = str(pathlib.Path().absolute()) + "/home.html"
    DOMAIN = "https://www2.sgc.gov.co"
    start_urls = [
        f"file:{BASE_FILE}"
    ]
#"file:C:\Users\cacer\Documents\python_courses\webcrawler\home.html"
    def concat_json(self):
        first_fifth = []
        ## requests.get() convert a json request to a dictionary object !!!
        req = requests.get('https://s3.amazonaws.com/sgc.sites.gov.co/feed/v1.0/summary/thirty_days_importan.json')
        
        if req.status_code == 200:
            results = req.json()
            first_fifth = [
                results['features'][0],
                results['features'][1],
                results['features'][2],
                results['features'][3],
                results['features'][4]
            ]
        return first_fifth
    """
    the first parameter is the local file to save the download image
    the second parameter is the image to download
    """
    def download_files(self, local_path, url_image):
        image = requests.get(url_image).content
        with open(local_path, 'wb') as handler:
        	handler.write(image)
    
    def create_folder(self, path):
        os.mkdir(f"{self.BASE_DIR}{path}") if not os.path.isdir(f"{self.BASE_DIR}{path}") else print('folder already exists')

    def parse(self, response):
        ## if the folder dont exist the os create the folder for download the images
        self.create_folder('/assets/banner')
        self.create_folder('/assets/contracts')
        self.create_folder('/assets/news')
        ## Scraping for the home webste according the slider, news and contract section
        banner_assets = []
        contracts_assets = []
        news_assets = []
        
        ## Banner Scraping
        banner = response.css('.bxHome')
        banner_images = banner.css('img::attr(src)').extract()
        banner_links = banner.css('ul li a').xpath('@href').extract()
        ## Contract Scraping
        contract_links = response.xpath('//div[@id="sgc-uContratog_e46649e2_22b6_47c2_b37f_cda342078c1b"]/div[@class="info"]/ul/li/p/a/@href').extract()
        contract_names = response.xpath('//div[@id="sgc-uContratog_e46649e2_22b6_47c2_b37f_cda342078c1b"]/div[@class="info"]/ul/li/p/a/text()').extract()
        contract_images = response.css('.icon img::attr(src)').extract()
        ## News scraping
        news = response.css('.noticiaItem')
        news_images = news.css('img::attr(src)').extract()
        news_date = news.css('.infoNoticias .date::text').extract()
        news_category = news.css('.infoNoticias .categoria::text').extract()
        news_text = response.css('.infoNoticias a::text').extract()
        news_links = response.css('.infoNoticias a::attr(href)').extract()


        for banner_count in range(0,len(banner_images)):

            banner_images[banner_count] = f"{self.DOMAIN}{banner_images[banner_count]}" # the link image to download
            ## Downloads the images at the banner folder
            file_name = f"/assets/banner/{date.datetime.today().timestamp()}.png"
            local_image = f"{self.BASE_DIR}{file_name}" # the name for saved
            self.download_files(local_image,banner_images[banner_count])
            ## if the link has not http so concat the domain with link
            banner_links[banner_count] = f"{self.DOMAIN}{banner_links[banner_count]}" if banner_links[banner_count].find('http') == -1 else banner_links[banner_count] 
            banner_assets.append({
                'link': banner_links[banner_count],
                'img': banner_images[banner_count],
                'local':file_name
            })
        
        
        for link in range(0,len(news_links)):

            ## the contract images array have the same size than the news links
            ## so the array take images contract links
            
            contract_images[link] = f"{self.DOMAIN}{contract_images[link]}" if contract_images[link].find('http') == -1 else contract_images[link]
            file_name = f"/assets/contracts/image{link}.png"
            local_image = f"{self.BASE_DIR}{file_name}" # the name for saved in the local machine
            self.download_files(local_image,contract_images[link])
            contracts_assets.append({
                'link': contract_links[link],
                'name': contract_names[link],
                'images':contract_images[link],
                'local': file_name
            })

            ## news links and images
            news_links[link] = f"{self.DOMAIN}{news_links[link]}" if news_links[link].find('http') == -1 else news_links[link]
            
            ## Downloads the images at the news folder
            
            file_name = f"/assets/news/{date.datetime.today().timestamp()}.png"
            local_image = f"{self.BASE_DIR}{file_name}" # the name for saved
            
            self.download_files(local_image,news_images[link])
            news_assets.append({
                'img': news_images[link],
                'date': news_date[link],
                'link':news_links[link],
                'category': news_category[link],
                'description': news_text[link]
            })
        yield {
            'slider':banner_assets,
            'contracts': contracts_assets,
            'latestnews': news_assets,
            'firstEQ': self.concat_json()
        }
        ##links = response.css('div.seccionMap li a').xpath('@href').extract()
        ##yield {'links': links}