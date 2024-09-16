import scrapy
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime, timedelta
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from scrapy.http import FormRequest
import pandas as pd
from pcd.items import PcdItem
# from pcd.items import NewsItem
class Update(scrapy.Spider , object ):
    name = 'updatestock'
    start_urls = [f'https://www.ilboursa.com/marches/historiques/AB']
    custom_settings = {'ITEM_PIPELINES': {"pcd.pipelines.PcdPipeline": 300}}
    my_value =''
    def __init__(self, companyName, process=None , *args, **kwargs):
        super(Update,self).__init__(*args, **kwargs)
        self.companyName = companyName
        self.process= process

    def start_requests(self):
        urls = f'https://www.ilboursa.com/marches/historiques/{self.companyName}'
        yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        items= PcdItem()
        date = response.css("#tblhistos td:nth-child(1)").css("::text").extract()
        items["close"] = response.css("#tblhistos td:nth-child(2)").css("::text").extract()
        items["open"] = response.css("#tblhistos td:nth-child(5)").css("::text").extract()
        items["high"] = response.css("#tblhistos td:nth-child(4)").css("::text").extract()
        items["low"]= response.css("#tblhistos td:nth-child(3)").css("::text").extract()
        items["date"]=date
        items["companyName"]=self.companyName
        yield items

    # def close(self):
    #     self.process.stop()
class CollectNews(scrapy.Spider):
    name = 'collectnews'
    start_urls = ['https://www.ilboursa.com/marches/news_valeur?p=1&s=ab']
    custom_settings = {'ITEM_PIPELINES': {"pcd.pipelines.NewsPipeline": 300}}
    # news = []
    # date = []
    i=1

    def __init__(self, companyName, process=None , *args, **kwargs):
        super(CollectNews,self).__init__(*args, **kwargs)
        self.companyName=  companyName
        self.process= process
        self.items = PcdItem()

    def start_requests(self):
        self.i = 1
        urls = f'https://www.ilboursa.com/marches/news_valeur?p=1&s={self.companyName}'
        yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        # items = response.meta.get('items')
        news = response.css(".lh25 a").css("::text").extract()
        date = response.css(".sp1").css("::text").extract()
        # self.news.extend(news)
        # self.date.extend(date)
        print("page number : ", self.i)
        self.i += 1
        if ((len(news) > 0) or (len(date) > 0)):
            yield scrapy.Request(
                url='https://www.ilboursa.com/marches/news_valeur?p=' + str(self.i) + f'&s={self.companyName}',
                callback=self.parse)
        self.items['date'] = date
        self.items['news'] = news
        self.items["companyName"] = self.companyName
        yield self.items

    # def close(self):
    #     if (self.process != None) : self.process.stop()
class UpdateNews(scrapy.Spider):
    name = 'updatenews'
    start_urls = ['https://www.ilboursa.com/marches/news_valeur?p=1&s=ab']
    custom_settings = {'ITEM_PIPELINES': {"pcd.pipelines.NewsPipeline": 300}}
    # news = []
    # date = []


    def __init__(self, companyName, process=None , *args, **kwargs):
        super(UpdateNews,self).__init__(*args, **kwargs)
        self.companyName=  companyName
        self.process= process
        self.items = PcdItem()

    def start_requests(self):
        urls = f'https://www.ilboursa.com/marches/news_valeur?p=1&s={self.companyName}'
        yield scrapy.Request(url=urls, callback=self.parse)


    def parse(self, response):
        # items = response.meta.get('items')
        news = response.css(".lh25 a").css("::text").extract()
        date = response.css(".sp1").css("::text").extract()
        # self.news.extend(news)
        # self.date.extend(date)

        self.items['date'] = date
        self.items['news'] = news
        self.items["companyName"] = self.companyName
        yield self.items

    # def close(self):
    #     if (self.process != None) : self.process.stop()
class FullData(scrapy.Spider):
    name = 'news1'
    start_urls = ['https://www.ilboursa.com/marches/news_valeur?p=1&s=BIAT']
    news = []
    date = []
    i=1

    def BiatPageNews(self,response ):
        news = response.css("#block-biat-corporate-content .field--name-node-title a").css("::text").extract()
        date = response.css("#block-biat-corporate-content .field--name-node-post-date").css("::text").extract()
        self.news.extend(news)
        self.date.extend(date)
        self.i += 1
        if ((len(news) > 0) or (len(date) > 0)):
            print("page number : ", self.i)
            yield scrapy.Request(url='https://www.biat.com.tn/biat-la-une/actualites?filter_theme=All&current_path=/node/49&keyword=&meta_key=&page=' + str(self.i),
                                 callback=self.BiatPageNews)


        df = pd.DataFrame({'date': self.date, 'news': self.news})
        df.to_csv("BIAT_News.csv", index=False)
        yield {'news': self.news, 'date': self.date}



    def parse(self, response):
        # news=response.css(".lh25 a").css("::text").extract()
        # date=response.css(".sp1").css("::text").extract()
        # self.news.extend(news)
        # self.date.extend(date)
        # self.i+=1
        # if ((len(news) > 0) or (len(date) > 0)):
        #     print("page number : " , self.i)
        #     yield scrapy.Request(url='https://www.ilboursa.com/marches/news_valeur?p='+str(self.i)+'&s=BIAT', callback=self.parse)
        #
        self.i=0

        url='https://www.biat.com.tn/biat-la-une/actualites?filter_theme=All&current_path=/node/49&keyword=&meta_key=&page=0'
        yield scrapy.Request(url, callback=self.BiatPageNews)
class Collect(scrapy.Spider):
    name = 'collect1'
    start_urls = ['https://www.ilboursa.com/marches/historiques/BIAT']

    def parse(self, response):
        # Change the first date
        yield FormRequest.from_response(response,
                                        formdata={'datefrom': '2018-10-16', 'dateto': '2018-11-16'},
                                        clickdata={'id': 'btnChange'},
                                        callback=self.parse_results)

    def parse_results(self, response):
        # Do the web scraping on the page that is shown after pressing the OK button
        # You can use XPath or CSS selectors to extract the data that you need
        data = response.css("#tblhistos td").css("::text").extract()
        yield {'data': data}
#collect stock data from ilboursa
class DataCollectionSpiderIlboursa(scrapy.Spider):
    name = "ilboursa_data1"
    start_urls = [
        'https://www.ilboursa.com/marches/historiques/BIAT'
    ]
    # Get today's date
    lastdate_date = datetime.now()

    # Subtract 3 months from today's date
    firstdate_date = lastdate_date - timedelta(days=90)
    pagenumbers=2


    def saveInCSVFile(self, name , data):
        with open(name+'.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for i in range(0, len(data), 8):
                row = data[i:i + 8]
                writer.writerow(row)

    def collect_data(self,driver,firstdate , lastdate):
        # Find the date inputs and enter the desired dates
        datefrom = driver.find_element(By.ID, "datefrom")
        datefrom.clear()
        datefrom.send_keys(firstdate)

        dateto = driver.find_element(By.ID, "dateto")
        dateto.clear()
        dateto.send_keys(lastdate)

        # Wait for the OK button to become clickable
        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnChange"))
        )
        ok_button.click()


        # collect data with selenium  but its too slow

        # Wait for the page to load and find the table
        # try:
        #     table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tblhistos")))
        #     data = table.find_elements(By.CSS_SELECTOR, "td")
        #     data = [d.text for d in data]
        #
        # except StaleElementReferenceException:
        #     # If element not found, refresh and try again
        #     # driver.refresh()
        #     table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tblhistos")))
        #     data = table.find_elements(By.CSS_SELECTOR, "td")
        #     data = [d.text for d in data]

        #****** data collection the fastest way ********
        time.sleep(1)
        try:
            # Wait for the table to become present and then extract the data
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tblhistos")))
            html = table.get_attribute('innerHTML')
            sel = Selector(text=html)
            data = sel.css('td::text').extract()

        except StaleElementReferenceException:
            # If element not found, refresh and try again
            # driver.refresh()
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tblhistos")))
            html = table.get_attribute('innerHTML')
            sel = Selector(text=html)
            data = sel.css('td::text').extract()

        return data



    def parse(self, response):

        # Create a new instance of the Firefox driver
        chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        # driver_path = "C:\path\to\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path

        driver = webdriver.Chrome( chrome_options=options )
        # Load the website
        driver.get("https://www.ilboursa.com/marches/historiques/BIAT")

        # get names(values) an abreviations(keys) of tunisia companies in a dic
        options = response.css('#dpShares option')[1:]
        companieNames = {option.attrib['value']: option.css('::text').get().strip() for option in options}






        for companieName in companieNames.keys():
            # vider data
            data=[]
            # Get today's date
            DataCollectionSpiderIlboursa.lastdate_date = datetime.now()

            # Subtract 3 months from today's date
            DataCollectionSpiderIlboursa.firstdate_date = DataCollectionSpiderIlboursa.lastdate_date - timedelta(days=90)
            driver.get("https://www.ilboursa.com/marches/historiques/"+companieName)
            time.sleep(2)
            datefortest = "7atachay"
            while (True):
                # Format the date as "dd-mm-yyyy"
                firstdate = DataCollectionSpiderIlboursa.firstdate_date.strftime('%d-%m-%Y')
                lastdate = DataCollectionSpiderIlboursa.lastdate_date.strftime('%d-%m-%Y')
                threemonthsdata = self.collect_data(driver, firstdate, lastdate)
                if (len(threemonthsdata) >0 ):
                    if( threemonthsdata[0] == datefortest) :
                        break
                else : break
                datefortest = threemonthsdata[0]
                data.extend(threemonthsdata)
                # Get the last date
                DataCollectionSpiderIlboursa.lastdate_date = DataCollectionSpiderIlboursa.lastdate_date - timedelta(days=91)
                # Subtract 3 months from today's date
                DataCollectionSpiderIlboursa.firstdate_date = DataCollectionSpiderIlboursa.lastdate_date - timedelta(days=90)


            self.saveInCSVFile(companieName+'_data' , data)

        # time.sleep(10)

        # Close the driver
        driver.quit()

        print("*****  the  length : ",len(data))

        # Return the scraped data
        yield {'data': data}

        # self.saveInCSVFile('data' , data)
#colect stock data from investing
class DataColectionSpiderInvesting(scrapy.Spider):
    name = "investing_data1"
    start_urls = [
        'https://www.investing.com/equities/air-liquide-tunisie-historical-data'
    ]

    def parse(self, response):
        # get dates
        todayDate = datetime.now().strftime('%d-%m-%Y')
        lastdate = '01-01-1990'

        # Create a new instance of the chrome driver
        chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path

        driver = webdriver.Chrome(chrome_options=options)


        # Load the website
        driver.get("https://www.investing.com/equities/air-liquide-tunisie-historical-data")

        time.sleep(2)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.navbar_navbar-sub-item__pKz6J:nth-child(1) .navbar_navbar-sub-item-link__Gx8Mt')))
        driver.execute_script("arguments[0].click();", element)
        print('it is clicked')

        time.sleep(10)


        # wait for the date range input elements to load
        date_range_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'NativeDateInput_root__wbgyP')))
        date_inputs = date_range_div.find_elements_by_tag_name('input')

        # enter the dates
        date_inputs[0].send_keys('01/01/1990')
        date_inputs[1].send_keys('02/15/2023')

        # get the apply button
        apply_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="historical-data_history-date-picker-wrapper__dDOuq"]//button')))

        # click the apply button using JavaScript
        driver.execute_script("arguments[0].click();", apply_button)

        # wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'download-data_download-data__jxNYT')))

        # get the download link
        download_link = driver.find_element_by_xpath('//div[@class="download-data_download-data__jxNYT"]/a')

        # click the download link
        download_link.click()

        time.sleep(10)
        driver.quit()






        # # Find the date input fields
        # date_inputs = response.css(
        #     '//div[contains(@class, "NativeDateRangeInput_root__7PylR")]//input[contains(@class, "NativeDateInput_input__3RJzK")]')
        # first_date_input, second_date_input = date_inputs[:2]
        #
        # # Set the new dates
        # first_date_input.attrib['value'] = '1990-01-01'
        # second_date_input.attrib['value'] = '2023-02-15'
        #
        # # Find and click the apply button
        # apply_button = response.xpath(
        #     '//div[contains(@class, "historical-data_history-date-picker-wrapper__dDOuq")]//button[contains(@class, "HistoryDatePicker_apply-button__fPr_G")]')
        # yield from response.follow(apply_button[0], self.parse)
        #
        # # Find and click the download link
        # download_link = response.xpath('//div[contains(@class, "download-data_download-data__jxNYT")]//a')
        # yield from response.follow(download_link[0], self.parse)



        # Return the scraped data
        yield {'data': 0}


